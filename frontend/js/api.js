// API Configuration
const API_BASE_URL = 'http://lvh.me:8001'; // data-api (Docker)
const CHAT_API_BASE_URL = 'http://lvh.me:8002'; // chatbot-api (Docker)

// API Service Class
class ApiService {
    constructor() {
        this.baseUrl = API_BASE_URL;
    }

    // Generic fetch method
    async fetchApi(endpoint, options = {}) {
        try {
            const url = `${this.baseUrl}${endpoint}`;
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Get employees with pagination (maps page/limit -> skip/limit)
    async getEmpleados(page = 1, limit = 10, search = null) {
        const skip = Math.max(0, (page - 1) * limit);
        let endpoint = `/empleados?skip=${skip}&limit=${limit}`;
        // Backend actual no soporta 'search' genérico; se puede mapear a filtros si aplica
        return await this.fetchApi(endpoint);
    }

    // Get employee by ID
    async getEmpleado(id) {
        return await this.fetchApi(`/empleados/${id}`);
    }

    // Get statistics (usa endpoint del data-api)
    async getStats() {
        return await this.fetchApi('/stats/empleados');
    }

    // Health check
    async healthCheck() {
        return await this.fetchApi('/health');
    }
}

// Chat Service for chatbot-api
class ChatService {
    constructor() {
        this.baseUrl = CHAT_API_BASE_URL;
        try {
            const saved = localStorage.getItem('chatSessionId');
            this.sessionId = saved || `web_${Date.now()}`;
            if (!saved) localStorage.setItem('chatSessionId', this.sessionId);
        } catch (e) {
            this.sessionId = `web_${Date.now()}`;
        }
    }

    async sendMessage(message, sessionId = null, context = null) {
        const effectiveSession = sessionId || this.sessionId;
        const body = JSON.stringify({ message, session_id: effectiveSession, context });
        const resp = await fetch(`${this.baseUrl}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body
        });
        if (!resp.ok) {
            throw new Error(`Chat API error: ${resp.status}`);
        }
        return await resp.json();
    }

    async health() {
        const resp = await fetch(`${this.baseUrl}/health`);
        return await resp.json();
    }
}

// Global API instances
const api = new ApiService();
const chatApi = new ChatService();

// Utility functions for UI
class EmpleadosUI {
    constructor() {
        this.api = api;
        this.currentPage = 1;
        this.currentLimit = 10;
        this.currentSearch = '';
    }

    // Load employees table
    async loadEmpleadosTable() {
        try {
            const result = await this.api.getEmpleados(this.currentPage, this.currentLimit, this.currentSearch);
            // Backend retorna lista o { empleados: [...] }
            const empleados = Array.isArray(result) ? result : (result.empleados || result.data || []);
            this.renderEmpleadosTable(empleados);
            // Render paginación básica
            const total = (result.pagination && result.pagination.total) || result.total || empleados.length || (this.currentPage * this.currentLimit);
            const pages = Math.ceil(total / this.currentLimit) || this.currentPage;
            this.renderPagination({ page: this.currentPage, pages, limit: this.currentLimit, total });
        } catch (error) {
            this.showError('Error de conexión: ' + error.message);
        }
    }

    // Render employees table
    renderEmpleadosTable(empleados) {
        const tableBody = document.getElementById('empleados-table-body');
        if (!tableBody) return;

        tableBody.innerHTML = '';

        empleados.forEach(empleado => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${empleado.id ?? ''}</td>
                <td>${(empleado.nombre || '')} ${(empleado.apellido || '')}</td>
                <td>${empleado.rol ?? '-'}</td>
                <td>${empleado.horario_laboral ?? '-'}</td>
                <td>
                    <span class="badge badge-${this.getEstadoBadgeClass((empleado.estado || 'activo').toString().toLowerCase())}">
                        ${empleado.estado || 'ACTIVO'}
                    </span>
                </td>
                <td>${empleado.email || '-'}</td>
                <td>${empleado.telefono || '-'}</td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="empleadosUI.viewEmpleado(${empleado.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-warning" onclick="empleadosUI.editEmpleado(${empleado.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    // Get badge class for status
    getEstadoBadgeClass(estado) {
        switch (estado) {
            case 'activo': return 'success';
            case 'inactivo': return 'danger';
            case 'vacaciones': return 'warning';
            default: return 'secondary';
        }
    }

    // Render pagination
    renderPagination(pagination) {
        const paginationContainer = document.getElementById('pagination-container');
        if (!paginationContainer) return;

        let paginationHTML = `
            <nav aria-label="Paginación de empleados">
                <ul class="pagination justify-content-center">
        `;

        // Previous button
        if (pagination.page > 1) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="empleadosUI.changePage(${pagination.page - 1})">
                        Anterior
                    </a>
                </li>
            `;
        }

        // Page numbers
        for (let i = 1; i <= pagination.pages; i++) {
            if (i === pagination.page) {
                paginationHTML += `
                    <li class="page-item active">
                        <span class="page-link">${i}</span>
                    </li>
                `;
            } else {
                paginationHTML += `
                    <li class="page-item">
                        <a class="page-link" href="#" onclick="empleadosUI.changePage(${i})">${i}</a>
                    </li>
                `;
            }
        }

        // Next button
        if (pagination.page < pagination.pages) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="empleadosUI.changePage(${pagination.page + 1})">
                        Siguiente
                    </a>
                </li>
            `;
        }

        paginationHTML += `
                </ul>
            </nav>
            <div class="text-center mt-2">
                <small class="text-muted">
                    Página ${pagination.page} • ${pagination.limit} por página
                </small>
            </div>
        `;

        paginationContainer.innerHTML = paginationHTML;
    }

    // Change page
    async changePage(page) {
        this.currentPage = page;
        await this.loadEmpleadosTable();
    }

    // Search employees
    async searchEmpleados(searchTerm) {
        this.currentSearch = searchTerm;
        this.currentPage = 1; // Reset to first page
        await this.loadEmpleadosTable();
    }

    // View employee details
    async viewEmpleado(id) {
        try {
            const result = await this.api.getEmpleado(id);
            const empleado = result && !Array.isArray(result) && result.id ? result : (result.data || result);
            if (empleado) {
                this.showEmpleadoModal(empleado, 'view');
            } else {
                this.showError('Empleado no encontrado');
            }
        } catch (error) {
            this.showError('Error de conexión: ' + error.message);
        }
    }

    // Edit employee
    async editEmpleado(id) {
        try {
            const result = await this.api.getEmpleado(id);
            const empleado = result && !Array.isArray(result) && result.id ? result : (result.data || result);
            if (empleado) {
                this.showEmpleadoModal(empleado, 'edit');
            } else {
                this.showError('Empleado no encontrado');
            }
        } catch (error) {
            this.showError('Error de conexión: ' + error.message);
        }
    }

    // Show employee modal
    showEmpleadoModal(empleado, mode) {
        const modal = document.getElementById('empleadoModal');
        if (!modal) return;

        const modalTitle = modal.querySelector('.modal-title');
        const modalBody = modal.querySelector('.modal-body');

        modalTitle.textContent = mode === 'view' ? 'Ver Empleado' : 'Editar Empleado';

        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <p><strong>ID:</strong> ${empleado.id ?? ''}</p>
                    <p><strong>Nombre:</strong> ${empleado.nombre ?? ''}</p>
                    <p><strong>Apellido:</strong> ${empleado.apellido ?? ''}</p>
                    <p><strong>Estado:</strong> 
                        <span class="badge badge-${this.getEstadoBadgeClass((empleado.estado || 'activo').toString().toLowerCase())}">
                            ${empleado.estado || 'ACTIVO'}
                        </span>
                    </p>
                </div>
                <div class="col-md-6">
                    <p><strong>Email:</strong> ${empleado.email || '-'}</p>
                    <p><strong>Teléfono:</strong> ${empleado.telefono || '-'}</p>
                    <p><strong>Fecha de ingreso:</strong> ${empleado.fecha_ingreso || '-'}</p>
                </div>
            </div>
        `;

        // Show modal
        $(modal).modal('show');
    }

    // Load dashboard statistics
    async loadStats() {
        try {
            const result = await this.api.getStats();
            // Adaptar a forma del backend
            if (result && typeof result === 'object') {
                this.renderStats(result);
            }
        } catch (error) {
            this.showError('Error de conexión: ' + error.message);
        }
    }

    // Render statistics (adaptado a /stats/empleados del data-api)
    renderStats(stats) {
        const totalElement = document.getElementById('total-empleados');
        const activosElement = document.getElementById('empleados-activos');
        const inactivosElement = document.getElementById('empleados-inactivos');
        const vacacionesElement = document.getElementById('empleados-vacaciones');

        if (totalElement && typeof stats.total_empleados !== 'undefined') totalElement.textContent = stats.total_empleados;
        // Si hay desglose por estado, intentar asignar
        if (Array.isArray(stats.por_estado)) {
            const map = Object.fromEntries(stats.por_estado.map(e => [String(e.estado || e.ESTADO || '').toLowerCase(), e.cantidad || e.CANTIDAD || 0]));
            if (activosElement && typeof map['activo'] !== 'undefined') activosElement.textContent = map['activo'];
            if (inactivosElement && typeof map['inactivo'] !== 'undefined') inactivosElement.textContent = map['inactivo'];
            if (vacacionesElement && typeof map['vacaciones'] !== 'undefined') vacacionesElement.textContent = map['vacaciones'];
        }
    }

    // Show error message
    showError(message) {
        console.error(message);
        alert(message); // Simple alert for now
    }

    // Initialize the UI
    init() {
        this.loadEmpleadosTable();
        this.loadStats();

        const searchInput = document.getElementById('search-empleados');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => {
                    this.searchEmpleados(e.target.value);
                }, 500);
            });
        }
    }
}

// Global UI instance
const empleadosUI = new EmpleadosUI();

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    empleadosUI.init();
});
