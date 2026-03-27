document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    ApiClient.setToken(null);
    window.location.href = 'index.html';
});

function openModal(id) { document.getElementById(id).classList.add('active'); }
function closeModal(id) { document.getElementById(id).classList.remove('active'); }

async function initDropdown() {
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

async function simulateTracking() {
    const pId = document.getElementById('patientSelect').value;
    const map = document.getElementById('mapWidget');
    if (!pId) {
        map.innerHTML = '<span>Select a patient to view telemetry...</span>';
        return;
    }

    map.innerHTML = '<div class="location-pin" style="top:50%; left:50%;"></div>';
    
    // Attempt to load places assigned to this user (we assign places to user_id)
    loadPlaces(pId);
}

async function loadPlaces(userId) {
    const list = document.getElementById('placesList');
    try {
        const places = await ApiClient.getPlaces(userId);
        
        // Sometimes backend returns empty if not implemented thoroughly, fallback UI:
        list.innerHTML = '';
        if (places && places.length > 0) {
            places.forEach(p => {
                const div = document.createElement('div');
                div.style.cssText = "padding: 1rem; border-bottom: 1px solid var(--surface-border); display:flex; justify-content:space-between; align-items:center;";
                div.innerHTML = `
                    <div>
                        <div style="font-weight: 500">${p.name || p.label}</div>
                        <div style="font-size:0.85rem;" class="text-muted">Rad: ${p.geofence_radius_m}m | Lat:${p.lat}</div>
                    </div>
                `;
                list.appendChild(div);
            });
        } else {
            list.innerHTML = '<p class="text-center text-muted">No safe places designated.</p>';
        }
    } catch(err) {
        list.innerHTML = '<p class="text-center text-muted">Error loading places.</p>';
    }
}

document.getElementById('addPlaceForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const pId = document.getElementById('patientSelect').value;
    
    if(!pId) {
        return ApiClient.notify("Please select a target patient from the map dropdown first to assign this place to.", "warning");
    }

    const data = {
        label: document.getElementById('plLabel').value,
        name: document.getElementById('plName').value,
        lat: parseFloat(document.getElementById('plLat').value),
        lng: parseFloat(document.getElementById('plLng').value),
        address: document.getElementById('plAddress').value,
        geofence_radius_m: parseInt(document.getElementById('plRadius').value)
    };

    try {
        await ApiClient.addPlace(pId, data);
        ApiClient.notify("Safe Place designated successfully!");
        closeModal('addPlaceModal');
        e.target.reset();
        loadPlaces(pId);
    } catch (err) {
        ApiClient.notify(err.message, "error");
    }
});

async function simulateLocationUpdate() {
    const pId = document.getElementById('patientSelect').value;
    if(!pId) return;

    // Simulate sending tracking ping
    try {
        await ApiClient.updateLocation(pId, {
            lat: 12.9716,
            lng: 77.5946,
            timestamp: Date.now() / 1000
        });
        ApiClient.notify("Live location pinged successfully", "success");
        
        // Randomly offset the map pin
        const pin = document.querySelector('.location-pin');
        if(pin) {
            const rx = 40 + Math.random() * 20;
            const ry = 40 + Math.random() * 20;
            pin.style.top = `${ry}%`;
            pin.style.left = `${rx}%`;
        }
    } catch(e) {
        ApiClient.notify(e.message, "error");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initDropdown();
});
