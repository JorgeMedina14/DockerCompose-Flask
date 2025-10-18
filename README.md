# Docker Lab - Aplicación Web Multi-Contenedor

## Descripción
Aplicación web multi-contenedor que incluye:
- **API Flask** (Python): Manejo de mensajes con endpoints REST
- **Base de datos PostgreSQL**: Almacenamiento persistente de datos
- **Docker Compose**: Orquestación de servicios

## Estructura del Proyecto
```
docker-lab/
├── app.py              # API Flask con endpoints
├── requirements.txt    # Dependencias de Python
├── Dockerfile         # Imagen de la aplicación Flask
├── docker-compose.yml # Orquestación de servicios
├── .dockerignore     # Archivos a ignorar en build
└── README.md         # Documentación
```

## Comandos de Operación

### 1. Construir y Levantar los Servicios
```bash
docker compose up -d
```

### 2. Verificar que los Contenedores están Ejecutándose
```bash
docker ps
```

### 3. Probar la Aplicación

#### Verificar conexión a la base de datos:
```bash
curl http://localhost:8080
```
**Respuesta esperada:** `App connected to PostgreSQL`

#### Añadir un mensaje:
```bash
curl -X POST "http://localhost:8080/add?texto=HolaDocker"
```
**Respuesta esperada:** `Message added: HolaDocker`

#### Añadir otro mensaje:
```bash
curl -X POST "http://localhost:8080/add?texto=Mensaje de prueba"
```

#### Listar todos los mensajes:
```bash
curl http://localhost:8080/list
```
**Respuesta esperada:** 
```json
{
  "mensajes": [
    {"id": 1, "texto": "HolaDocker"},
    {"id": 2, "texto": "Mensaje de prueba"}
  ]
}
```

### 4. Probar Persistencia de Datos

#### Detener los servicios:
```bash
docker compose down
```

#### Volver a levantar:
```bash
docker compose up -d
```

#### Verificar que los datos persisten:
```bash
curl http://localhost:8080/list
```
*Los mensajes anteriores deben seguir existiendo.*

### 5. Comandos Adicionales de Gestión

#### Ver logs de la aplicación:
```bash
docker compose logs app
```

#### Ver logs de la base de datos:
```bash
docker compose logs db
```

#### Detener servicios (conservando volúmenes):
```bash
docker compose down
```

#### Detener servicios y eliminar volúmenes:
```bash
docker compose down -v
```

#### Reconstruir imágenes:
```bash
docker compose up --build
```

## Arquitectura de la Solución

### Servicios
1. **flask-app**: Contenedor con la API Flask
   - Puerto expuesto: 8080 → 5000
   - Variables de entorno para conexión DB
   - Depende del servicio `db`

2. **postgres-db**: Contenedor con PostgreSQL 16
   - Base de datos: `mensajesdb`
   - Usuario: `admin`
   - Volumen persistente: `db_data`

### Red
- Red bridge personalizada `app-network` para comunicación segura entre contenedores

### Volúmenes
- `db_data`: Almacenamiento persistente de PostgreSQL en `/var/lib/postgresql/data`

## Endpoints de la API

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| GET | `/` | Verificar conexión DB | - |
| POST | `/add` | Añadir mensaje | `texto` (query param) |
| GET | `/list` | Listar mensajes | - |

## Reflexión Técnica

### 1. Ventajas de Variables de Entorno vs Credenciales Hardcodeadas

**Variables de Entorno:**
- ✅ **Seguridad**: Las credenciales no quedan expuestas en el código fuente
- ✅ **Flexibilidad**: Diferentes configuraciones por entorno (dev, staging, prod)
- ✅ **Reutilización**: El mismo código funciona en múltiples entornos
- ✅ **Buenas prácticas**: Cumple con principios de 12-factor app
- ✅ **Gestión de secretos**: Facilita integración con sistemas de gestión de secretos

**Credenciales Hardcodeadas:**
- ❌ **Riesgo de seguridad**: Credenciales expuestas en repositorios
- ❌ **Inflexibilidad**: Requiere cambios de código para diferentes entornos
- ❌ **Mantenimiento**: Difícil gestión cuando hay múltiples despliegues
- ❌ **Auditoría**: Dificulta el rastreo de accesos y cambios

### 2. Ventajas de Docker Compose vs Contenedores por Separado

**Docker Compose:**
- ✅ **Orquestación simplificada**: Un solo comando para levantar toda la infraestructura
- ✅ **Gestión de dependencias**: Controla el orden de inicio de servicios
- ✅ **Redes automáticas**: Comunicación segura entre contenedores
- ✅ **Configuración declarativa**: Infraestructura como código
- ✅ **Gestión de volúmenes**: Persistencia de datos simplificada
- ✅ **Escalabilidad**: Fácil replicación de servicios

**Contenedores por Separado:**
- ❌ **Complejidad**: Múltiples comandos docker run con configuración manual
- ❌ **Gestión de redes**: Configuración manual de comunicación entre contenedores
- ❌ **Dependencias**: Control manual del orden de inicio
- ❌ **Mantenimiento**: Mayor probabilidad de errores de configuración
- ❌ **Documentación**: Más difícil documentar la arquitectura completa

### 3. Implicaciones de Eliminar el Volumen db_data

**Consecuencias inmediatas:**
- 🔥 **Pérdida total de datos**: Todos los mensajes almacenados se eliminarán permanentemente
- 🔥 **Reset completo**: La base de datos volverá a su estado inicial vacío
- 🔥 **No reversible**: Los datos no se pueden recuperar una vez eliminado el volumen

**Cuándo sería necesario:**
- 🧹 **Cleanup completo**: Limpiar entorno de desarrollo
- 🔄 **Reset de testing**: Volver a estado inicial para pruebas
- 🗑️ **Cambio de esquema**: Reestructuración completa de la base de datos
- 💾 **Problemas de corrupción**: Resolver problemas de integridad de datos

**Comando para eliminar:**
```bash
# ⚠️ PELIGRO: Esto elimina TODOS los datos
docker compose down -v
```

**Alternativas seguras:**
```bash
# Solo detener servicios (conservar datos)
docker compose down

# Backup antes de eliminar
docker compose exec db pg_dump -U admin mensajesdb > backup.sql
```

## Buenas Prácticas Implementadas

1. **Seguridad**:
   - Variables de entorno para credenciales
   - Red aislada para comunicación entre contenedores
   - Usuario no-root en contenedores

2. **Mantenimiento**:
   - Código comentado y estructurado
   - Manejo de errores en conexiones DB
   - Logs informativos

3. **DevOps**:
   - `.dockerignore` para builds optimizados
   - Restart policies para alta disponibilidad
   - Separación de responsabilidades por contenedor

4. **Desarrollo**:
   - Estructura modular y reutilizable
   - Endpoints RESTful claros
   - Respuestas HTTP apropiadas

---

## Troubleshooting

### Si la aplicación no conecta a la base de datos:
```bash
# Verificar logs
docker compose logs app
docker compose logs db

# Verificar red
docker network ls
docker network inspect docker-lab_app-network
```

### Si PostgreSQL no inicia:
```bash
# Verificar permisos de volumen
docker volume inspect docker-lab_db_data

# Recrear volumen si es necesario
docker compose down -v
docker compose up -d
```