import React, { createContext, useContext, useState } from 'react';
import { dataIngestionAPI } from './api';

const DataIngestionContext = createContext();

export const useDataIngestion = () => {
  const context = useContext(DataIngestionContext);
  if (!context) {
    throw new Error('useDataIngestion must be used within a DataIngestionProvider');
  }
  return context;
};

export const DataIngestionProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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

  const getData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await dataIngestionAPI.getData();
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getStatistics = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await dataIngestionAPI.getStatistics();
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getSchema = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await dataIngestionAPI.getSchema();
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    loading,
    error,
    ingestData,
    getData,
    getStatistics,
    getSchema,
  };

  return (
    <DataIngestionContext.Provider value={value}>
      {children}
    </DataIngestionContext.Provider>
  );
};
