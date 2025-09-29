# Frontend - Data Ingestion UI

Interfaz web simplificada en React para ingesta manual de datos de tiro deportivo.

## Características

- **React 18**: Interfaz moderna y responsiva
- **Formulario Inteligente**: Validación automática y selectores
- **Tiempo Real**: Muestra datos ingresados inmediatamente
- **Modo Offline**: Funciona sin backend para demos
- **Responsive**: Optimizada para desktop y móvil

## Instalación Rápida

### Método 1: Script Automático (Windows)
```bash
# Desde la raíz del proyecto
start-frontend.bat
```

### Método 2: Manual
```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
```

## Acceso

- **Frontend**: http://localhost:3000
- **Hot Reload**: Los cambios se reflejan automáticamente

## Estructura Simplificada

```
frontend/
├── src/
│   ├── App.js                  # Componente principal
│   ├── pages/
│   │   ├── Dashboard.js        # Dashboard con estadísticas
│   │   ├── DataForm.js         # Formulario ingesta manual
│   │   └── DataViewer.js       # Visualizador de datos
│   ├── services/
│   │   ├── api.js              # Cliente API
│   │   └── DataIngestionContext.js # Contexto React
│   └── components/
│       └── Header.js           # Navegación
├── package.json                # Dependencias
└── public/                     # Archivos estáticos
```

## Páginas Principales

### 1. Dashboard (`/`)
- Resumen de estadísticas
- Gráficos básicos
- Estado del sistema

### 2. Formulario (`/form`)
- **Ingesta Manual**: Formulario completo
- **Validación**: En tiempo real
- **Cálculos**: Precisión automática
- **Selectores**: Género y ambiente

### 3. Visualizador (`/data`)
- **Tabla de Datos**: Registros ingresados
- **Filtros**: Por campo
- **Paginación**: Para grandes datasets

## Formulario de Ingesta

### Campos Disponibles
| Campo | Tipo | Validación |
|-------|------|------------|
| **Nombre** | Texto | Requerido, min 2 caracteres |
| **Edad** | Número | 0-120 años |
| **Género** | Selector | Masculino/Femenino |
| **Experiencia** | Número | 0-50 años |
| **Distancia** | Número | 0-1000 metros, decimales |
| **Ambiente** | Selector | Interior/Exterior |
| **Tiros Exitosos** | Número | 0-máximo |
| **Tiros Totales** | Número | 1-máximo |
| **Tiempo Sesión** | Número | 0-600 minutos, decimales |

### Características del Formulario
- **Precisión Automática**: Se calcula al ingresar tiros
- **Validación Visual**: Campos con error se resaltan
- **Limpieza**: Botón para resetear formulario
- **Confirmación**: Mensaje de éxito/error

## Configuración

### Variables de Entorno
```env
# .env o .env.local
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Modo de Desarrollo
```javascript
// En src/services/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
```

## Desarrollo

### Comandos Útiles
```bash
# Desarrollo
npm start                # Servidor de desarrollo

# Build
npm run build           # Compilar para producción

# Testing
npm test               # Ejecutar tests

# Linting
npm run lint           # Verificar código
```

### Estructura de Componentes
```jsx
App
├── Header              # Navegación
├── Dashboard          # Página principal
├── DataForm           # Formulario ingesta
└── DataViewer         # Visualizador datos
```

### Context API
```javascript
// Proveedor global de datos
DataIngestionProvider
├── addManualEntry()   # Agregar registro
├── getData()          # Obtener datos  
├── getDataSchema()    # Obtener esquema
└── loading/error      # Estados
```

## Personalización

### Agregar Nuevos Campos
1. El esquema se obtiene automáticamente del backend
2. El formulario se genera dinámicamente
3. No requiere cambios manuales en frontend

### Cambiar Estilos
```css
/* src/pages/DataForm.css */
.form-input {
    /* Personalizar campos */
}

.btn-primary {
    /* Personalizar botones */
}
```

### Agregar Validaciones
```javascript
// En src/pages/DataForm.js
const validateField = (name, value) => {
    switch(name) {
        case 'edad':
            return value >= 0 && value <= 120;
        // Agregar más validaciones
    }
};
```

## Dependencias Principales

```json
{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0"
}
```

## Solución de Problemas

### Error de CORS
```javascript
// El backend ya tiene CORS configurado
// Si hay problemas, verificar:
// 1. Backend ejecutándose en puerto 8000
// 2. Variable REACT_APP_API_URL correcta
```

### Puerto ocupado
```bash
# React detecta automáticamente y sugiere otro puerto
# O forzar puerto específico:
PORT=3001 npm start
```

### Error de build
```bash
# Limpiar caché
npm run build
rm -rf node_modules package-lock.json
npm install
```

### Problemas de dependencias
```bash
# Reinstalación completa
rm -rf node_modules package-lock.json
npm install --force
```

## Modo Offline

El frontend funciona **sin backend**:
- Formulario se carga normalmente
- Validación funciona en cliente
- Muestra mensaje de "modo offline"
- Perfecto para demos y desarrollo

## Testing

### Probar Manualmente
1. Ir a http://localhost:3000/form
2. Llenar formulario con datos válidos
3. Verificar cálculo automático de precisión
4. Enviar y verificar mensaje de confirmación

### Casos de Prueba
- **Datos válidos**: Formulario completo
- **Solo nombre**: Campo mínimo requerido
- **Tiros**: Verificar cálculo de precisión
- **Validación**: Campos con errores

Este frontend está optimizado para facilidad de uso y desarrollo rápido.
