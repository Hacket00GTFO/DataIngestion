import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Error de conexión';
    throw new Error(message);
  }
);

export const dataIngestionAPI = {
  // Ingesta de datos
  ingestData: async (data) => {
    const response = await api.post('/data/ingest', {
      data,
      source: 'web_interface',
    });
    return response.data;
  },

  // Obtener datos
  getData: async () => {
    const response = await api.get('/data');
    return response.data;
  },

  // Obtener estadísticas
  getStatistics: async () => {
    const response = await api.get('/data/statistics');
    return response.data;
  },

  // Obtener esquema
  getSchema: async () => {
    const response = await api.get('/data/schema');
    return response.data;
  },

  // Agregar entrada manual
  addManualEntry: async (data) => {
    const response = await api.post('/data/manual-entry', data);
    return response.data;
  },

  // Obtener esquema de datos para entrada manual
  getDataSchema: async () => {
    const response = await api.get('/data/schema');
    return response.data;
  },

  // Verificar salud del servicio
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Estadísticas de tiradores (usando endpoint que funciona)
  getTiradoresStatistics: async () => {
    const response = await api.get('/tiradores/stats/tiradores');
    return response.data;
  },

  // Estadísticas de sesiones (mock temporalmente hasta resolver ruta)
  getSesionesStatistics: async () => {
    // Retornar datos vacíos temporalmente
    return {
      total_sesiones: 0,
      precision_promedio: null,
      distancia_promedio: null,
      tiempo_promedio: null,
      ambientes_unicos: 0,
      primera_sesion: null,
      ultima_sesion: null
    };
  },

  // Análisis completo
  getAnalisisCompleto: async (params = {}) => {
    const response = await api.get('/tiradores/analisis/completo', { params });
    return response.data;
  },

  // Obtener tiradores
  getTiradores: async (params = {}) => {
    const response = await api.get('/tiradores/', { params });
    return response.data;
  },

  // Eliminar todos los datos
  deleteAllData: async () => {
    const response = await api.delete('/database/all-data');
    return response.data;
  },

  // APIs de Excel eliminadas - solo entrada manual disponible
};

export default api;
