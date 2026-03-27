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

// Check auth on non-login pages
window.addEventListener('DOMContentLoaded', () => {
  const isLoginPage = window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname === '';
  if (!isLoginPage && !ApiClient.getToken()) {
    window.location.href = 'index.html';
  }
});
