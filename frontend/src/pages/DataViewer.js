import React, { useState, useEffect } from 'react';
import { useDataIngestion } from '../services/DataIngestionContext';
import './DataViewer.css';

const DataViewer = () => {
  const { getData } = useDataIngestion();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortField, setSortField] = useState('');
  const [sortDirection, setSortDirection] = useState('asc');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const result = await getData();
      setData(result.data || []);
    } catch (err) {
      setError('Error cargando datos');
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const filteredAndSortedData = () => {
    let filtered = data;

    // Aplicar filtro de búsqueda
    if (searchTerm) {
      filtered = data.filter(record =>
        Object.values(record).some(value =>
          String(value).toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }

    // Aplicar ordenamiento
    if (sortField) {
      filtered.sort((a, b) => {
        const aVal = a[sortField];
        const bVal = b[sortField];
        
        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return filtered;
  };

  const paginatedData = () => {
    const filtered = filteredAndSortedData();
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return filtered.slice(startIndex, endIndex);
  };

  const totalPages = Math.ceil(filteredAndSortedData().length / itemsPerPage);

  const getColumns = () => {
    if (data.length === 0) return [];
    return Object.keys(data[0]);
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
    <div className="data-viewer">
      <div className="container">
        <h2>Visualizador de Datos</h2>
        <p>Visualice y explore los datos procesados del sistema.</p>

        <div className="viewer-controls">
          <div className="search-box">
            <input
              type="text"
              placeholder="Buscar en los datos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="form-input"
            />
          </div>
          
          <div className="viewer-info">
            <span>
              Mostrando {paginatedData().length} de {filteredAndSortedData().length} registros
            </span>
          </div>
        </div>

        {data.length === 0 ? (
          <div className="empty-state">
            <h3>No hay datos disponibles</h3>
            <p>Los datos aparecerán aquí una vez que se procesen registros.</p>
          </div>
        ) : (
          <>
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    {getColumns().map((column) => (
                      <th
                        key={column}
                        onClick={() => handleSort(column)}
                        className="sortable"
                      >
                        {column}
                        {sortField === column && (
                          <span className="sort-indicator">
                            {sortDirection === 'asc' ? '↑' : '↓'}
                          </span>
                        )}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {paginatedData().map((record, index) => (
                    <tr key={index}>
                      {getColumns().map((column) => (
                        <td key={column}>
                          {record[column] || '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {totalPages > 1 && (
              <div className="pagination">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="btn btn-secondary"
                >
                  Anterior
                </button>
                
                <span className="pagination-info">
                  Página {currentPage} de {totalPages}
                </span>
                
                <button
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="btn btn-secondary"
                >
                  Siguiente
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default DataViewer;
