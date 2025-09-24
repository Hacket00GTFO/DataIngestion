import React, { useState, useEffect } from 'react';
import { useDataIngestion } from '../services/DataIngestionContext';
import './DataForm.css';

const DataForm = () => {
  const { ingestData, getSchema } = useDataIngestion();
  const [formData, setFormData] = useState([]);
  const [schema, setSchema] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  useEffect(() => {
    loadSchema();
  }, []);

  const loadSchema = async () => {
    try {
      const schemaData = await getSchema();
      setSchema(schemaData.columns || []);
      initializeFormData(schemaData.columns || []);
    } catch (error) {
      setMessage('Error cargando esquema de datos');
      setMessageType('error');
    }
  };

  const initializeFormData = (columns) => {
    const initialData = {};
    columns.forEach(column => {
      initialData[column.name] = '';
    });
    setFormData([initialData]);
  };

  const addNewRecord = () => {
    const newRecord = {};
    schema.forEach(column => {
      newRecord[column.name] = '';
    });
    setFormData([...formData, newRecord]);
  };

  const removeRecord = (index) => {
    if (formData.length > 1) {
      const newData = formData.filter((_, i) => i !== index);
      setFormData(newData);
    }
  };

  const updateRecord = (index, field, value) => {
    const newData = [...formData];
    newData[index][field] = value;
    setFormData(newData);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const result = await ingestData(formData);
      if (result.success) {
        setMessage(result.message);
        setMessageType('success');
        initializeFormData(schema);
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

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('/api/v1/data/upload-excel', {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      
      if (result.success) {
        setMessage('Archivo procesado exitosamente');
        setMessageType('success');
      } else {
        setMessage('Error procesando archivo');
        setMessageType('error');
      }
    } catch (error) {
      setMessage('Error subiendo archivo');
      setMessageType('error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="data-form">
      <div className="container">
        <h2>Ingesta de Datos</h2>
        <p>Ingrese nuevos registros basados en el esquema de evidencia big data.</p>

        {message && (
          <div className={`alert alert-${messageType}`}>
            {message}
          </div>
        )}

        <div className="form-section">
          <h3>Subir Archivo Excel</h3>
          <div className="file-upload">
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileUpload}
              className="file-input"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="file-label">
              Seleccionar Archivo Excel
            </label>
          </div>
        </div>

        <div className="form-section">
          <div className="section-header">
            <h3>Ingreso Manual de Datos</h3>
            <button
              type="button"
              onClick={addNewRecord}
              className="btn btn-secondary"
            >
              Agregar Registro
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {formData.map((record, recordIndex) => (
              <div key={recordIndex} className="record-form">
                <div className="record-header">
                  <h4>Registro {recordIndex + 1}</h4>
                  {formData.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeRecord(recordIndex)}
                      className="btn btn-danger"
                    >
                      Eliminar
                    </button>
                  )}
                </div>

                <div className="form-grid">
                  {schema.map((column) => (
                    <div key={column.name} className="form-group">
                      <label className="form-label">
                        {column.name}
                        {column.required && <span className="required">*</span>}
                      </label>
                      <input
                        type={column.type === 'number' ? 'number' : 'text'}
                        className="form-input"
                        value={record[column.name] || ''}
                        onChange={(e) => updateRecord(recordIndex, column.name, e.target.value)}
                        required={column.required}
                      />
                    </div>
                  ))}
                </div>
              </div>
            ))}

            <div className="form-actions">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Procesando...' : 'Procesar Datos'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default DataForm;
