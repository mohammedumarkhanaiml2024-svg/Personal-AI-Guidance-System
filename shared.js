// Personal AI Guidance System - Shared JavaScript Functions

class AIGuidanceApp {
    constructor() {
        this.API_URL = window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : window.location.protocol + '//' + window.location.hostname.replace('-8080', '-8000');
        
        this.token = null;
        this.isAuthenticated = false;
        this.currentUser = null;
        this.charts = {};
        
        this.init();
    }

    init() {
        console.log('AI Guidance System initialized. API URL:', this.API_URL);
        this.checkAuth();
        this.createFloatingParticles();
    }

    // Authentication Methods
    checkAuth() {
        const savedToken = localStorage.getItem('ai_guidance_token');
        const savedUsername = localStorage.getItem('ai_guidance_username');
        
        if (savedToken && savedUsername) {
            this.token = savedToken;
            this.currentUser = savedUsername;
            this.isAuthenticated = true;
            return true;
        }
        return false;
    }

    async login(username, password) {
        try {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);
            
            const response = await fetch(`${this.API_URL}/token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });
            
            if (response.ok) {
                const data = await response.json();
                this.token = data.access_token;
                this.currentUser = username;
                this.isAuthenticated = true;
                
                localStorage.setItem('ai_guidance_token', data.access_token);
                localStorage.setItem('ai_guidance_username', username);
                
                return { success: true, message: 'Login successful!' };
            } else {
                const error = await response.json();
                return { success: false, message: error.detail };
            }
        } catch (error) {
            return { success: false, message: `Error: ${error.message}` };
        }
    }

    async register(username, password) {
        try {
            const response = await fetch(`${this.API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            if (response.ok) {
                return { success: true, message: 'Registration successful! Please login.' };
            } else {
                const error = await response.json();
                return { success: false, message: error.detail };
            }
        } catch (error) {
            return { success: false, message: `Error: ${error.message}` };
        }
    }

    logout() {
        this.token = null;
        this.currentUser = null;
        this.isAuthenticated = false;
        
        localStorage.removeItem('ai_guidance_token');
        localStorage.removeItem('ai_guidance_username');
        
        window.location.href = '/';
    }

    // Data Fetching Methods
    async fetchData(endpoint, method = 'GET', body = null) {
        const options = {
            method,
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            }
        };
        
        if (body) {
            options.body = JSON.stringify(body);
        }
        
        const response = await fetch(`${this.API_URL}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }
        
        return response.json();
    }

    // Chart Helper Methods
    async loadChartData() {
        try {
            const [habits, productivity, mood] = await Promise.all([
                this.fetchData('/habits?limit=30'),
                this.fetchData('/productivity?limit=30'),
                this.fetchData('/mood?limit=30')
            ]);
            
            return { habits, productivity, mood };
        } catch (error) {
            console.error('Error loading chart data:', error);
            return { habits: [], productivity: [], mood: [] };
        }
    }

    setupChartDefaults() {
        if (typeof Chart !== 'undefined') {
            Chart.defaults.color = '#9ca3af';
            Chart.defaults.borderColor = 'rgba(139, 92, 246, 0.2)';
        }
    }

    // UI Helper Methods
    showLoading(element, message = 'Loading...') {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        
        element.innerHTML = `
            <div class="flex items-center justify-center py-12">
                <div class="spinner mr-4"></div>
                <span class="text-gray-400">${message}</span>
            </div>
        `;
    }

    showError(element, message) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        
        element.innerHTML = `
            <div class="text-center py-12">
                <div class="text-6xl mb-4">⚠️</div>
                <p class="text-red-400 text-lg">${message}</p>
            </div>
        `;
    }

    createFloatingParticles() {
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'floating-particles';
        document.body.appendChild(particlesContainer);

        for (let i = 0; i < 15; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + 'vw';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
            particlesContainer.appendChild(particle);
        }
    }

    // Navigation Helper
    navigateTo(page) {
        window.location.href = `/${page}.html`;
    }

    // Format Helper Methods
    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString();
    }

    formatNumber(num, decimals = 1) {
        return Number(num).toFixed(decimals);
    }

    // Statistics Calculation
    calculateAverage(array, field) {
        if (!array || array.length === 0) return 0;
        const sum = array.reduce((acc, item) => acc + (item[field] || 0), 0);
        return sum / array.length;
    }

    calculateTotal(array, field) {
        if (!array || array.length === 0) return 0;
        return array.reduce((acc, item) => acc + (item[field] || 0), 0);
    }

    // Theme and Animation Helpers
    addHoverEffect(element) {
        element.addEventListener('mouseenter', () => {
            element.style.transform = 'translateY(-5px)';
            element.style.transition = 'transform 0.3s ease';
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.transform = 'translateY(0)';
        });
    }

    // Notification System
    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-xl font-semibold z-50 transition-all transform translate-x-full`;
        
        if (type === 'success') {
            notification.className += ' bg-green-900/90 text-green-400 border border-green-500';
        } else if (type === 'error') {
            notification.className += ' bg-red-900/90 text-red-400 border border-red-500';
        } else {
            notification.className += ' bg-blue-900/90 text-blue-400 border border-blue-500';
        }
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Global instance
window.aiApp = new AIGuidanceApp();

// Common navigation function
function createNavigation(currentPage = '') {
    return `
        <nav class="glow-card rounded-3xl p-2 mb-6">
            <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
                <a href="/" class="nav-tab ${currentPage === 'overview' ? 'active' : ''} py-4 px-6 rounded-2xl font-bold text-center transition-all transform hover:scale-105">
                    📊 Overview
                </a>
                <a href="/track.html" class="nav-tab ${currentPage === 'track' ? 'active' : ''} py-4 px-6 rounded-2xl font-bold text-center transition-all transform hover:scale-105">
                    📝 Track
                </a>
                <a href="/analytics.html" class="nav-tab ${currentPage === 'analytics' ? 'active' : ''} py-4 px-6 rounded-2xl font-bold text-center transition-all transform hover:scale-105">
                    📈 Analytics
                </a>
                <a href="/brain.html" class="nav-tab ${currentPage === 'brain' ? 'active' : ''} py-4 px-6 rounded-2xl font-bold text-center transition-all transform hover:scale-105">
                    🧠 AI Brain
                </a>
                <a href="/chat.html" class="nav-tab ${currentPage === 'chat' ? 'active' : ''} py-4 px-6 rounded-2xl font-bold text-center transition-all transform hover:scale-105">
                    💬 Chat
                </a>
            </div>
        </nav>
    `;
}

// Common header function
function createHeader(username) {
    return `
        <div class="glow-card rounded-3xl p-6 mb-6">
            <div class="flex flex-col md:flex-row items-center justify-between gap-4">
                <div>
                    <h2 class="text-4xl font-black gradient-text mb-2">
                        Welcome, ${username}! 👋
                    </h2>
                    <p class="text-gray-400">Your personalized AI-powered dashboard</p>
                </div>
                <button 
                    onclick="aiApp.logout()"
                    class="px-8 py-3 bg-red-600 hover:bg-red-700 text-white rounded-xl font-bold transform hover:scale-105 transition-all shadow-lg shadow-red-500/50"
                >
                    🚪 Logout
                </button>
            </div>
        </div>
    `;
}

// Authentication check for protected pages
function requireAuth() {
    if (!aiApp.checkAuth()) {
        window.location.href = '/';
        return false;
    }
    return true;
}