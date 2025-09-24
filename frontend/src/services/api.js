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

  // Subir archivo Excel
  uploadExcel: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/data/upload-excel', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Verificar salud del servicio
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
