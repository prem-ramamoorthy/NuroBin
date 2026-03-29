document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    ApiClient.setToken(null);
    window.location.href = 'index.html';
});

// Load profile for header
async function loadProfile() {
    try {
        const profile = await ApiClient.getProfile();
        if (profile) {
            document.getElementById('userName').textContent = profile.name || profile.username;
            document.getElementById('userRole').textContent = profile.role.charAt(0).toUpperCase() + profile.role.slice(1);
            document.getElementById('userInitial').textContent = (profile.name || profile.username).charAt(0).toUpperCase();
            
            // Set current date
            document.getElementById('currDate').textContent = new Date().toLocaleDateString('en-US', { 
                weekday: 'long', month: 'long', day: 'numeric' 
            });

            // Store role globally for UI logic
            window.userRole = profile.role;
        }
    } catch (e) { console.error("Profile load error:", e); }
}

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
            
            const deleteBtn = (window.userRole === 'doctor' || window.userRole === 'admin') ? 
                `<button onclick="event.stopPropagation(); deletePatientAccount(${p.id})" class="btn" style="position:absolute; top:10px; right:10px; color:var(--danger); padding:0.25rem;">
                    <svg style="width:16px;height:16px" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>` : '';

            card.style.position = 'relative';
            card.onclick = () => openPatientDetails(p);
            card.innerHTML = `
                ${deleteBtn}
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

async function deletePatientAccount(id) {
    const modal = document.getElementById('deleteConfirmModal');
    modal.classList.add('active');
    
    // Clear old listeners by cloning the button
    const oldBtn = document.getElementById('confirmDeleteBtn');
    const newBtn = oldBtn.cloneNode(true);
    oldBtn.parentNode.replaceChild(newBtn, oldBtn);
    
    newBtn.addEventListener('click', async () => {
        try {
            newBtn.disabled = true;
            newBtn.textContent = "Deleting...";
            const endpoint = window.userRole === 'admin' ? `/admin/user/${id}` : `/doctors/manage/patient/${id}`;
            await ApiClient.request(endpoint, { method: 'DELETE' });
            ApiClient.notify("Patient removed successfully");
            closeModal('deleteConfirmModal');
            loadPatients();
        } catch (e) { 
            ApiClient.notify(e.message, "error"); 
            newBtn.disabled = false;
            newBtn.textContent = "Delete Now";
        }
    });
}

async function loadLookups() {
    try {
        const caretakers = await ApiClient.getCaretakers();
        const doctors = await ApiClient.getDoctors();
        
        const ctSelect = document.getElementById('linkCaretakerId');
        if (ctSelect) {
            ctSelect.innerHTML = '<option value="" disabled selected>Select Caretaker...</option>';
            if (caretakers && caretakers.length > 0) {
                caretakers.forEach(c => {
                    const opt = document.createElement('option');
                    opt.value = c.id;
                    opt.textContent = c.name + " (ID: " + c.id + ")";
                    ctSelect.appendChild(opt);
                });
            } else {
                ctSelect.innerHTML = '<option disabled>No Caretakers available</option>';
            }
        }

        const docSelect = document.getElementById('linkDoctorId');
        if (docSelect) {
            docSelect.innerHTML = '<option value="" disabled selected>Select Doctor...</option>';
            if (doctors && doctors.length > 0) {
                doctors.forEach(d => {
                    const opt = document.createElement('option');
                    opt.value = d.id;
                    opt.textContent = d.name + " (ID: " + d.id + ")";
                    docSelect.appendChild(opt);
                });
            } else {
                docSelect.innerHTML = '<option disabled>No Doctors available</option>';
            }
        }

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
    
    // Load links
    loadPatientTeam(p.id);
    
    openModal('patientDetailModal');
}

async function loadPatientTeam(patientId) {
    try {
        const ctLinks = await ApiClient.getCaretakerLinks();
        const docLinks = await ApiClient.getDoctorLinks();
        
        const ctList = ctLinks.filter(l => l.patient_id === patientId);
        const dList = docLinks.filter(l => l.patient_id === patientId);
        
        const container = document.getElementById('currentLinksContainer');
        if (!container) {
            // Need to add this to the HTML
            const teamTab = document.getElementById('tab-team');
            const newContainer = document.createElement('div');
            newContainer.id = 'currentLinksContainer';
            newContainer.style.marginTop = '1.5rem';
            teamTab.appendChild(newContainer);
        }
        
        const c = document.getElementById('currentLinksContainer');
        c.innerHTML = '<h4>Active Team</h4>';
        
        if (ctList.length === 0 && dList.length === 0) {
            c.innerHTML += '<p class="text-muted">No team members linked.</p>';
        }

        ctList.forEach(l => {
            c.innerHTML += `
                <div class="flex justify-between align-center p-2 border-b">
                    <span>Caretaker ID: ${l.caretaker_id}</span>
                    <button class="btn btn-danger" style="padding:0.2rem 0.5rem; font-size:0.75rem;" onclick="unlinkCaretaker(${l.id})">Unlink</button>
                </div>
            `;
        });
        
        dList.forEach(l => {
            c.innerHTML += `
                <div class="flex justify-between align-center p-2 border-b">
                    <span>Doctor ID: ${l.doctor_id}</span>
                </div>
            `;
        });

    } catch(e) { console.error(e); }
}

async function unlinkCaretaker(linkId) {
    if (!confirm("Remove this caretaker from the team?")) return;
    try {
        await ApiClient.request(`/caretaker-patient-links/${linkId}`, { method: 'DELETE' });
        ApiClient.notify("Caretaker unlinked");
        loadPatientTeam(parseInt(document.getElementById('editPatientId').value));
    } catch(e) { ApiClient.notify(e.message, "error"); }
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
        loadPatientTeam(parseInt(pId));
    } catch(e) { ApiClient.notify(e.message, "error"); }
}

async function linkDoctor() {
    const pId = document.getElementById('editPatientId').value;
    const dId = document.getElementById('linkDoctorId').value;
    if (!dId) return alert("Select Doctor");
    
    try {
        await ApiClient.createDoctorLink({ patient_id: parseInt(pId), doctor_id: parseInt(dId) });
        ApiClient.notify("Doctor linked!");
        loadPatientTeam(parseInt(pId));
    } catch(e) { ApiClient.notify(e.message, "error"); }
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadProfile();
    loadPatients();
    loadLookups();
});
