/**
 * PassTheATS Theme Engine
 * Features: LocalStorage Persistence, System Preference Detection,
 * Multi-tab Synchronization, and Live OS Theme Listening.
 */

// 1. Determine the best theme to load
const getPreferredTheme = () => {
    const storedTheme = localStorage.getItem('theme')
    if (storedTheme) {
        return storedTheme
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

// 2. Apply the theme to the DOM
const setTheme = function (theme) {
    document.documentElement.setAttribute('data-bs-theme', theme)
    
    // Update Icon
    const icon = document.getElementById('theme-icon');
    if(icon) {
        if (theme === 'dark') {
            icon.classList.remove('bi-moon-stars-fill');
            icon.classList.add('bi-sun-fill');
        } else {
            icon.classList.remove('bi-sun-fill');
            icon.classList.add('bi-moon-stars-fill');
        }
    }
}

// 3. Initialize immediately
setTheme(getPreferredTheme())

// 4. Toggle Function (Attached to Button)
const toggleTheme = () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme')
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark'
    
    localStorage.setItem('theme', newTheme)
    setTheme(newTheme)
}

// ---------------------------------------------------------
// ULTRA ENHANCEMENTS (New)
// ---------------------------------------------------------

// A. Listen for OS Theme Changes (e.g., Mac going Day -> Night)
// Only works if the user hasn't manually set a preference yet
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (!localStorage.getItem('theme')) {
        setTheme(getPreferredTheme())
    }
})

// B. Sync Across Multiple Tabs
// If user toggles theme in Tab A, Tab B updates instantly without reload
window.addEventListener('storage', (event) => {
    if (event.key === 'theme') {
        setTheme(event.newValue)
    }
})