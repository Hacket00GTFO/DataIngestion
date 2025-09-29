import React, { useState, useEffect, useCallback } from 'react';
import { useDataIngestion } from '../services/DataIngestionContext';
import './DataForm.css';

const DataForm = () => {
  const { addManualEntry, getDataSchema, getData } = useDataIngestion();
  const [formData, setFormData] = useState({});
  const [schema, setSchema] = useState([]);
  const [existingData, setExistingData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const loadSchema = useCallback(async () => {
    try {
      const schemaData = await getDataSchema();
      setSchema(schemaData.columns || []);
      initializeFormData(schemaData.columns || []);
    } catch (error) {
      setMessage('Error cargando esquema de datos');
      setMessageType('error');
    }
  }, [getDataSchema]);

  const loadExistingData = useCallback(async () => {
    try {
      const dataResponse = await getData();
      setExistingData(dataResponse.data || []);
    } catch (error) {
      console.error('Error cargando datos existentes:', error);
    }
  }, [getData]);

  useEffect(() => {
    loadSchema();
    loadExistingData();
  }, [loadSchema, loadExistingData]);

  const initializeFormData = (columns) => {
    const initialData = {};
    columns.forEach(column => {
      initialData[column.name] = column.type === 'number' ? '' : '';
    });
    setFormData(initialData);
  };

  const updateField = (field, value) => {
    setFormData({
      ...formData,
      [field]: value
    });
  };

  const resetForm = () => {
    initializeFormData(schema);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      // Filtrar campos vacíos para enviar solo datos válidos
      const cleanData = {};
      Object.keys(formData).forEach(key => {
        if (formData[key] !== '' && formData[key] !== null && formData[key] !== undefined) {
          // Convertir números si es necesario
          const schemaField = schema.find(s => s.name === key);
          if (schemaField && schemaField.type === 'number') {
            cleanData[key] = parseFloat(formData[key]) || 0;
          } else {
            cleanData[key] = formData[key];
          }
        }
      });

      const result = await addManualEntry(cleanData);
      if (result.success) {
        setMessage(result.message);
        setMessageType('success');
        resetForm();
        loadExistingData(); // Recargar datos para mostrar el nuevo registro
      } else {
        setMessage(result.message || 'Error en el procesamiento');
        setMessageType('error');
      }
    } catch (error) {
      setMessage('Error de conexión con el servidor');
      setMessageType('error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="data-form">
      <div className="container">
        <h2>Ingesta Manual de Datos</h2>
        <p>Ingrese nuevos registros de tiro de forma manual para análisis.</p>

        {message && (
          <div className={`alert alert-${messageType}`}>
            {message}
          </div>
        )}

        <div className="form-section">
          <h3>Datos Existentes</h3>
          {existingData.length > 0 ? (
            <div className="data-preview">
              <p>Se encontraron {existingData.length} registros:</p>
              <div className="data-table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      {schema.slice(0, 6).map((column) => (
                        <th key={column.name}>{column.name}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {existingData.slice(0, 5).map((record, index) => (
                      <tr key={index}>
                        {schema.slice(0, 6).map((column) => (
                          <td key={column.name}>
                            {record[column.name] || '-'}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {existingData.length > 5 && (
                  <p className="data-more">
                    ... y {existingData.length - 5} registros más
                  </p>
                )}
              </div>
            </div>
          ) : (
            <p>No hay datos cargados aún. Agregue el primer registro abajo.</p>
          )}
        </div>

        <div className="form-section">
          <div className="section-header">
            <h3>Nuevo Registro</h3>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              {schema.map((column) => (
                <div key={column.name} className="form-group">
                  <label className="form-label">
                    {column.name.replace(/_/g, ' ').toUpperCase()}
                    {column.required && <span className="required">*</span>}
                  </label>
                  {column.description && (
                    <small className="field-description">{column.description}</small>
                  )}
                  
                  {column.name === 'genero' ? (
                    <select 
                      className="form-input"
                      value={formData[column.name] || ''}
                      onChange={(e) => updateField(column.name, e.target.value)}
                      required={column.required}
                    >
                      <option value="">Seleccionar...</option>
                      <option value="Masculino">Masculino</option>
                      <option value="Femenino">Femenino</option>
                    </select>
                  ) : column.name === 'ambiente' ? (
                    <select 
                      className="form-input"
                      value={formData[column.name] || ''}
                      onChange={(e) => updateField(column.name, e.target.value)}
                      required={column.required}
                    >
                      <option value="">Seleccionar...</option>
                      <option value="Interior">Interior</option>
                      <option value="Exterior">Exterior</option>
                    </select>
                  ) : (
                    <input
                      type={column.type === 'number' ? 'number' : 'text'}
                      className="form-input"
                      value={formData[column.name] || ''}
                      onChange={(e) => updateField(column.name, e.target.value)}
                      required={column.required}
                      placeholder={`Ingrese ${column.name.replace(/_/g, ' ').toLowerCase()}`}
                      step={column.type === 'number' ? '0.01' : undefined}
                      min={column.type === 'number' && (column.name.includes('edad') || column.name.includes('experiencia') || column.name.includes('tiros')) ? '0' : undefined}
                    />
                  )}
                  
                  <small className="field-type">
                    {column.required ? 'Requerido' : 'Opcional'}
                  </small>
                </div>
              ))}
            </div>

            <div className="form-actions">
              <button
                type="button"
                onClick={resetForm}
                className="btn btn-secondary"
                style={{marginRight: '10px'}}
              >
                Limpiar
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Guardando...' : 'Guardar Registro'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default DataForm;
