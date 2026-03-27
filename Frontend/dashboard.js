document.addEventListener('DOMContentLoaded', async () => {
  // Set date
  document.getElementById('currDate').textContent = new Date().toLocaleDateString('en-US', { 
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
  });

  // Logout handler
  document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    ApiClient.setToken(null);
    window.location.href = 'index.html';
  });

  try {
    // Optionally fetch /profile if available (currently assuming not strict or use fallback)
    // For now, populate with placeholder/fallback
    document.getElementById('userName').textContent = "Admin";
    document.getElementById('userInitial').textContent = "A";

    // Load actual patients
    const patients = await ApiClient.getPatients();
    document.getElementById('totalPatients').textContent = patients ? patients.length : 0;
    
    // Render patient table (recent 5)
    const tbody = document.getElementById('patientsTableBody');
    tbody.innerHTML = '';
    
    if (patients && patients.length > 0) {
      patients.slice(0, 5).forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><div style="font-weight: 500;">${p.name}</div></td>
          <td>${p.age} yrs</td>
          <td>${p.phone}</td>
          <td><span class="badge badge-success">Stable</span></td>
        `;
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No patients found.</td></tr>';
    }

    // Load actual meetings
    const meetings = await ApiClient.getMeetings();
    const todayMeetings = meetings ? meetings.filter(m => new Date(m.scheduled_time).toDateString() === new Date().toDateString()) : [];
    
    document.getElementById('upcomingMeetings').textContent = todayMeetings.length;
    
    const mList = document.getElementById('meetingsList');
    mList.innerHTML = '';
    
    if (todayMeetings.length > 0) {
      todayMeetings.forEach(m => {
        const time = new Date(m.scheduled_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        const div = document.createElement('div');
        div.style.cssText = "padding: 0.75rem; border-left: 3px solid var(--warning); background: rgba(245, 158, 11, 0.05); margin-bottom: 0.75rem; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;";
        div.innerHTML = `
          <div style="font-size: 0.85rem; color: var(--text-muted);">${time}</div>
          <div style="font-weight: 500; margin-top: 0.25rem;">Checkup Appt (#${m.id})</div>
        `;
        mList.appendChild(div);
      });
    } else {
      mList.innerHTML = '<p class="text-center" style="color:var(--text-muted); font-size:0.9rem; margin-top: 2rem;">No meetings scheduled for today.</p>';
    }

  } catch (err) {
    console.error("Dashboard Load Error:", err);
    ApiClient.notify("Failed to load dashboard data", "error");
  }
});
