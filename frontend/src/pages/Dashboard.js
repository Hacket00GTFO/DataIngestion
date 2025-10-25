import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useDataIngestion } from '../services/DataIngestionContext';
import StatCard from '../components/StatCard';
import BarChart from '../components/BarChart';
import './Dashboard.css';

const Dashboard = () => {
  const { 
    getStatistics, 
    getTiradoresStatistics, 
    getSesionesStatistics, 
    getAnalisisCompleto 
  } = useDataIngestion();
  
  const [statistics, setStatistics] = useState(null);
  const [tiradoresStats, setTiradoresStats] = useState(null);
  const [sesionesStats, setSesionesStats] = useState(null);
  const [analisisCompleto, setAnalisisCompleto] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadAllStatistics = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Loading dashboard statistics...');
      
      const [stats, tiradores, sesiones, analisis] = await Promise.all([
        getStatistics(),
        getTiradoresStatistics(),
        getSesionesStatistics(),
        getAnalisisCompleto({ limit: 10 })
      ]);
      
      setStatistics(stats);
      setTiradoresStats(tiradores);
      setSesionesStats(sesiones);
      setAnalisisCompleto(analisis);
      console.log('Dashboard statistics loaded successfully');
    } catch (err) {
      console.error('Error loading dashboard statistics:', err);
      setError('Error cargando estadísticas');
    } finally {
      setLoading(false);
    }
  }, [getStatistics, getTiradoresStatistics, getSesionesStatistics, getAnalisisCompleto]);

  useEffect(() => {
    console.log('Dashboard useEffect triggered');
    loadAllStatistics();
  }, [loadAllStatistics]);

  // Preparar datos para gráficas usando useMemo para evitar recálculos
  // IMPORTANTE: Los hooks deben estar antes de cualquier return early
  const topTiradoresPrecisionData = useMemo(() => {
    if (!analisisCompleto.length) return [];
    return analisisCompleto
      .sort((a, b) => (b.precision_porcentaje || 0) - (a.precision_porcentaje || 0))
      .slice(0, 5)
      .map(tirador => ({
        label: tirador.nombre || 'Sin nombre',
        value: tirador.precision_porcentaje || 0
      }));
  }, [analisisCompleto]);

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

  const getDistribucionGeneroData = () => {
    if (!analisisCompleto.length) return [];
    const generos = analisisCompleto.reduce((acc, item) => {
      const genero = item.genero || 'No especificado';
      acc[genero] = (acc[genero] || 0) + 1;
      return acc;
    }, {});
    
    return Object.entries(generos).map(([genero, count]) => ({
      label: genero,
      value: count
    }));
  };

  const getAmbientesData = () => {
    if (!analisisCompleto.length) return [];
    const ambientes = analisisCompleto.reduce((acc, item) => {
      const ambiente = item.ambiente || 'No especificado';
      acc[ambiente] = (acc[ambiente] || 0) + 1;
      return acc;
    }, {});
    
    return Object.entries(ambientes).map(([ambiente, count]) => ({
      label: ambiente,
      value: count
    }));
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="container">
          <h1 className="dashboard-title">Dashboard</h1>
          <p className="dashboard-subtitle">
            Sistema de ingesta y procesamiento de datos para evidencia big data
          </p>
        </div>
      </div>

      {/* Estadísticas Principales */}
      <div className="dashboard-section">
        <div className="container">
          <h2 className="section-title">Estadísticas Generales</h2>
          <div className="stats-grid stats-grid-3">
            <StatCard
              title="Total de Registros"
              value={statistics?.total_records || 0}
              label="Registros procesados"
              icon="📊"
              color="#059669"
            />
            <StatCard
              title="Total de Tiradores"
              value={tiradoresStats?.total_tiradores || 0}
              label="Tiradores registrados"
              icon="👥"
              color="#10b981"
            />
            <StatCard
              title="Total de Sesiones"
              value={sesionesStats?.total_sesiones || 0}
              label="Sesiones de tiro"
              icon="🎯"
              color="#34d399"
            />
          </div>
        </div>
      </div>

      {/* Métricas de Rendimiento */}
      <div className="dashboard-section">
        <div className="container">
          <h2 className="section-title">Métricas de Rendimiento</h2>
          <div className="stats-grid stats-grid-4">
            <StatCard
              title="Precisión Promedio"
              value={sesionesStats?.precision_promedio ? 
                `${sesionesStats.precision_promedio.toFixed(1)}%` : 'N/A'}
              label="Tasa de aciertos"
              icon="🎯"
              color="#047857"
            />
            <StatCard
              title="Distancia Promedio"
              value={sesionesStats?.distancia_promedio ? 
                `${sesionesStats.distancia_promedio.toFixed(1)}m` : 'N/A'}
              label="Metros de tiro"
              icon="📏"
              color="#059669"
            />
            <StatCard
              title="Tiempo Promedio"
              value={sesionesStats?.tiempo_promedio ? 
                `${sesionesStats.tiempo_promedio.toFixed(1)}s` : 'N/A'}
              label="Segundos por tiro"
              icon="⏱️"
              color="#10b981"
            />
            <StatCard
              title="Diversidad de Géneros"
              value={tiradoresStats?.generos_unicos || 0}
              label="Géneros únicos"
              icon="⚧️"
              color="#34d399"
            />
          </div>
        </div>
      </div>

      {/* Estadísticas Demográficas */}
      <div className="dashboard-section">
        <div className="container">
          <h2 className="section-title">Estadísticas Demográficas</h2>
          <div className="stats-grid stats-grid-3">
            <StatCard
              title="Edad Promedio"
              value={tiradoresStats?.edad_promedio ? 
                `${tiradoresStats.edad_promedio.toFixed(1)}` : 'N/A'}
              label="Años de edad"
              icon="📅"
              color="#065f46"
            />
            <StatCard
              title="Experiencia Promedio"
              value={tiradoresStats?.experiencia_promedio ? 
                `${tiradoresStats.experiencia_promedio.toFixed(1)}` : 'N/A'}
              label="Años de práctica"
              icon="🏆"
              color="#047857"
            />
            <StatCard
              title="Altura Promedio"
              value={tiradoresStats?.altura_promedio ? 
                `${tiradoresStats.altura_promedio.toFixed(2)}m` : 'N/A'}
              label="Metros de estatura"
              icon="📐"
              color="#059669"
            />
          </div>
        </div>
      </div>

      {/* Análisis con Gráficas */}
      {analisisCompleto.length > 0 && (
        <div className="dashboard-section">
          <div className="container">
            <h2 className="section-title">Análisis de Rendimiento</h2>
            <div className="charts-grid">
              <div className="chart-card">
                <h3 className="chart-title">Top 5 Tiradores por Precisión</h3>
                <BarChart
                  data={topTiradoresPrecisionData}
                  title="Precisión (%)"
                  color="#047857"
                  height={250}
                  horizontal={true}
                />
              </div>

              <div className="chart-card">
                <h3 className="chart-title">Distribución por Género</h3>
                <BarChart
                  data={getDistribucionGeneroData()}
                  title="Cantidad"
                  color="#10b981"
                  height={250}
                />
              </div>

              <div className="chart-card">
                <h3 className="chart-title">Ambientes de Tiro</h3>
                <BarChart
                  data={getAmbientesData()}
                  title="Sesiones"
                  color="#34d399"
                  height={250}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Acciones Rápidas */}
      <div className="dashboard-section">
        <div className="container">
          <h2 className="section-title">Acciones Rápidas</h2>
          <div className="quick-actions-grid">
            <a href="/ingest" className="action-card action-primary">
              <div className="action-icon">📥</div>
              <div className="action-content">
                <h3>Ingresar Nuevos Datos</h3>
                <p>Cargar y procesar nuevos datos de tiro</p>
              </div>
            </a>
            <a href="/view" className="action-card action-secondary">
              <div className="action-icon">👁️</div>
              <div className="action-content">
                <h3>Ver Datos Existentes</h3>
                <p>Explorar y analizar datos almacenados</p>
              </div>
            </a>
          </div>
        </div>
      </div>

      {/* Estado del Sistema */}
      <div className="dashboard-section">
        <div className="container">
          <h2 className="section-title">Estado del Sistema</h2>
          <div className="system-status-grid">
            <div className="status-card status-healthy">
              <div className="status-icon">🟢</div>
              <div className="status-content">
                <h4>API Backend</h4>
                <span className="status-label">Conectado</span>
              </div>
            </div>
            <div className="status-card status-healthy">
              <div className="status-icon">🟢</div>
              <div className="status-content">
                <h4>Base de Datos</h4>
                <span className="status-label">Activa</span>
              </div>
            </div>
            <div className="status-card status-healthy">
              <div className="status-icon">🟢</div>
              <div className="status-content">
                <h4>Procesamiento</h4>
                <span className="status-label">Operativo</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
