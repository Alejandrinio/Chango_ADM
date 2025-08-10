// Sistema de Autenticación Unificado
class AuthManager {
    constructor() {
        this.checkAuth();
    }

    checkAuth() {
        const userData = localStorage.getItem('user_data');
        if (!userData) {
            // No hay sesión activa, redirigir al login
            window.location.href = 'login.html';
            return;
        }

        const user = JSON.parse(userData);
        this.currentUser = user;

        // Verificar que el usuario tenga acceso a la página actual
        this.checkPageAccess();
    }

    checkPageAccess() {
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        
        // Definir qué páginas puede acceder cada rol
        const adminPages = ['index.html', 'empleados.html', 'fichajes.html', 'recibos.html'];
        const empleadoPages = ['empleado-portal.html'];

        if (this.currentUser.role === 'admin') {
            // Administradores pueden acceder a todas las páginas excepto el portal de empleados
            if (empleadoPages.includes(currentPage)) {
                alert('Acceso denegado. Solo empleados pueden acceder a esta página.');
                window.location.href = 'index.html';
            }
        } else if (this.currentUser.role === 'empleado') {
            // Empleados solo pueden acceder al portal de empleados
            if (!empleadoPages.includes(currentPage)) {
                alert('Acceso denegado. Solo administradores pueden acceder a esta página.');
                window.location.href = 'empleado-portal.html';
            }
        }
    }

    logout() {
        localStorage.removeItem('user_data');
        localStorage.removeItem('unified_remembered');
        window.location.href = 'login.html';
    }

    getCurrentUser() {
        return this.currentUser;
    }

    isAdmin() {
        return this.currentUser && this.currentUser.role === 'admin';
    }

    isEmpleado() {
        return this.currentUser && this.currentUser.role === 'empleado';
    }

    // Actualizar la información del usuario en la UI
    updateUserInfo() {
        if (this.currentUser) {
            // Actualizar nombre en el navbar si existe
            const userNameElement = document.querySelector('.user-name');
            if (userNameElement) {
                userNameElement.textContent = `${this.currentUser.nombre} ${this.currentUser.apellido}`;
            }

            // Actualizar rol en el navbar si existe
            const userRoleElement = document.querySelector('.user-role');
            if (userRoleElement) {
                userRoleElement.textContent = this.currentUser.rol;
            }
        }
    }
}

// Inicializar el sistema de autenticación
let authManager;
document.addEventListener('DOMContentLoaded', function() {
    authManager = new AuthManager();
    
    // Actualizar información del usuario en la UI
    if (authManager) {
        authManager.updateUserInfo();
    }
});

// Función global para logout
function logout() {
    if (authManager) {
        authManager.logout();
    }
}
