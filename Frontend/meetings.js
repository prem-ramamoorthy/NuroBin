document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    ApiClient.setToken(null);
    window.location.href = 'index.html';
});

function openModal(id) { document.getElementById(id).classList.add('active'); }
function closeModal(id) { document.getElementById(id).classList.remove('active'); }

async function initLookups() {
    try {
        const patients = await ApiClient.getPatients();
        const doctors = await ApiClient.getDoctors();
        const caretakers = await ApiClient.getCaretakers();

        const ps = document.getElementById('mPatient');
        if (patients) patients.forEach(p => ps.innerHTML += `<option value="${p.id}">${p.name}</option>`);

        const ds = document.getElementById('mDoctor');
        if (doctors) doctors.forEach(p => ds.innerHTML += `<option value="${p.id}">${p.name}</option>`);

        const cs = document.getElementById('mCaretaker');
        if (caretakers) caretakers.forEach(p => cs.innerHTML += `<option value="${p.id}">${p.name}</option>`);

    } catch(e) { console.error(e); }
}

async function loadMeetings() {
    const list = document.getElementById('meetingsList');
    try {
        const meetings = await ApiClient.getMeetings();
        list.innerHTML = '';

        if (!meetings || meetings.length === 0) {
            list.innerHTML = '<p class="text-muted">No meetings scheduled.</p>';
            return;
        }

        // Sort by scheduled time
        meetings.sort((a,b) => new Date(a.scheduled_time) - new Date(b.scheduled_time));

        meetings.forEach(m => {
            const date = new Date(m.scheduled_time);
            const month = date.toLocaleString('default', { month: 'short' });
            const day = date.getDate();
            const time = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            const card = document.createElement('div');
            card.className = 'glass-card meeting-card mb-4';
            card.innerHTML = `
                <div class="time-block">
                    <div class="month">${month}</div>
                    <div class="day">${day}</div>
                    <div class="text-muted" style="font-size:0.85rem; margin-top:0.25rem;">${time}</div>
                </div>
                <div class="details">
                    <h3 style="margin-bottom:0.25rem;">Clinical Consultation (Doc ID: ${m.doctor_id})</h3>
                    <p class="text-muted" style="margin-bottom:0.5rem; font-size: 0.9rem;">Patient ID: ${m.patient_id} • Duration: ${m.duration_minutes}m</p>
                    <span class="badge badge-${m.status === 'completed'? 'success' : 'primary'}">${m.status}</span>
                </div>
                <div class="actions">
                    <button class="btn btn-secondary">Join Call</button>
                </div>
            `;
            list.appendChild(card);
        });

    } catch(e) {
        list.innerHTML = '<p class="text-danger">Error loading meetings.</p>';
    }
}

document.getElementById('addMeetingForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Ensure accurate offset string format 2026-03-27T10:00:00Z format
    let localTime = document.getElementById('mTime').value;
    const utcdatestr = new Date(localTime).toISOString();

    const data = {
        patient_id: parseInt(document.getElementById('mPatient').value),
        doctor_id: parseInt(document.getElementById('mDoctor').value),
        scheduled_time: utcdatestr,
        duration_minutes: parseInt(document.getElementById('mDuration').value),
        notes: document.getElementById('mNotes').value
    };

    const cId = document.getElementById('mCaretaker').value;
    if (cId) data.caretaker_id = parseInt(cId);

    try {
        await ApiClient.createMeeting(data);
        ApiClient.notify("Meeting scheduled successfully");
        closeModal('addMeetingModal');
        e.target.reset();
        loadMeetings();
    } catch (err) {
        ApiClient.notify(err.message, "error");
    }
});

document.addEventListener('DOMContentLoaded', () => {
    initLookups();
    loadMeetings();
});
