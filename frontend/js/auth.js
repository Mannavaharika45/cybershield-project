/**
 * CyberShield Authentication Library
 * Handles signup, login, logout, token management, and route guarding.
 * Requires the API to be running at API_BASE_URL.
 */

const _AUTH_API_URL = 'https://cybershield-project-7e4c.onrender.com';
const TOKEN_KEY = 'cybershield_token';
const USER_KEY = 'cybershield_user';
/** Retrieve the stored JWT token from localStorage. */
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

/** Retrieve the stored user object from localStorage. */
function getUser() {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
}

/** Return Authorization headers for protected API calls. */
function authHeaders() {
    const token = getToken();
    return {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
}

/** Check if user is currently logged in. */
function isLoggedIn() {
    return !!getToken();
}

/**
 * Guard a protected page. Redirects to login.html if not authenticated.
 * Call this at the top of every protected page's script.
 */
function guardPage() {
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
    } else {
        renderUserAvatar();
    }
}

/**
 * Inject the logged-in user's name and a logout option into the navbar.
 * Replaces the existing static "Login / Demo" button.
 */
function renderUserAvatar() {
    const user = getUser();
    if (!user) return;

    // Find the login button in the navbar and replace it
    const loginBtn = document.getElementById('loginNavBtn');
    if (loginBtn) {
        const initials = user.full_name
            .split(' ')
            .map(n => n[0])
            .join('')
            .toUpperCase()
            .slice(0, 2);

        loginBtn.outerHTML = `
            <div class="flex items-center space-x-3" id="userMenuWrapper">
                <!-- User avatar & dropdown -->
                <div class="relative" id="userAvatarWrapper">
                    <button id="userAvatarBtn" class="flex items-center space-x-2 glass-card px-3 py-2 rounded-lg border border-accent/20 hover:border-accent/60 transition-all">
                        <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-cyan-400 flex items-center justify-center text-xs font-bold text-white">
                            ${initials}
                        </div>
                        <span class="text-sm font-medium text-primary hidden md:block">${user.full_name.split(' ')[0]}</span>
                        <i class="fa-solid fa-chevron-down text-xs text-secondary"></i>
                    </button>
                    <!-- Dropdown -->
                    <div id="userDropdown" class="absolute right-0 top-12 w-52 glass-panel rounded-xl shadow-2xl overflow-hidden hidden z-50 border border-accent/10">
                        <div class="px-4 py-3 border-b border-accent/10">
                            <p class="text-sm font-semibold text-primary truncate">${user.full_name}</p>
                            <p class="text-xs text-secondary truncate">${user.email}</p>
                        </div>
                        <button onclick="logout()" class="w-full text-left px-4 py-3 text-sm text-danger hover:bg-red-500/10 transition flex items-center space-x-2">
                            <i class="fa-solid fa-right-from-bracket"></i>
                            <span>Logout</span>
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Toggle dropdown on click
        setTimeout(() => {
            const btn = document.getElementById('userAvatarBtn');
            const dropdown = document.getElementById('userDropdown');
            if (btn && dropdown) {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    dropdown.classList.toggle('hidden');
                });
                document.addEventListener('click', () => dropdown.classList.add('hidden'));
            }
        }, 0);
    }
}

/**
 * Render a simple "Login" button in the navbar for public pages.
 * Call this on index.html and tips.html.
 */
function renderPublicNavbar() {
    if (isLoggedIn()) {
        renderUserAvatar();
        return;
    }
    // Already has the login button from HTML, nothing to do
}

/** Signup a new user. */
async function signup(fullName, email, password) {
    const res = await fetch(`${_AUTH_API_URL}/api/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name: fullName, email: email, password: password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Signup failed.');
    _saveSession(data);
    return data;
}

/** Login an existing user. */
async function login(email, password) {
    console.log("LOGIN CLICKED");
    const res = await fetch(`${_AUTH_API_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed.');
    _saveSession(data);
    return data;
}

/** Logout — clear session and redirect to home. */
function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    window.location.href = 'index.html';
}

/** Internal: save token and user to localStorage. */
function _saveSession(data) {
    localStorage.setItem(TOKEN_KEY, data.access_token);
    localStorage.setItem(USER_KEY, JSON.stringify(data.user));
}
