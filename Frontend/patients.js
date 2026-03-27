document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    ApiClient.setToken(null);
    window.location.href = 'index.html';
});

// Modal controls
function openModal(id) { document.getElementById(id).classList.add('active'); }
function closeModal(id) { document.getElementById(id).classList.remove('active'); }

function switchDetailTab(tabId) {
    document.querySelectorAll('.detail-tab').forEach(t => t.style.display = 'none');
    document.getElementById(`tab-${tabId}`).style.display = 'block';
    document.querySelectorAll('.tab-link').forEach(l => l.classList.remove('active'));
    event.target.classList.add('active');
    
    // Hide save button if on team linking tab
    document.getElementById('updateActions').style.display = tabId === 'team' ? 'none' : 'block';
}

async function loadPatients() {
    try {
        const patients = await ApiClient.getPatients();
        const grid = document.getElementById('patientsGrid');
        grid.innerHTML = '';

        if (!patients || patients.length === 0) {
            grid.innerHTML = '<p class="text-muted">No patients found. Create one.</p>';
            return;
        }

        patients.forEach(p => {
            const initial = p.name ? p.name.charAt(0).toUpperCase() : '?';
            const card = document.createElement('div');
            card.className = 'glass-card patient-card';
            card.onclick = () => openPatientDetails(p);
            card.innerHTML = `
                <div class="flex align-center gap-4 mb-4">
                    <div class="avatar">${initial}</div>
                    <div>
                        <h3 style="margin:0">${p.name}</h3>
                        <div class="badge badge-success mt-1">Active</div>
                    </div>
                </div>
                <div class="text-muted" style="font-size: 0.9rem;">
                    <p style="margin-bottom:0.25rem;"><strong>Age:</strong> ${p.age}</p>
                    <p style="margin-bottom:0px;"><strong>Phone:</strong> ${p.phone}</p>
                </div>
            `;
            grid.appendChild(card);
        });

    } catch (e) {
        document.getElementById('patientsGrid').innerHTML = '<p class="text-danger">Failed to load patients.</p>';
        console.error(e);
    }
}

async function loadLookups() {
    try {
        const caretakers = await ApiClient.getCaretakers();
        const doctors = await ApiClient.getDoctors();
        
        const ctSelect = document.getElementById('linkCaretakerId');
        ctSelect.innerHTML = caretakers && caretakers.length > 0 ? 
            caretakers.map(c => `<option value="${c.id}">${c.name}</option>`).join('') :
            '<option disabled>No Caretakers available</option>';

        const docSelect = document.getElementById('linkDoctorId');
        docSelect.innerHTML = doctors && doctors.length > 0 ? 
            doctors.map(d => `<option value="${d.id}">${d.name}</option>`).join('') :
            '<option disabled>No Doctors available</option>';

    } catch(e) { console.error("Lookup error:", e); }
}

async function openPatientDetails(p) {
    document.getElementById('editPatientId').value = p.id;
    document.getElementById('epName').value = p.name || '';
    document.getElementById('epAge').value = p.age || '';
    document.getElementById('epAddress').value = p.address || '';
    document.getElementById('epPhone').value = p.phone || '';
    document.getElementById('epHistory').value = p.medical_history || '';
    document.getElementById('detailName').textContent = p.name;
    
    openModal('patientDetailModal');
}

document.getElementById('addPatientForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('pUsername').value,
        email: document.getElementById('pEmail').value,
        password: document.getElementById('pPassword').value,
        name: document.getElementById('pName').value,
        age: parseInt(document.getElementById('pAge').value),
        address: document.getElementById('pAddress').value,
        phone: document.getElementById('pPhone').value,
        medical_history: document.getElementById('pHistory').value || "",
    };

    try {
        await ApiClient.registerPatient(data);
        ApiClient.notify("Patient added successfully!");
        closeModal('addPatientModal');
        e.target.reset();
        loadPatients();
    } catch (err) {
        ApiClient.notify(err.message || "Failed to add patient", "error");
    }
});

document.getElementById('updatePatientForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('editPatientId').value;
    const data = {};
    if (document.getElementById('epName').value) data.name = document.getElementById('epName').value;
    if (document.getElementById('epAge').value) data.age = parseInt(document.getElementById('epAge').value);
    if (document.getElementById('epAddress').value) data.address = document.getElementById('epAddress').value;
    if (document.getElementById('epPhone').value) data.phone = document.getElementById('epPhone').value;
    
    // History
    if (document.getElementById('epHistory').value !== undefined) {
        data.medical_history = document.getElementById('epHistory').value;
    }

    try {
        await ApiClient.updatePatient(id, data);
        ApiClient.notify("Patient updated successfully!");
        closeModal('patientDetailModal');
        loadPatients();
    } catch (err) {
        ApiClient.notify(err.message || "Failed to update patient", "error");
    }
});

async function linkCaretaker() {
    const pId = document.getElementById('editPatientId').value;
    const ctId = document.getElementById('linkCaretakerId').value;
    if (!ctId) return alert("Select Caretaker");
    
    try {
        await ApiClient.createCaretakerLink({ patient_id: parseInt(pId), caretaker_id: parseInt(ctId) });
        ApiClient.notify("Caretaker linked!");
    } catch(e) { ApiClient.notify(e.message, "error"); }
}

async function linkDoctor() {
    const pId = document.getElementById('editPatientId').value;
    const dId = document.getElementById('linkDoctorId').value;
    if (!dId) return alert("Select Doctor");
    
    try {
        await ApiClient.createDoctorLink({ patient_id: parseInt(pId), doctor_id: parseInt(dId) });
        ApiClient.notify("Doctor linked!");
    } catch(e) { ApiClient.notify(e.message, "error"); }
}

document.addEventListener('DOMContentLoaded', () => {
    loadPatients();
    loadLookups();
});
