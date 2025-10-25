import React, { useState, useEffect } from 'react';
import { useDataIngestion } from '../services/DataIngestionContext';

const DebugPanel = () => {
  const { clearCache } = useDataIngestion();
  const [isVisible, setIsVisible] = useState(false);
  const [apiCallCount, setApiCallCount] = useState(0);

  useEffect(() => {
    // Escuchar los console.log para contar las llamadas API
    const originalLog = console.log;
    console.log = (...args) => {
      if (args[0] && typeof args[0] === 'string' && args[0].includes('API call for')) {
        setApiCallCount(prev => prev + 1);
      }
      originalLog(...args);
    };

    return () => {
      console.log = originalLog;
    };
  }, []);

  if (!isVisible) {
    return (
      <div 
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          background: '#007bff',
          color: 'white',
          padding: '10px',
          borderRadius: '5px',
          cursor: 'pointer',
          fontSize: '12px',
          zIndex: 1000
        }}
        onClick={() => setIsVisible(true)}
      >
        Debug Panel
      </div>
    );
  }

  return (
    <div 
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        background: 'white',
        border: '1px solid #ccc',
        borderRadius: '5px',
        padding: '15px',
        minWidth: '200px',
        fontSize: '12px',
        zIndex: 1000,
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
        <h4 style={{ margin: 0 }}>Debug Panel</h4>
        <button onClick={() => setIsVisible(false)} style={{ border: 'none', background: 'none', cursor: 'pointer' }}>×</button>
      </div>
      
      <div style={{ marginBottom: '10px' }}>
        <strong>API Calls Count:</strong> {apiCallCount}
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <button 
          onClick={() => setApiCallCount(0)}
          style={{
            padding: '5px 10px',
            marginRight: '10px',
            background: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '3px',
            cursor: 'pointer'
          }}
        >
          Reset Count
        </button>
        
        <button 
          onClick={clearCache}
          style={{
            padding: '5px 10px',
            background: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '3px',
            cursor: 'pointer'
          }}
        >
          Clear Cache
        </button>
      </div>
      
      <div style={{ fontSize: '11px', color: '#666' }}>
        <p>• Cache duration: 30s</p>
        <p>• Debounce delay: 300ms</p>
        <p>• Check console for detailed logs</p>
      </div>
    </div>
  );
};

export default DebugPanel;
