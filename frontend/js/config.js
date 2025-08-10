// Configuración del frontend
const API_BASE_URL = 'http://localhost:8000';

// Función helper para hacer llamadas a la API
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
        ...options
    };
    
    try {
        const response = await fetch(url, defaultOptions);
        return await response.json();
    } catch (error) {
        console.error('Error en llamada API:', error);
        throw error;
    }
}

// Exportar para uso global
window.API_BASE_URL = API_BASE_URL;
window.apiCall = apiCall;
