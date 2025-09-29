FROM node:18-alpine

# Metadatos del contenedor
LABEL maintainer="Data Ingestion Frontend"
LABEL description="Frontend React para visualización de datos Excel con 14 columnas"
LABEL version="1.0.0"

# Instalar curl para healthcheck
RUN apk add --no-cache curl

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm ci --only=production && npm cache clean --force

# Copiar código fuente
COPY . .

# Construir la aplicación
RUN npm run build

# Crear usuario no-root para seguridad
RUN addgroup -g 1001 -S nodejs && \
    adduser -S react -u 1001
RUN chown -R react:nodejs /app
USER react

# Exponer puerto
EXPOSE 3000

# Healthcheck para verificar que el frontend está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Variables de entorno
ENV NODE_ENV=production
ENV REACT_APP_API_URL=http://localhost:8000/api/v1

# Comando para ejecutar la aplicación
CMD ["npm", "start"]
