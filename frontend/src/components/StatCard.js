import React from 'react';
import './StatCard.css';

const StatCard = ({ 
  title, 
  value, 
  label, 
  icon, 
  color = '#007bff',
  trend = null,
  chartComponent = null 
}) => {
  return (
    <div className="stat-card">
      <div className="stat-card-header">
        <div className="stat-card-title">
          {icon && <span className="stat-card-icon" style={{ color }}>{icon}</span>}
          {title}
        </div>
        {trend && (
          <div className={`stat-trend ${trend.type}`}>
            <span className="trend-arrow">
              {trend.type === 'up' ? '↗' : trend.type === 'down' ? '↘' : '→'}
            </span>
            {trend.value}
          </div>
        )}
      </div>
      
      <div className="stat-card-content">
        <div className="stat-value" style={{ color }}>
          {value}
        </div>
        <div className="stat-label">
          {label}
        </div>
      </div>

      {chartComponent && (
        <div className="stat-card-chart">
          {chartComponent}
        </div>
      )}
    </div>
  );
};

export default StatCard;
