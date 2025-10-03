# Instrucciones para usar PostgreSQL con Docker

## Archivos creados

1. **Dockerfile.postgres**: Dockerfile para crear la imagen de PostgreSQL con la base de datos UTN
2. **docker-compose.yml**: Configuración para levantar el contenedor fácilmente
3. **env_example.txt**: Actualizado con la nueva configuración de conexión

## Uso

### Opción 1: Con docker-compose (Recomendado)

```bash
# Levantar el contenedor PostgreSQL
docker-compose up -d postgres_utn

# Ver logs del contenedor
docker-compose logs postgres_utn

# Parar el contenedor
docker-compose down
```

### Opción 2: Con Docker directamente

```bash
# Construir la imagen
docker build -f Dockerfile.postgres -t postgres-utn .

# Ejecutar el contenedor
docker run -d \
  --name postgres_utn_db \
  -e POSTGRES_DB=UTN \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 55432:5432 \
  -v postgres_utn_data:/var/lib/postgresql/data \
  postgres-utn
```

## Conexión a la base de datos

- **Host**: localhost
- **Puerto**: 55432
- **Base de datos**: UTN
- **Usuario**: postgres
- **Contraseña**: postgres
- **URL de conexión**: `postgresql://postgres:postgres@localhost:55432/UTN`

## Para conectar desde tu aplicación FastAPI

Crea un archivo `.env` basado en `env_example.txt` y usa la URL de conexión proporcionada.
