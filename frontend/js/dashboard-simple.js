// Dashboard Simple Debug
console.log('🚀 Dashboard Simple iniciado');

// Test API endpoints directly
async function testAPI() {
    console.log('🔍 Probando API...');
    
    try {
        // Test KPIs
        console.log('📊 Probando KPIs...');
        const kpisResponse = await fetch('http://localhost:8000/api/dashboard/kpis');
        const kpisData = await kpisResponse.json();
        console.log('✅ KPIs Response:', kpisData);
        
        if (kpisData.success) {
            updateKPIs(kpisData.data);
        }
        
        // Test Charts
        console.log('📈 Probando Charts...');
        const chartsResponse = await fetch('http://localhost:8000/api/dashboard/charts');
        const chartsData = await chartsResponse.json();
        console.log('✅ Charts Response:', chartsData);
        
        if (chartsData.success) {
            renderCharts(chartsData.data);
        }
        
    } catch (error) {
        console.error('❌ Error en API:', error);
    }
}

function updateKPIs(data) {
    console.log('📈 Actualizando KPIs:', data);
    
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

function renderCharts(data) {
    console.log('🎨 Renderizando charts:', data);
    
    // Chart 1: Distribución por Roles
    if (data.distribucion_roles) {
        renderPieChart('roles-chart', data.distribucion_roles);
    }
    
    // Chart 2: Asistencia Semanal
    if (data.asistencia_semanal) {
        renderLineChart('asistencia-chart', data.asistencia_semanal);
    }
    
    // Chart 3: Horas Extras por Área
    if (data.horas_extras_area) {
        renderBarChart('horas-extras-chart', data.horas_extras_area);
    }
}

function renderPieChart(canvasId, data) {
    console.log(`🥧 Renderizando pie chart ${canvasId}:`, data);
    
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`❌ Canvas no encontrado: ${canvasId}`);
        return;
    }

    const labels = data.map(item => item.rol);
    const values = data.map(item => item.cantidad);
    const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'];

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
        console.log(`✅ Pie chart ${canvasId} renderizado`);
    } catch (error) {
        console.error(`❌ Error en pie chart ${canvasId}:`, error);
    }
}

function renderLineChart(canvasId, data) {
    console.log(`📈 Renderizando line chart ${canvasId}:`, data);
    
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`❌ Canvas no encontrado: ${canvasId}`);
        return;
    }

    const labels = data.map(item => item.dia);
    const values = data.map(item => item.asistencia);

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
        console.log(`✅ Line chart ${canvasId} renderizado`);
    } catch (error) {
        console.error(`❌ Error en line chart ${canvasId}:`, error);
    }
}

function renderBarChart(canvasId, data) {
    console.log(`📊 Renderizando bar chart ${canvasId}:`, data);
    
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`❌ Canvas no encontrado: ${canvasId}`);
        return;
    }

    const labels = data.map(item => item.area);
    const values = data.map(item => item.horas);

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
        console.log(`✅ Bar chart ${canvasId} renderizado`);
    } catch (error) {
        console.error(`❌ Error en bar chart ${canvasId}:`, error);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM cargado, iniciando test...');
    
    // Verificar Chart.js
    if (typeof Chart !== 'undefined') {
        console.log('✅ Chart.js disponible');
        console.log('📊 Versión Chart.js:', Chart.version);
    } else {
        console.error('❌ Chart.js NO disponible');
    }
    
    // Ejecutar test después de un pequeño delay
    setTimeout(testAPI, 1000);
});

// También ejecutar inmediatamente si ya está cargado
if (document.readyState === 'loading') {
    console.log('📝 DOM aún cargando...');
} else {
    console.log('📝 DOM ya cargado, ejecutando inmediatamente...');
    testAPI();
}
