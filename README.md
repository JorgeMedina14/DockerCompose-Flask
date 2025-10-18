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

## Reflexión Técnica - Preguntas y Respuestas

### 1. ¿Por qué es mejor usar variables de entorno que hardcodear credenciales?

**🔐 Variables de Entorno (✅ Mejor práctica):**

**Ventajas de Seguridad:**
- **🔒 Protección de credenciales**: Las credenciales no quedan expuestas en el código fuente ni en repositorios
- **🔐 Gestión de secretos**: Facilita integración con sistemas como Azure Key Vault, AWS Secrets Manager, Docker Secrets
- **🔍 Auditoría mejorada**: Mejor control y rastreo de quién accede a qué recursos
- **👥 Trabajo en equipo**: Cada desarrollador puede usar sus propias credenciales sin conflictos

**Ventajas Operacionales:**
- **🌍 Flexibilidad multi-entorno**: Diferentes configuraciones por entorno (desarrollo, pruebas, producción)
- **♻️ Reutilización de código**: El mismo código funciona en múltiples entornos sin modificaciones
- **📋 Cumplimiento de estándares**: Sigue principios de 12-Factor App para aplicaciones modernas
- **🔄 CI/CD optimizado**: Facilita pipelines de integración y despliegue continuo

**❌ Credenciales Hardcodeadas (Mala práctica):**
- **⚠️ Riesgo de seguridad crítico**: Credenciales expuestas en repositorios públicos (GitHub, GitLab)
- **🔒 Inflexibilidad**: Requiere cambios de código para diferentes entornos
- **🔧 Mantenimiento complejo**: Difícil gestión en múltiples despliegues y equipos
- **📊 Problemas de auditoría**: Dificulta el rastreo de accesos y cumplimiento normativo
- **💼 Riesgos legales**: Posibles violaciones de normativas como GDPR, SOX, PCI-DSS

### 2. ¿Qué ventaja ofrece Docker Compose frente a ejecutar contenedores por separado?

**🎯 Docker Compose (✅ Recomendado):**

**Orquestación y Gestión:**
- **🎯 Orquestación simplificada**: Un solo comando (`docker compose up`) levanta toda la infraestructura
- **🔗 Gestión automática de dependencias**: Controla el orden de inicio de servicios con `depends_on`
- **🌐 Redes automáticas**: Comunicación segura entre contenedores sin configuración manual
- **💾 Gestión centralizada de volúmenes**: Persistencia de datos simplificada y coordinada

**Desarrollo y Operaciones:**
- **📝 Infraestructura como código**: Configuración declarativa y versionable en YAML
- **📈 Escalabilidad integrada**: Fácil replicación y escalado de servicios (`docker compose up --scale`)
- **🔄 Reproducibilidad garantizada**: Entornos idénticos en cualquier máquina
- **📋 Documentación integrada**: El archivo docker-compose.yml documenta toda la arquitectura

**Productividad:**
- **⚡ Desarrollo ágil**: Levantar/bajar stack completo en segundos
- **🐛 Debugging simplificado**: Logs centralizados con `docker compose logs`
- **🔄 Hot reload**: Fácil reinicio de servicios individuales

**❌ Contenedores por separado (Más complejo):**
- **⚙️ Configuración manual tediosa**: Múltiples comandos `docker run` con parámetros complejos
- **🌐 Gestión manual de redes**: Configuración manual de comunicación entre contenedores
- **🔄 Control manual de dependencias**: Manejo manual del orden de inicio y health checks
- **🐛 Propenso a errores**: Mayor probabilidad de errores de configuración y inconsistencias
- **📚 Documentación fragmentada**: Más difícil documentar y mantener la arquitectura completa
- **🔧 Escalado manual**: Configuración manual para réplicas y load balancing

### 3. ¿Qué sucede si eliminas el volumen db_data?

**🔥 Consecuencias Inmediatas:**

**Pérdida de Datos:**
- **💥 Pérdida total e irreversible**: Todos los mensajes almacenados se eliminarán permanentemente
- **🔄 Reset completo**: La base de datos PostgreSQL volverá a su estado inicial vacío
- **⚠️ Sin posibilidad de recuperación**: Los datos no se pueden recuperar una vez eliminado el volumen
- **🏗️ Recreación automática**: Docker creará un nuevo volumen vacío en el próximo `docker compose up`

**🎯 Casos de Uso Legítimos:**

**Desarrollo y Testing:**
- **🧹 Cleanup de desarrollo**: Limpiar completamente el entorno de desarrollo
- **🔄 Reset para testing**: Volver al estado inicial para pruebas automatizadas
- **🎭 Datos de prueba**: Restablecer datos de demo o testing

**Mantenimiento:**
- **�️ Cambio de esquema**: Reestructuración completa de la base de datos
- **🔧 Problemas de corrupción**: Resolver problemas de integridad de datos
- **📊 Migración de versiones**: Actualización mayor de PostgreSQL

**⚠️ Comandos y Alternativas:**

**Comando peligroso:**
```bash
# ⚠️ PELIGRO: Esto elimina TODOS los datos permanentemente
docker compose down -v
```

**Alternativas seguras:**
```bash
# Solo detener servicios (conservar datos)
docker compose down

# Crear backup antes de eliminar
docker compose exec db pg_dump -U admin mensajesdb > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar desde backup
docker compose exec -T db psql -U admin -d mensajesdb < backup_20241018_224500.sql

# Verificar volúmenes existentes
docker volume ls | grep docker-lab
```

**💡 Mejores Prácticas:**
- **📅 Backups regulares**: Programar backups automáticos en producción
- **🔄 Testing de restauración**: Probar regularmente la recuperación de backups
- **📊 Monitoreo de volúmenes**: Supervisar uso de espacio en volúmenes
- **🎯 Ambientes separados**: Usar volúmenes diferentes para dev/staging/prod

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