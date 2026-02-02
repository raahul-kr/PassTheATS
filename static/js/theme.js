/**
 * ═══════════════════════════════════════════════════════════
 * ✨ PassTheATS - Minimal Theme Engine
 * Pure JavaScript. Zero Dependencies. Maximum Impact.
 * ═══════════════════════════════════════════════════════════
 */

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// CONFIG
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

const THEME = {
  key: 'theme',
  light: 'light',
  dark: 'dark',
  icons: {
    light: 'bi-moon-stars-fill',
    dark: 'bi-sun-fill'
  }
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// CORE
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

const getTheme = () => 
  localStorage.getItem(THEME.key) || 
  (matchMedia('(prefers-color-scheme: dark)').matches ? THEME.dark : THEME.light);

const setTheme = (theme) => {
  document.documentElement.setAttribute('data-bs-theme', theme);
  localStorage.setItem(THEME.key, theme);
  updateIcon(theme);
  createRipple(theme);
};

const updateIcon = (theme) => {
  const icon = document.getElementById('theme-icon');
  if (!icon) return;
  
  icon.style.transform = 'scale(0) rotate(180deg)';
  
  setTimeout(() => {
    icon.className = theme === THEME.dark ? THEME.icons.dark : THEME.icons.light;
    icon.style.transform = 'scale(1) rotate(0deg)';
  }, 150);
};

const createRipple = (theme) => {
  const ripple = document.createElement('div');
  Object.assign(ripple.style, {
    position: 'fixed',
    top: '50%',
    left: '50%',
    width: '0',
    height: '0',
    borderRadius: '50%',
    background: theme === THEME.dark ? '#0a0a0a' : '#fafafa',
    transform: 'translate(-50%, -50%)',
    pointerEvents: 'none',
    zIndex: '9999',
    transition: 'all .6s cubic-bezier(.4, 0, .2, 1)',
    opacity: '0'
  });
  
  document.body.appendChild(ripple);
  
  requestAnimationFrame(() => {
    ripple.style.width = ripple.style.height = '200vmax';
    ripple.style.opacity = '.8';
  });
  
  setTimeout(() => ripple.remove(), 600);
};

const toggleTheme = () => {
  const current = document.documentElement.getAttribute('data-bs-theme');
  setTheme(current === THEME.dark ? THEME.light : THEME.dark);
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// OBSERVERS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// Sync across tabs
addEventListener('storage', (e) => {
  if (e.key === THEME.key && e.newValue) {
    document.documentElement.setAttribute('data-bs-theme', e.newValue);
    updateIcon(e.newValue);
  }
});

// OS theme changes
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (!localStorage.getItem(THEME.key)) {
    setTheme(e.matches ? THEME.dark : THEME.light);
  }
});

// Keyboard shortcut (Ctrl/Cmd + Shift + L)
addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'L') {
    e.preventDefault();
    toggleTheme();
  }
});

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// ENHANCEMENTS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// Drag & Drop feedback
const initDragDrop = () => {
  document.querySelectorAll('.upload-area').forEach(area => {
    ['dragenter', 'dragover'].forEach(e => 
      area.addEventListener(e, (ev) => {
        ev.preventDefault();
        area.classList.add('dragover');
      })
    );
    
    ['dragleave', 'drop'].forEach(e => 
      area.addEventListener(e, (ev) => {
        ev.preventDefault();
        area.classList.remove('dragover');
      })
    );
  });
};

// Scroll animations
const initScrollAnimations = () => {
  if (!('IntersectionObserver' in window)) return;
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.cssText = `
          animation: fadeIn .6s ease forwards;
        `;
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  
  document.querySelectorAll('.glass-card, .report-card, .fade-in').forEach(el => 
    observer.observe(el)
  );
};

// Smooth scroll
const initSmoothScroll = () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      e.preventDefault();
      const target = document.querySelector(href);
      target?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
};

// Lazy load images
const initLazyLoad = () => {
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('img[data-src]').forEach(img => {
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
    });
    return;
  }
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        observer.unobserve(img);
      }
    });
  });
  
  document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
};

// Cursor glow effect (desktop only)
const initCursorGlow = () => {
  if (matchMedia('(pointer: fine)').matches) {
    const glow = document.createElement('div');
    Object.assign(glow.style, {
      position: 'fixed',
      width: '300px',
      height: '300px',
      background: 'radial-gradient(circle, rgba(59, 130, 246, .08), transparent 70%)',
      pointerEvents: 'none',
      zIndex: '9998',
      transition: 'opacity .3s',
      opacity: '0'
    });
    document.body.appendChild(glow);
    
    addEventListener('mousemove', (e) => {
      glow.style.left = `${e.clientX - 150}px`;
      glow.style.top = `${e.clientY - 150}px`;
      glow.style.opacity = '1';
    });
    
    addEventListener('mouseleave', () => glow.style.opacity = '0');
  }
};

// Form validation feedback
const initFormFeedback = () => {
  document.querySelectorAll('.form-control, .form-select').forEach(input => {
    input.addEventListener('invalid', (e) => {
      e.preventDefault();
      input.style.borderColor = 'var(--danger)';
      input.style.boxShadow = '0 0 0 4px rgba(239, 68, 68, .15)';
    });
    
    input.addEventListener('input', () => {
      if (input.validity.valid) {
        input.style.borderColor = '';
        input.style.boxShadow = '';
      }
    });
  });
};

// Card hover sound (subtle)
const initCardSounds = () => {
  if (!('AudioContext' in window)) return;
  
  const playTick = () => {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    
    osc.connect(gain);
    gain.connect(ctx.destination);
    
    osc.frequency.value = 800;
    gain.gain.value = 0.01;
    
    osc.start();
    gain.gain.exponentialRampToValueAtTime(0.00001, ctx.currentTime + 0.03);
    osc.stop(ctx.currentTime + 0.03);
  };
  
  document.querySelectorAll('.report-card, .dashboard-card').forEach(card => {
    card.addEventListener('mouseenter', playTick, { passive: true });
  });
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// INIT
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

const init = () => {
  setTheme(getTheme());
  
  initDragDrop();
  initScrollAnimations();
  initSmoothScroll();
  initLazyLoad();
  initCursorGlow();
  initFormFeedback();
  initCardSounds();
  
  // Add theme toggle to buttons
  document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
    btn.addEventListener('click', toggleTheme);
  });
  
  // Respect reduced motion
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.style.setProperty('--transition', '0ms');
  }
  
  console.log('%c✨ PassTheATS', 'color: #3b82f6; font-size: 16px; font-weight: bold;');
};

// Run when ready
if (document.readyState === 'loading') {
  addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// GLOBAL API
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

window.PassTheATS = {
  theme: {
    get: () => document.documentElement.getAttribute('data-bs-theme'),
    set: setTheme,
    toggle: toggleTheme,
    reset: () => {
      localStorage.removeItem(THEME.key);
      setTheme(getTheme());
    }
  }
};