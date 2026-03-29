const API_BASE = 'http://localhost:8000';

class ApiClient {
  static getToken() {
    return localStorage.getItem('token');
  }

  static setToken(token) {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }

  static async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    // Remove Content-Type for FormData
    if (options.body instanceof FormData) {
      delete headers['Content-Type'];
    }

    try {
      const response = await fetch(url, { ...options, headers });
      
      if (!response.ok) {
        if (response.status === 401 && endpoint !== '/token') {
          // Auto logout on unauthorized
          this.setToken(null);
          window.location.href = 'index.html';
          return null;
        }

        const errorData = await response.json().catch(() => null);
        throw new Error((errorData && errorData.detail) ? (typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail)) : `API Error: ${response.status}`);
      }

      // Check content type to see how to parse
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.indexOf("application/json") !== -1) {
        return await response.json();
      } else {
        return await response.text();
      }
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  // --- Auth ---
  static async login(username, password) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    params.append('grant_type', 'password');

    const data = await this.request('/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params,
    });
    
    // Assuming FastAPI OAuth2PasswordBearer returns access_token
    if (data && data.access_token) {
      this.setToken(data.access_token);
    }
    return data;
  }

  static async getProfile() {
    return this.request('/profile', { method: 'GET' });
  }

  // --- Patients ---
  static async getPatients() {
    return this.request('/patients/', { method: 'GET' });
  }

  static async getPatient(id) {
    return this.request(`/patients/${id}`, { method: 'GET' });
  }

  static async registerPatient(data) {
    return this.request('/patients/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  static async updatePatient(id, data) {
    return this.request(`/patients/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  static async deletePatient(id) {
    return this.request(`/patients/${id}`, { method: 'DELETE' });
  }

  // --- Caretakers ---
  static async getCaretakers() {
    return this.request('/caretaker/', { method: 'GET' });
  }

  // --- Doctors ---
  static async getDoctors() {
    return this.request('/doctors/', { method: 'GET' });
  }

  // --- Meetings ---
  static async getMeetings() {
    return this.request('/meetings/', { method: 'GET' });
  }

  static async createMeeting(data) {
    return this.request('/meetings/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // --- Links (Caretaker-Patient) ---
  static async getCaretakerLinks() {
    return this.request('/caretaker-patient-links/', { method: 'GET' });
  }

  static async createCaretakerLink(data) {
    return this.request('/caretaker-patient-links/', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // --- Links (Doctor-Patient) ---
  static async getDoctorLinks() {
    return this.request('/doctor-patient-links/', { method: 'GET' });
  }

  static async createDoctorLink(data) {
    return this.request('/doctor-patient-links/', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // --- Locations/Places ---
  static async updateLocation(userId, data) {
    return this.request(`/gmaps/location/update?user_id=${userId}`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  static async getLatestLocation(userId) {
    return this.request(`/gmaps/location/latest/${userId}`, { method: 'GET' });
  }

  static async addPlace(userId, data) {
    return this.request(`/gmaps/places?user_id=${userId}`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  static async getPlaces(userId) {
    return this.request(`/gmaps/places?user_id=${userId}`, { method: 'GET' });
  }

  static async getMemoryTriggers() {
    return this.request('/family/me', { method: 'GET' });
  }

  static logout() {
    this.setToken(null);
    window.location.href = 'index.html';
  }

  // --- Notification System ---
  static notify(message, type = 'success') {
    let container = document.getElementById('notifications');
    if (!container) {
      container = document.createElement('div');
      container.id = 'notifications';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    // Icon
    const icon = type === 'success' ? '✓' : '⚠';
    toast.innerHTML = `<span style="font-weight:bold; font-size:1.2rem;">${icon}</span> <span>${message}</span>`;
    
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'fadeOut 0.3s forwards';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
}

class SidebarManager {
  static async init() {
    const isLoginPage = window.location.pathname.endsWith('index.html') || 
                        window.location.pathname.endsWith('admin_login.html') || 
                        window.location.pathname === '/' || 
                        window.location.pathname === '';
    
    if (isLoginPage) return;

    try {
      const profile = await ApiClient.getProfile();
      if (!profile) return;
      
      window.userRole = profile.role;
      const role = profile.role;

      // Select elements
      const patientsTab = document.querySelector('a[href="patients.html"]');
      const memoryTab = document.querySelector('a[href="memory.html"]');

      if (role === 'patient') {
        // Patients see Memory tab, not Patients tab
        if (patientsTab) patientsTab.style.display = 'none';
        if (memoryTab) memoryTab.style.display = 'flex';
        const faceRecTab = document.querySelector('a[href="face_recognition.html"]');
        if (faceRecTab) faceRecTab.style.display = 'none';
      } else if (role === 'caretaker') {
        // Caregiver/Family: show Face Recognition, hide patient list
        if (patientsTab) patientsTab.style.display = 'none';
        if (memoryTab) memoryTab.style.display = 'none';
        
        let faceRecTab = document.querySelector('a[href="face_recognition.html"]');
        if (!faceRecTab && patientsTab) {
            faceRecTab = document.createElement('a');
            faceRecTab.href = 'face_recognition.html';
            faceRecTab.className = window.location.pathname.includes('face_recognition.html') ? 'menu-item active' : 'menu-item';
            faceRecTab.innerHTML = `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg> Face Recognition`;
            patientsTab.insertAdjacentElement('afterend', faceRecTab);
        } else if (faceRecTab) {
            faceRecTab.style.display = 'flex';
        }
      } else {
        // Doctor / Admin: show Patients tab as-is, hide Face Recognition
        if (patientsTab) patientsTab.style.display = 'flex';
        if (memoryTab) memoryTab.style.display = 'none';
        const faceRecTab = document.querySelector('a[href="face_recognition.html"]');
        if (faceRecTab) faceRecTab.style.display = 'none';
      }

      // Update avatar/name globally if elements exist
      const nameEl = document.getElementById('userName');
      const roleEl = document.getElementById('userRole');
      const initialEl = document.getElementById('userInitial');
      
      if (nameEl) nameEl.textContent = profile.username;
      if (roleEl) roleEl.textContent = role.charAt(0).toUpperCase() + role.slice(1);
      if (initialEl) initialEl.textContent = profile.username.charAt(0).toUpperCase();

      // Handle logout mapping
      const logoutBtns = document.querySelectorAll('.logout-btn, #logoutBtn');
      logoutBtns.forEach(btn => {
          btn.addEventListener('click', (e) => {
              e.preventDefault();
              ApiClient.logout();
          });
      });

    } catch (e) {
      console.error('Sidebar Init Failed:', e);
    }
  }
}

// Check auth and init sidebar
window.addEventListener('DOMContentLoaded', () => {
  const isLoginPage = window.location.pathname.endsWith('index.html') || 
                      window.location.pathname.endsWith('admin_login.html') || 
                      window.location.pathname === '/' || 
                      window.location.pathname === '';
  
  if (!isLoginPage && !ApiClient.getToken()) {
    window.location.href = 'index.html';
  } else if (!isLoginPage) {
    SidebarManager.init();
  }
});
