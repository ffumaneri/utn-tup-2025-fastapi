# Trabajo Práctico: API CRUD de Ventas de Autos

## Programación IV - Universidad Tecnológica Nacional

---

## Objetivo

Desarrollar una API REST completa para la gestión de ventas de autos utilizando **FastAPI**, **SQLModel** y **PostgreSQL**. El sistema debe permitir administrar un inventario de autos y registrar las ventas realizadas, implementando todas las operaciones CRUD y aplicando patrones de diseño profesionales.

---

## Descripción del Dominio

El sistema debe gestionar dos entidades principales con una relación uno-a-muchos:

### Entidad: Auto
- **marca**: Marca del vehículo (ej: Toyota, Ford, Chevrolet)
- **modelo**: Modelo específico (ej: Corolla, Focus, Cruze)  
- **año**: Año de fabricación (entre 1900 y año actual)
- **numero_chasis**: Número único de identificación del chasis (alfanumérico, único en el sistema)

### Entidad: Venta
- **nombre_comprador**: Nombre completo del comprador
- **precio**: Precio de venta del vehículo
- **auto_id**: Referencia al auto vendido (clave foránea)
- **fecha_venta**: Fecha y hora de la venta

---

## Tecnologías Requeridas

- **FastAPI**: Framework web para crear la API REST
- **SQLModel**: ORM para interactuar con la base de datos
- **PostgreSQL**: Base de datos relacional
- **Pydantic**: Validación de datos y serialización

---

## Estructura del Proyecto

El proyecto debe organizarse con la siguiente estructura de archivos:

```
proyecto/
├── main.py              # Aplicación FastAPI principal
├── database.py          # Configuración de base de datos
├── models.py            # Modelos SQLModel
├── repository.py        # Patrón Repository para acceso a datos
├── autos.py            # Router de endpoints para autos
├── ventas.py           # Router de endpoints para ventas
├── requirements.txt     # Dependencias Python
└── README.md           # Documentación del proyecto
```

---

## Requerimientos Técnicos

### 1. Modelos de Datos (models.py)

Implementar los siguientes modelos usando **SQLModel**:

#### Para la entidad Auto:
- `AutoBase`: Modelo base con campos comunes
- `Auto`: Modelo de tabla con relaciones
- `AutoCreate`: Modelo para creación
- `AutoUpdate`: Modelo para actualizaciones parciales
- `AutoResponse`: Modelo para respuestas de API
- `AutoResponseWithVentas`: Modelo que incluye las ventas del auto

#### Para la entidad Venta:
- `VentaBase`: Modelo base con campos comunes
- `Venta`: Modelo de tabla con relaciones
- `VentaCreate`: Modelo para creación
- `VentaUpdate`: Modelo para actualizaciones parciales
- `VentaResponse`: Modelo para respuestas de API
- `VentaResponseWithAuto`: Modelo que incluye información del auto

#### Validaciones requeridas:
- **Auto**: Año entre 1900 y año actual, número de chasis único y alfanumérico
- **Venta**: Precio mayor a 0, nombre del comprador no vacío, fecha no futura

### 2. Configuración de Base de Datos (database.py)

- Configurar conexión a PostgreSQL usando variables de entorno
- Implementar función para crear tablas
- Configurar sesión de base de datos con generator pattern
- Incluir configuración de logging SQL (echo=True para desarrollo)

### 3. Patrón Repository (repository.py)

Implementar el patrón Repository con interfaces y clases concretas:

#### AutoRepository:
- `create(auto: AutoCreate) -> Auto`
- `get_by_id(auto_id: int) -> Optional[Auto]`
- `get_all(skip: int, limit: int) -> List[Auto]`
- `update(auto_id: int, auto_update: AutoUpdate) -> Optional[Auto]`
- `delete(auto_id: int) -> bool`
- `get_by_chasis(numero_chasis: str) -> Optional[Auto]`

#### VentaRepository:
- `create(venta: VentaCreate) -> Venta`
- `get_by_id(venta_id: int) -> Optional[Venta]`
- `get_all(skip: int, limit: int) -> List[Venta]`
- `update(venta_id: int, venta_update: VentaUpdate) -> Optional[Venta]`
- `delete(venta_id: int) -> bool`
- `get_by_auto_id(auto_id: int) -> List[Venta]`
- `get_by_comprador(nombre: str) -> List[Venta]`

### 4. Endpoints de API

#### Endpoints para Autos (/autos):
- `POST /autos` - Crear nuevo auto
- `GET /autos` - Listar autos con paginación
- `GET /autos/{auto_id}` - Obtener auto por ID
- `PUT /autos/{auto_id}` - Actualizar auto
- `DELETE /autos/{auto_id}` - Eliminar auto
- `GET /autos/chasis/{numero_chasis}` - Buscar por número de chasis
- `GET /autos/{auto_id}/with-ventas` - Auto con sus ventas

#### Endpoints para Ventas (/ventas):
- `POST /ventas` - Crear nueva venta
- `GET /ventas` - Listar ventas con paginación
- `GET /ventas/{venta_id}` - Obtener venta por ID
- `PUT /ventas/{venta_id}` - Actualizar venta
- `DELETE /ventas/{venta_id}` - Eliminar venta
- `GET /ventas/auto/{auto_id}` - Ventas de un auto específico
- `GET /ventas/comprador/{nombre}` - Ventas por nombre de comprador
- `GET /ventas/{venta_id}/with-auto` - Venta con información del auto

### 5. Características Técnicas Adicionales

#### Validaciones y Manejo de Errores:
- Validar que el auto existe antes de crear una venta
- Manejo apropiado de errores HTTP (400, 404, 422)
- Validaciones de integridad referencial
- Números de chasis únicos

#### Paginación:
- Implementar paginación en endpoints de listado
- Parámetros `skip` y `limit` con valores por defecto
- Validación de parámetros de paginación

#### Funcionalidades de Búsqueda:
- Búsqueda de autos por marca y modelo (parcial)
- Búsqueda de ventas por nombre de comprador
- Filtros por rango de fechas en ventas
- Filtros por rango de precios

#### Configuración de Base de Datos:
- Configurar PostgreSQL local o en servidor
- Variables de entorno para configuración
- Scripts de inicialización de base de datos

---

## Ejemplos de Uso de la API

### Crear un Auto:
```json
POST /autos
{
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "TOY2023COR123456"
}
```

### Crear una Venta:
```json
POST /ventas
{
    "nombre_comprador": "Juan Pérez",
    "precio": 25000.00,
    "auto_id": 1,
    "fecha_venta": "2024-03-15T10:30:00"
}
```

### Respuesta de Auto con Ventas:
```json
GET /autos/1/with-ventas
{
    "id": 1,
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "TOY2023COR123456",
    "ventas": [
        {
            "id": 1,
            "nombre_comprador": "Juan Pérez",
            "precio": 25000.00,
            "fecha_venta": "2024-03-15T10:30:00"
        }
    ]
}
```

---

## Criterios de Evaluación

### Funcionalidad (40 puntos)
- ✅ Todos los endpoints funcionan correctamente
- ✅ Operaciones CRUD completas para ambas entidades
- ✅ Validaciones de datos implementadas
- ✅ Relaciones entre entidades funcionando

### Arquitectura y Patrones (25 puntos)
- ✅ Implementación correcta del patrón Repository
- ✅ Separación adecuada de responsabilidades
- ✅ Uso correcto de dependency injection
- ✅ Estructura de archivos organizada

### Calidad del Código (20 puntos)
- ✅ Código limpio y bien documentado
- ✅ Manejo apropiado de errores
- ✅ Tipado correcto con Python typing
- ✅ Convenciones de nomenclatura

### Base de Datos (15 puntos)
- ✅ Configuración correcta de PostgreSQL
- ✅ Migraciones y creación de tablas
- ✅ Relaciones de base de datos implementadas
- ✅ Conexión y configuración funcionando

---

## Entregables

1. **Código fuente completo** con la estructura especificada
2. **Base de datos funcional** con PostgreSQL
3. **README.md** con instrucciones de instalación y ejecución
4. **Archivo requirements.txt** con todas las dependencias
5. **Documentación de API** (automática con FastAPI)

---

## Instrucciones de Desarrollo

### Configuración del Entorno:
1. Crear un entorno virtual Python
2. Instalar dependencias con `pip install -r requirements.txt`
3. Configurar PostgreSQL local (instalación nativa o servidor existente)
4. Crear la base de datos `autos_db`
5. Ejecutar la aplicación con `uvicorn main:app --reload`
6. Acceder a la documentación en `http://localhost:8000/docs`

### Variables de Entorno:
```bash
DATABASE_URL=postgresql://usuario:password@localhost:5432/autos_db
```

### Comandos Útiles:
```bash
# Ejecutar aplicación en modo desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Verificar conexión a PostgreSQL
psql -h localhost -p 5432 -U usuario -d autos_db
```

---

## Notas Importantes

- **Seguridad**: Implementar validaciones robustas en todos los endpoints
- **Performance**: Usar paginación en listados grandes
- **Mantenibilidad**: Seguir principios SOLID en el diseño
- **Documentación**: FastAPI genera documentación automática, pero agregar comentarios en el código

---

## Recursos de Apoyo

- [Documentación oficial de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de SQLModel](https://sqlmodel.tiangolo.com/)
- [Documentación oficial de PostgreSQL](https://www.postgresql.org/docs/)

---

**¡Éxitos en el desarrollo!** 🚗💻

