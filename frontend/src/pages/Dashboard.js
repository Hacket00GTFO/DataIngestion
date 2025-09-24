import React, { useState, useEffect } from 'react';
import { useDataIngestion } from '../services/DataIngestionContext';
import './Dashboard.css';

const Dashboard = () => {
  const { getStatistics } = useDataIngestion();
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      setLoading(true);
      const stats = await getStatistics();
      setStatistics(stats);
    } catch (err) {
      setError('Error cargando estadísticas');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="alert alert-error">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="container">
        <h2>Dashboard - Data Ingestion System</h2>
        <p className="dashboard-description">
          Sistema de ingesta y procesamiento de datos para evidencia big data.
        </p>
      </div>

      <div className="grid grid-3">
        <div className="card">
          <div className="card-title">Total de Registros</div>
          <div className="card-content">
            <div className="stat-number">
              {statistics?.total_records || 0}
            </div>
            <div className="stat-label">Registros procesados</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Última Actualización</div>
          <div className="card-content">
            <div className="stat-text">
              {statistics?.last_updated || 'N/A'}
            </div>
            <div className="stat-label">Timestamp</div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Fuentes de Datos</div>
          <div className="card-content">
            <div className="stat-number">
              {statistics?.data_sources?.length || 0}
            </div>
            <div className="stat-label">Fuentes activas</div>
          </div>
        </div>
      </div>

      <div className="container">
        <h3>Acciones Rápidas</h3>
        <div className="quick-actions">
          <a href="/ingest" className="btn btn-primary">
            Ingresar Nuevos Datos
          </a>
          <a href="/view" className="btn btn-secondary">
            Ver Datos Existentes
          </a>
        </div>
      </div>

      <div className="container">
        <h3>Estado del Sistema</h3>
        <div className="system-status">
          <div className="status-item">
            <span className="status-label">API Backend:</span>
            <span className="status-value status-healthy">Conectado</span>
          </div>
          <div className="status-item">
            <span className="status-label">Base de Datos:</span>
            <span className="status-value status-healthy">Activa</span>
          </div>
          <div className="status-item">
            <span className="status-label">Procesamiento:</span>
            <span className="status-value status-healthy">Operativo</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
