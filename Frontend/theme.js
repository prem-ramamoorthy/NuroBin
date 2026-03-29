// ============================================================
// NeuroBin – Global Dark Mode Toggle
// This script self-injects a toggle button into every page.
// It persists the user's preference via localStorage.
// ============================================================

(function () {
  // 1. Apply saved theme IMMEDIATELY to avoid flash
  //    Default to 'dark' if no preference saved yet
  const saved = localStorage.getItem('neurobin-theme');
  if (saved !== 'light') {
    document.documentElement.classList.add('dark-theme');
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Also set on body for CSS selectors that use body.dark-theme
    if (localStorage.getItem('neurobin-theme') !== 'light') {
      document.body.classList.add('dark-theme');
    }

    // 2. Create the toggle button dynamically
    //    Remove any existing one first (from HTML) to avoid duplicates
    const existing = document.getElementById('themeToggleBtn');
    if (existing) existing.remove();

    const btn = document.createElement('button');
    btn.id = 'themeToggleBtn';
    btn.title = 'Toggle Dark Mode';
    btn.setAttribute('aria-label', 'Toggle Dark Mode');
    Object.assign(btn.style, {
      position: 'fixed',
      top: '1rem',
      right: '1rem',
      background: 'var(--surface)',
      border: '1px solid var(--surface-border)',
      borderRadius: '50%',
      width: '44px',
      height: '44px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      color: 'var(--text-main)',
      backdropFilter: 'blur(12px)',
      WebkitBackdropFilter: 'blur(12px)',
      zIndex: '99999',
      boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)',
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      padding: '0',
    });

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('stroke', 'currentColor');
    svg.style.width = '20px';
    svg.style.height = '20px';
    svg.id = 'themeIcon';
    btn.appendChild(svg);

    document.body.appendChild(btn);

    // 3. Set initial icon
    setIcon();

    // 4. Toggle handler
    btn.addEventListener('click', () => {
      const isDark = document.body.classList.toggle('dark-theme');
      document.documentElement.classList.toggle('dark-theme', isDark);
      localStorage.setItem('neurobin-theme', isDark ? 'dark' : 'light');
      setIcon();
    });

    // Hover effect
    btn.addEventListener('mouseenter', () => {
      btn.style.transform = 'scale(1.1)';
      btn.style.boxShadow = '0 6px 20px rgba(79,70,229,0.3)';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'scale(1)';
      btn.style.boxShadow = '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)';
    });
  });

  function setIcon() {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    const isDark = document.body.classList.contains('dark-theme');
    if (isDark) {
      // Sun icon → click to go light
      icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />';
    } else {
      // Moon icon → click to go dark
      icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />';
    }
  }
})();
