// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

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

    // Get employees with pagination and search
    async getEmpleados(page = 1, limit = 10, search = null) {
        let endpoint = `/empleados?page=${page}&limit=${limit}`;
        if (search) {
            endpoint += `&search=${encodeURIComponent(search)}`;
        }
        return await this.fetchApi(endpoint);
    }

    // Get employee by ID
    async getEmpleado(id) {
        return await this.fetchApi(`/empleados/${id}`);
    }

    // Get statistics
    async getStats() {
        return await this.fetchApi('/stats');
    }

    // Health check
    async healthCheck() {
        return await this.fetchApi('/health');
    }
}

// Global API instance
const api = new ApiService();

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
            
            if (result.success) {
                this.renderEmpleadosTable(result.data);
                this.renderPagination(result.pagination);
            } else {
                this.showError('Error al cargar empleados: ' + result.error);
            }
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
                <td>${empleado.id}</td>
                <td>${empleado.nombre} ${empleado.apellido}</td>
                <td>${empleado.rol}</td>
                <td>${empleado.horario_laboral}</td>
                <td>
                    <span class="badge badge-${this.getEstadoBadgeClass(empleado.estado)}">
                        ${empleado.estado}
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
                    Mostrando ${((pagination.page - 1) * pagination.limit) + 1} a 
                    ${Math.min(pagination.page * pagination.limit, pagination.total)} 
                    de ${pagination.total} empleados
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
            if (result.success) {
                this.showEmpleadoModal(result.data, 'view');
            } else {
                this.showError('Error al cargar empleado: ' + result.error);
            }
        } catch (error) {
            this.showError('Error de conexión: ' + error.message);
        }
    }

    // Edit employee
    async editEmpleado(id) {
        try {
            const result = await this.api.getEmpleado(id);
            if (result.success) {
                this.showEmpleadoModal(result.data, 'edit');
            } else {
                this.showError('Error al cargar empleado: ' + result.error);
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
                    <p><strong>ID:</strong> ${empleado.id}</p>
                    <p><strong>Nombre:</strong> ${empleado.nombre}</p>
                    <p><strong>Apellido:</strong> ${empleado.apellido}</p>
                    <p><strong>Rol:</strong> ${empleado.rol}</p>
                    <p><strong>Estado:</strong> 
                        <span class="badge badge-${this.getEstadoBadgeClass(empleado.estado)}">
                            ${empleado.estado}
                        </span>
                    </p>
                </div>
                <div class="col-md-6">
                    <p><strong>Email:</strong> ${empleado.email || '-'}</p>
                    <p><strong>Teléfono:</strong> ${empleado.telefono || '-'}</p>
                    <p><strong>Horario:</strong> ${empleado.horario_laboral}</p>
                    <p><strong>Nivel de estudio:</strong> ${empleado.nivel_estudio}</p>
                    <p><strong>Fecha de nacimiento:</strong> ${empleado.fecha_nacimiento || '-'}</p>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <p><strong>Domicilio:</strong> ${empleado.domicilio || '-'}</p>
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
            if (result.success) {
                this.renderStats(result.data);
            } else {
                this.showError('Error al cargar estadísticas: ' + result.error);
            }
        } catch (error) {
            this.showError('Error de conexión: ' + error.message);
        }
    }

    // Render statistics
    renderStats(stats) {
        // Update stats cards
        const totalElement = document.getElementById('total-empleados');
        const activosElement = document.getElementById('empleados-activos');
        const inactivosElement = document.getElementById('empleados-inactivos');
        const vacacionesElement = document.getElementById('empleados-vacaciones');

        if (totalElement) totalElement.textContent = stats.empleados.total;
        if (activosElement) activosElement.textContent = stats.empleados.activos;
        if (inactivosElement) inactivosElement.textContent = stats.empleados.inactivos;
        if (vacacionesElement) vacacionesElement.textContent = stats.empleados.vacaciones;

        // Render roles chart if exists
        this.renderRolesChart(stats.roles);
    }

    // Render roles chart
    renderRolesChart(roles) {
        const chartContainer = document.getElementById('roles-chart');
        if (!chartContainer) return;

        // Simple chart using Chart.js if available
        if (typeof Chart !== 'undefined') {
            const ctx = chartContainer.getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: roles.map(r => r.rol),
                    datasets: [{
                        data: roles.map(r => r.cantidad),
                        backgroundColor: [
                            '#FF6384',
                            '#36A2EB',
                            '#FFCE56',
                            '#4BC0C0',
                            '#9966FF'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    }

    // Show error message
    showError(message) {
        // You can implement this based on your UI framework
        console.error(message);
        alert(message); // Simple alert for now
    }

    // Initialize the UI
    init() {
        // Load initial data
        this.loadEmpleadosTable();
        this.loadStats();

        // Setup search functionality
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
