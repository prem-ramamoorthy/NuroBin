document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  const btn = document.getElementById('loginBtn');
  const tabs = document.querySelectorAll('.tab');

  // If already logged in, redirect to dashboard
  if (ApiClient.getToken()) {
    window.location.href = 'dashboard.html';
  }

  // Handle visual tab switching
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      // Update demo credentials based on tab if needed
      const role = tab.getAttribute('data-role');
      const demoBox = document.getElementById('demoCredsBox');
      const demoEmail = document.getElementById('demoEmail');
      const demoPass = document.getElementById('demoPass');

      if (role === 'family') {
        demoEmail.textContent = 'caregiver@neurobin.com';
        demoPass.textContent = 'neurobin123';
        demoBox.style.display = 'block';
      } else if (role === 'doctor') {
        demoEmail.textContent = 'doctor@neurobin.com';
        demoPass.textContent = 'neurobin123';
        demoBox.style.display = 'block';
      } else {
        demoBox.style.display = 'none';
      }
    });
  });

  // Password Toggle Logic
  const passwordInput = document.getElementById('password');
  const passwordToggle = document.getElementById('passwordToggle');
  const eyeIcon = document.getElementById('eyeIcon');

  if (passwordToggle && passwordInput && eyeIcon) {
    passwordToggle.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const isPassword = passwordInput.getAttribute('type') === 'password';
      passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
      
      // Toggle Eye Icon SVG
      if (isPassword) {
        eyeIcon.innerHTML = `
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7 1.274-4.057 5.064-7 9.542-7 1.225 0 2.39.221 3.468.625m4.468 4.468a10.05 10.05 0 011.542 3.468M9 9l6 6m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3l18 18" />
        `;
      } else {
        eyeIcon.innerHTML = `
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        `;
      }
    });
  }

  // Demo Credentials Auto-fill
  const demoBox = document.getElementById('demoCredsBox');
  if (demoBox) {
    demoBox.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      const email = document.getElementById('demoEmail')?.textContent;
      const pass = document.getElementById('demoPass')?.textContent;
      
      if (email && pass) {
        document.getElementById('username').value = email;
        document.getElementById('password').value = pass;
        if (typeof ApiClient !== 'undefined' && ApiClient.notify) {
          ApiClient.notify('Credentials auto-filled', 'success');
        }
      }
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
      btn.disabled = true;
      btn.innerHTML = `
        <svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24" style="animation: spin 1s linear infinite; width:20px; height:20px;">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg> Authenticating...`;

      await ApiClient.login(username, password);
      
      ApiClient.notify('Login successful! Redirecting...', 'success');
      setTimeout(() => {
        window.location.href = 'dashboard.html';
      }, 1000);

    } catch (error) {
      ApiClient.notify(error.message || 'Login failed. Please check credentials.', 'error');
      btn.disabled = false;
      btn.innerHTML = 'Secure Login';
    }
  });
});

// Add spin keyframes to head for loading icon
const style = document.createElement('style');
style.innerHTML = `
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);
