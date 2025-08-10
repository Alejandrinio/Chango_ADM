/**
 * Dashboard.js - Funcionalidad del Dashboard de RRHH
 * Maneja KPIs, charts y acciones rápidas
 */

class DashboardUI {
    constructor() {
        this.apiBase = 'http://localhost:8000/api';
        this.selectedDate = null;
        this.charts = {}; // Almacenar referencias a los charts
        this.init();
    }

    async init() {
        this.setupDateSelector();
        await this.loadKPIs();
        await this.loadCharts();
        this.setupEventListeners();
    }

    setupDateSelector() {
        const dateSelector = document.getElementById('dashboard-date');
        const quickActionDateSelector = document.getElementById('date-selector');
        
        // Establecer fecha actual por defecto
        const today = new Date().toISOString().split('T')[0];
        
        console.log('🔧 SetupDateSelector - Fecha actual:', today);
        
        if (dateSelector) {
            dateSelector.value = today;
            dateSelector.addEventListener('change', (e) => {
                this.selectedDate = e.target.value;
                console.log('📅 DateSelector cambiado a:', this.selectedDate);
                // Sincronizar ambos selectores
                if (quickActionDateSelector) {
                    quickActionDateSelector.value = e.target.value;
                }
                this.refreshDashboard();
            });
        }
        
        if (quickActionDateSelector) {
            quickActionDateSelector.value = today;
            quickActionDateSelector.addEventListener('change', (e) => {
                this.selectedDate = e.target.value;
                console.log('📅 QuickActionDateSelector cambiado a:', this.selectedDate);
                // Sincronizar ambos selectores
                if (dateSelector) {
                    dateSelector.value = e.target.value;
                }
                this.refreshDashboard();
            });
        }
    }

    async loadKPIs() {
        try {
            let url = `${this.apiBase}/dashboard/kpis`;
            if (this.selectedDate) {
                url += `?fecha=${this.selectedDate}`;
            }
            
            const response = await fetch(url);
            const result = await response.json();
            
            if (result.success) {
                this.updateKPICards(result.data);
            } else {
                console.error('Error cargando KPIs:', result.error);
            }
        } catch (error) {
            console.error('Error en loadKPIs:', error);
        }
    }

    updateKPICards(data) {
        // Actualizar cards de KPIs
        const elements = {
            'kpi-empleados-activos': data.empleados_activos || 0,
            'kpi-ausencias-hoy': data.ausencias_hoy || 0,
            'kpi-horas-extras': data.horas_extras_mes || 0,
            'kpi-recibos-pendientes': data.recibos_pendientes || 0
        };

        for (const [id, value] of Object.entries(elements)) {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        }
    }

    async loadCharts() {
        try {
            let url = `${this.apiBase}/dashboard/charts`;
            if (this.selectedDate) {
                url += `?fecha=${this.selectedDate}`;
            }
            
            console.log('🔍 Debug loadCharts:', {
                selectedDate: this.selectedDate,
                url: url
            });
            
            const response = await fetch(url);
            const result = await response.json();
            
            if (result.success) {
                console.log('📊 Charts data:', result.data);
                this.renderCharts(result.data);
            } else {
                console.error('Error cargando charts:', result.error);
            }
        } catch (error) {
            console.error('Error en loadCharts:', error);
        }
    }

    renderCharts(data) {
        // Destruir charts existentes antes de crear nuevos
        this.destroyCharts();
        
        // Chart 1: Distribución por Roles (Pie Chart)
        this.renderPieChart('roles-chart', data.distribucion_roles);
        
        // Chart 2: Asistencia Semanal (Line Chart)
        this.renderLineChart('asistencia-chart', data.asistencia_semanal);
        
        // Chart 3: Horas Extras por Área (Bar Chart)
        this.renderBarChart('horas-extras-chart', data.horas_extras_area);
    }

    destroyCharts() {
        // Destruir todos los charts existentes
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
        this.charts = {};
    }

    renderPieChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const labels = data.map(item => item.rol);
        const values = data.map(item => item.cantidad);
        const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'];

        this.charts[canvasId] = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Distribución por Roles'
                    }
                }
            }
        });
    }

    renderLineChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const labels = data.map(item => item.dia);
        const values = data.map(item => item.asistencia);

        this.charts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Asistencia (%)',
                    data: values,
                    borderColor: '#36A2EB',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Asistencia Semanal'
                    }
                }
            }
        });
    }

    renderBarChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const labels = data.map(item => item.area);
        const values = data.map(item => item.horas);

        this.charts[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Horas Extras',
                    data: values,
                    backgroundColor: '#FF6384',
                    borderColor: '#FF6384',
                    borderWidth: 1
                    }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Horas Extras por Área'
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Botones de acción rápida
        const quickActions = document.querySelectorAll('.quick-action');
        quickActions.forEach(button => {
            button.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                this.handleQuickAction(action);
            });
        });

        // Botón de refresh
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshDashboard();
            });
        }
    }

    handleQuickAction(action) {
        switch (action) {
            case 'empleados':
                window.location.href = 'empleados.html';
                break;
            case 'fichajes':
                window.location.href = 'fichajes.html';
                break;
            case 'recibos':
                window.location.href = 'recibos.html';
                break;
            case 'reportes':
                window.location.href = 'charts.html';
                break;
            default:
                console.log('Acción no implementada:', action);
        }
    }

    async refreshDashboard() {
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Actualizando...';
            refreshBtn.disabled = true;
        }

        try {
            await this.loadKPIs();
            await this.loadCharts();
        } finally {
            if (refreshBtn) {
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Actualizar';
                refreshBtn.disabled = false;
            }
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si estamos en la página del dashboard
    if (document.getElementById('dashboard-container')) {
        window.dashboardUI = new DashboardUI();
    }
});
