import { useState, useEffect } from 'react';

/**
 * Hook personalizado para debouncing de valores
 * @param {any} value - Valor a debounce
 * @param {number} delay - Delay en milisegundos
 * @returns {any} - Valor debouncado
 */
export const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

/**
 * Hook para manejar llamadas de API con debouncing
 * @param {Function} apiCall - Función de API a llamar
 * @param {number} delay - Delay en milisegundos
 * @returns {Function} - Función debouncada
 */
export const useDebouncedApiCall = (apiCall, delay = 300) => {
  const [timeoutId, setTimeoutId] = useState(null);

  const debouncedCall = (...args) => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    const newTimeoutId = setTimeout(() => {
      apiCall(...args);
    }, delay);

    setTimeoutId(newTimeoutId);
  };

  useEffect(() => {
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [timeoutId]);

  return debouncedCall;
};
