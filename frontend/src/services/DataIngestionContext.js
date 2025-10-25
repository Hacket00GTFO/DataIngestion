import React, { createContext, useContext, useState, useRef, useCallback } from 'react';
import { dataIngestionAPI } from './api';

const DataIngestionContext = createContext();

export const useDataIngestion = () => {
  const context = useContext(DataIngestionContext);
  if (!context) {
    throw new Error('useDataIngestion must be used within a DataIngestionProvider');
  }
  return context;
};

// Cache para almacenar respuestas de API
const apiCache = new Map();
const CACHE_DURATION = 30000; // 30 segundos

// Función para crear una clave de cache
const createCacheKey = (method, params = {}) => {
  return `${method}_${JSON.stringify(params)}`;
};

// Función para verificar si el cache es válido
const isCacheValid = (cacheEntry) => {
  return cacheEntry && (Date.now() - cacheEntry.timestamp) < CACHE_DURATION;
};

export const DataIngestionProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const debounceTimers = useRef(new Map());

  // Función helper para manejo de cache y debouncing
  const cachedApiCall = async (method, apiFunction, params = {}, useCache = true) => {
    const cacheKey = createCacheKey(method, params);
    
    // Verificar cache si está habilitado
    if (useCache) {
      const cached = apiCache.get(cacheKey);
      if (isCacheValid(cached)) {
        console.log(`Cache hit for ${method}`);
        return cached.data;
      }
    }

    // Debouncing: cancelar llamada anterior si existe
    if (debounceTimers.current.has(cacheKey)) {
      clearTimeout(debounceTimers.current.get(cacheKey));
    }

    return new Promise((resolve, reject) => {
      const timerId = setTimeout(async () => {
        try {
          console.log(`API call for ${method}`);
          const response = await apiFunction(params);
          
          // Guardar en cache
          if (useCache) {
            apiCache.set(cacheKey, {
              data: response,
              timestamp: Date.now()
            });
          }
          
          debounceTimers.current.delete(cacheKey);
          resolve(response);
        } catch (error) {
          debounceTimers.current.delete(cacheKey);
          reject(error);
        }
      }, 300); // 300ms de debounce

      debounceTimers.current.set(cacheKey, timerId);
    });
  };

  const ingestData = async (data) => {
    try {
      setLoading(true);
      setError(null);
      const response = await dataIngestionAPI.ingestData(data);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await cachedApiCall('getData', () => dataIngestionAPI.getData(), {}, true);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getStatistics = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await cachedApiCall('getStatistics', () => dataIngestionAPI.getStatistics(), {}, true);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getSchema = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await cachedApiCall('getSchema', () => dataIngestionAPI.getSchema(), {}, true);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getTiradoresStatistics = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await cachedApiCall('getTiradoresStatistics', () => dataIngestionAPI.getTiradoresStatistics(), {}, true);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getSesionesStatistics = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await dataIngestionAPI.getSesionesStatistics();
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getAnalisisCompleto = async (params = {}) => {
    try {
      setLoading(true);
      setError(null);
      const response = await cachedApiCall('getAnalisisCompleto', () => dataIngestionAPI.getAnalisisCompleto(params), params, true);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getTiradores = async (params = {}) => {
    try {
      setLoading(true);
      setError(null);
      const response = await dataIngestionAPI.getTiradores(params);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const addManualEntry = async (data) => {
    try {
      setLoading(true);
      setError(null);
      const response = await dataIngestionAPI.addManualEntry(data);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getDataSchema = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await cachedApiCall('getDataSchema', () => dataIngestionAPI.getDataSchema(), {}, true);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteAllData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await dataIngestionAPI.deleteAllData();
      // Limpiar cache después de eliminar datos
      apiCache.clear();
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Función para limpiar cache manualmente
  const clearCache = () => {
    apiCache.clear();
    console.log('Cache cleared');
  };

  const value = {
    loading,
    error,
    ingestData,
    getData,
    getStatistics,
    getSchema,
    getTiradoresStatistics,
    getSesionesStatistics,
    getAnalisisCompleto,
    getTiradores,
    addManualEntry,
    getDataSchema,
    deleteAllData,
    clearCache,
  };

  return (
    <DataIngestionContext.Provider value={value}>
      {children}
    </DataIngestionContext.Provider>
  );
};
