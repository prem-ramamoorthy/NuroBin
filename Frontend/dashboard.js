document.addEventListener('DOMContentLoaded', async () => {
  // Set date
  document.getElementById('currDate').textContent = new Date().toLocaleDateString('en-US', { 
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
  });

  // Check auth and init sidebar are handled by api.js SidebarManager

  try {
    // 1. Fetch Location Data
    const params = new URLSearchParams(window.location.search);
    const userId = params.get('user_id') || 1; // Default to 1 for demo purposes
    
    try {
        const locations = await ApiClient.request(`/gmaps/location/latest/${userId}`);
        if (locations && locations.lat && locations.lng) {
            document.getElementById('lastGps').textContent = `${locations.lat.toFixed(2)}, ${locations.lng.toFixed(2)}`;
            document.getElementById('lastGps').nextElementSibling.textContent = 'Live tracking';
        }
    } catch {
        // Fallback mock if endpoint isn't fully ready
        document.getElementById('lastGps').textContent = 'Home';
    }

    // 2. Mock missing endpoints for ui.json aesthetics
    // Mood & Adherence
    document.getElementById('medAdherence').textContent = '96%';
    document.getElementById('todayMood').textContent = 'Calm / Joyful';
    
    // Memory Triggers - fetch from DB in future, mock for now
    const trigs = document.getElementById('memoryTriggersList');
    if (trigs) {
        // Just keeping the HTML structure intact as a perfect placeholder
    }

    // Alerts - could pull from Meetings or a dedicated Alert DB
    const alerts = document.getElementById('alertsList');
    if (alerts && alerts.children.length > 0) {
        // Placeholder intact
    }
  } catch (err) {
    console.error("Dashboard Load Error:", err);
    ApiClient.notify("Failed to load some dashboard data", "error");
  }
});
