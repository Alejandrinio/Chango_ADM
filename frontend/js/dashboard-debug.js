/**
 * Dashboard Debug - Versión de debug para identificar problemas
 */

class DashboardDebug {
    constructor() {
        this.apiBase = 'http://localhost:8000/api';
        this.init();
    }

    async init() {
        console.log('🔍 Dashboard Debug iniciado');
        await this.testKPIs();
        await this.testCharts();
        this.testChartJS();
    }

    async testKPIs() {
        console.log('📊 Probando KPIs...');
        try {
            const response = await fetch(`${this.apiBase}/dashboard/kpis`);
            const result = await response.json();
            
            console.log('✅ KPIs Response:', result);
            
            if (result.success) {
                this.updateKPICards(result.data);
            } else {
                console.error('❌ Error en KPIs:', result.error);
            }
        } catch (error) {
            console.error('❌ Error cargando KPIs:', error);
        }
    }

    updateKPICards(data) {
        console.log('📈 Actualizando KPIs con datos:', data);
        
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
                console.log(`✅ Actualizado ${id}: ${value}`);
            } else {
                console.error(`❌ Elemento no encontrado: ${id}`);
            }
        }
    }

    async testCharts() {
        console.log('📊 Probando Charts...');
        try {
            const response = await fetch(`${this.apiBase}/dashboard/charts`);
            const result = await response.json();
            
            console.log('✅ Charts Response:', result);
            
            if (result.success) {
                this.renderCharts(result.data);
            } else {
                console.error('❌ Error en Charts:', result.error);
            }
        } catch (error) {
            console.error('❌ Error cargando Charts:', error);
        }
    }

    renderCharts(data) {
        console.log('🎨 Renderizando charts con datos:', data);
        
        // Chart 1: Distribución por Roles
        this.renderPieChart('roles-chart', data.distribucion_roles);
        
        // Chart 2: Asistencia Semanal
        this.renderLineChart('asistencia-chart', data.asistencia_semanal);
        
        // Chart 3: Horas Extras por Área
        this.renderBarChart('horas-extras-chart', data.horas_extras_area);
    }

    renderPieChart(canvasId, data) {
        console.log(`🥧 Renderizando pie chart ${canvasId} con datos:`, data);
        
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`❌ Canvas no encontrado: ${canvasId}`);
            return;
        }

        console.log(`✅ Canvas encontrado: ${canvasId}`);

        const labels = data.map(item => item.rol);
        const values = data.map(item => item.cantidad);
        const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'];

        console.log('📊 Datos del pie chart:', { labels, values });

        try {
            new Chart(ctx, {
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
            console.log(`✅ Pie chart ${canvasId} renderizado exitosamente`);
        } catch (error) {
            console.error(`❌ Error renderizando pie chart ${canvasId}:`, error);
        }
    }

    renderLineChart(canvasId, data) {
        console.log(`📈 Renderizando line chart ${canvasId} con datos:`, data);
        
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`❌ Canvas no encontrado: ${canvasId}`);
            return;
        }

        console.log(`✅ Canvas encontrado: ${canvasId}`);

        const labels = data.map(item => item.dia);
        const values = data.map(item => item.asistencia);

        console.log('📊 Datos del line chart:', { labels, values });

        try {
            new Chart(ctx, {
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
            console.log(`✅ Line chart ${canvasId} renderizado exitosamente`);
        } catch (error) {
            console.error(`❌ Error renderizando line chart ${canvasId}:`, error);
        }
    }

    renderBarChart(canvasId, data) {
        console.log(`📊 Renderizando bar chart ${canvasId} con datos:`, data);
        
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`❌ Canvas no encontrado: ${canvasId}`);
            return;
        }

        console.log(`✅ Canvas encontrado: ${canvasId}`);

        const labels = data.map(item => item.area);
        const values = data.map(item => item.horas);

        console.log('📊 Datos del bar chart:', { labels, values });

        try {
            new Chart(ctx, {
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
            console.log(`✅ Bar chart ${canvasId} renderizado exitosamente`);
        } catch (error) {
            console.error(`❌ Error renderizando bar chart ${canvasId}:`, error);
        }
    }

    testChartJS() {
        console.log('🧪 Probando Chart.js...');
        
        if (typeof Chart !== 'undefined') {
            console.log('✅ Chart.js está disponible');
            console.log('📊 Versión de Chart.js:', Chart.version);
        } else {
            console.error('❌ Chart.js NO está disponible');
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM cargado, iniciando Dashboard Debug');
    
    // Verificar si estamos en la página del dashboard
    if (document.getElementById('dashboard-container')) {
        console.log('✅ Dashboard container encontrado');
        window.dashboardDebug = new DashboardDebug();
    } else {
        console.log('❌ Dashboard container no encontrado');
    }
});
