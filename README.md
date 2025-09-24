# API de Objetos con FastAPI

Una API REST simple construida con FastAPI que administra una colección de objetos (teléfonos, tablets, laptops, etc.).

## Características

- Obtener todos los objetos o filtrar por IDs
- Obtener un objeto por ID
- Agregar nuevos objetos
- Eliminar objetos
- Documentación automática de la API
- Validación de peticiones/respuestas con Pydantic

## Instalación

1. Asegúrate de tener Python 3.7+ instalado
2. Instala FastAPI y Uvicorn:

```bash
pip install fastapi uvicorn
```

## Ejecutar la Aplicación

Iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs
- **Documentación Alternativa**: http://localhost:8000/redoc

## Endpoints de la API

### 1. Obtener Todos los Objetos

**GET** `/objects`

Devuelve todos los objetos en la colección.

```bash
curl http://localhost:8000/objects
```

### 2. Filtrar Objetos por IDs

**GET** `/objects?id=3&id=5&id=10`

Devuelve solo los objetos con los IDs especificados.

```bash
curl "http://localhost:8000/objects?id=3&id=5&id=10"
```

### 3. Obtener un Objeto Individual

**GET** `/objects/{object_id}`

Devuelve un objeto individual por ID.

```bash
curl http://localhost:8000/objects/7
```

**Respuesta (200 OK):**
```json
{
  "id": "7",
  "name": "Apple MacBook Pro 16",
  "data": {
    "year": 2019,
    "price": 1849.99,
    "CPU model": "Intel Core i9",
    "Hard disk size": "1 TB"
  }
}
```

**Respuesta de Error (404 Not Found):**
```json
{
  "detail": "Object with id '999' not found"
}
```

### 4. Agregar Nuevo Objeto

**POST** `/objects`

Crea un nuevo objeto en la colección.

**Cuerpo de la Petición:**
```json
{
  "name": "Samsung Galaxy S23",
  "data": {
    "color": "Phantom Black",
    "storage": "256 GB",
    "price": 799.99
  }
}
```

```bash
curl -X POST http://localhost:8000/objects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Samsung Galaxy S23",
    "data": {
      "color": "Phantom Black",
      "storage": "256 GB",
      "price": 799.99
    }
  }'
```

**Respuesta (201 Created):**
```json
{
  "id": "14",
  "name": "Samsung Galaxy S23",
  "data": {
    "color": "Phantom Black",
    "storage": "256 GB",
    "price": 799.99
  }
}
```

### 5. Eliminar Objeto

**DELETE** `/objects/{object_id}`

Elimina un objeto por ID.

```bash
curl -X DELETE http://localhost:8000/objects/7
```

**Respuesta:**
- **204 No Content** - Objeto eliminado exitosamente
- **404 Not Found** - Objeto no encontrado

## Datos de Ejemplo

La API viene pre-cargada con 13 objetos incluyendo:

- Google Pixel 6 Pro
- Apple iPhone 12 Mini, 256GB, Blue
- Apple iPhone 12 Pro Max
- Apple iPhone 11, 64GB
- Samsung Galaxy Z Fold2
- Apple AirPods
- Apple MacBook Pro 16
- Apple Watch Series 8
- Beats Studio3 Wireless
- Apple iPad Mini 5th Gen (2 variantes)
- Apple iPad Air (2 variantes)

## Estructura de Datos

Cada objeto tiene la siguiente estructura:

```json
{
  "id": "string",
  "name": "string",
  "data": {
    // Cualquier par clave-valor (opcional)
  }
}
```

El campo `data` es flexible y puede contener cualquier propiedad relevante al objeto.

## Manejo de Errores

La API devuelve códigos de estado HTTP apropiados:

- **200 OK** - Peticiones GET exitosas
- **201 Created** - Creación de objeto exitosa
- **204 No Content** - Eliminación exitosa
- **404 Not Found** - Objeto no encontrado
- **422 Unprocessable Entity** - Datos de petición inválidos

## Documentación Interactiva

FastAPI genera automáticamente documentación interactiva de la API. Visita:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Estas interfaces te permiten:
- Ver todos los endpoints disponibles
- Ver esquemas de peticiones/respuestas
- Probar la API directamente desde el navegador
- Descargar la especificación OpenAPI

## Desarrollo

### Estructura del Proyecto

```
clase1-fastapi/
├── main.py          # Aplicación FastAPI
├── README.md        # Este archivo
└── __pycache__/     # Archivos cache de Python
```

### Dependencias Principales

- **FastAPI** - Framework web moderno y rápido para APIs
- **Uvicorn** - Servidor ASGI para ejecutar FastAPI
- **Pydantic** - Validación de datos usando anotaciones de tipos de Python

### Agregar Nuevas Funcionalidades

La API está diseñada para ser fácilmente extensible. Para agregar nuevos endpoints:

1. Definir modelos Pydantic para validación de peticiones/respuestas
2. Agregar funciones de endpoint con decoradores apropiados
3. Incluir manejo de errores apropiado
4. Actualizar este README con documentación

## Licencia

Este es un proyecto de ejemplo con fines educativos.