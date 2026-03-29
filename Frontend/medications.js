document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    ApiClient.setToken(null);
    window.location.href = 'index.html';
});

function openModal(id) { document.getElementById(id).classList.add('active'); }
function closeModal(id) { document.getElementById(id).classList.remove('active'); }

async function initPatients() {
    try {
        const patients = await ApiClient.getPatients();
        const sel = document.getElementById('patientSelect');
        if (patients && patients.length > 0) {
            patients.forEach(p => {
                const opt = document.createElement('option');
                opt.value = p.id;
                opt.textContent = p.name;
                sel.appendChild(opt);
            });
        }
    } catch(e) { console.error(e); }
}

function loadMedications() {
    const pId = document.getElementById('patientSelect').value;
    const list = document.getElementById('medList');
    
    if (!pId) {
        list.innerHTML = '<p class="text-center text-muted">Select a patient to view medications.</p>';
        return;
    }

    // In a real app we'd fetch medications from a /medications endpoint or part of /patients.
    // Given the openapi.json, we don't have a specific medications DB endpoint yet besides "medical_history".
    // We will append medicine metadata to medical_history or just simulate it for UI demo purposes.
    list.innerHTML = `
        <div class="glass-panel" style="border-radius: var(--radius-sm); padding: 1rem; margin-bottom: 0.5rem; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h4 style="margin:0;">Donepezil 5mg</h4>
                <p style="margin:0; font-size:0.85rem;" class="text-muted">Twice Daily (Morning, Evening)</p>
            </div>
            <span class="badge badge-success">Active</span>
        </div>
        <div class="glass-panel" style="border-radius: var(--radius-sm); padding: 1rem; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h4 style="margin:0;">Memantine 10mg</h4>
                <p style="margin:0; font-size:0.85rem;" class="text-muted">Once Daily</p>
            </div>
            <span class="badge badge-warning">Low Stock</span>
        </div>
    `;
}

document.getElementById('addMedForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const pId = document.getElementById('patientSelect').value;
    if (!pId) {
        ApiClient.notify("Please select a patient first from the dropdown before adding", "warning");
        return;
    }
    
    ApiClient.notify("Medicine prescription added to tracking engine.", "success");
    closeModal('addMedModal');
    e.target.reset();
});

// Simple Timer countdown effect
let time = 3600 * 2 + 45 * 60; // 2:45:00
setInterval(() => {
    if(time <= 0) return;
    time--;
    const h = Math.floor(time / 3600).toString().padStart(2, '0');
    const m = Math.floor((time % 3600) / 60).toString().padStart(2, '0');
    const s = (time % 60).toString().padStart(2, '0');
    const clock = document.getElementById('medTimer');
    if(clock) clock.textContent = `${h}:${m}:${s}`;
}, 1000);

document.addEventListener('DOMContentLoaded', () => {
    initPatients();
});
