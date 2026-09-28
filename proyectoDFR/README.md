# Práctico 3 - Django REST Framework (DRF)

API REST desarrollada con Django y Django REST Framework para la gestión de órdenes de trabajo, clientes, técnicos y detalles de servicio.

En esta tercera entrega se incorporaron:
1. **ViewSets**: Reemplazo de vistas *Concrete Generics* por ViewSets:
   - `OrdenViewSet`, `ClienteViewSet`, `DetalleOrdenViewSet` implementando `viewsets.ModelViewSet` (CRUD completo).
   - `TecnicoViewSet` implementando `viewsets.ReadOnlyModelViewSet` (solo lectura: `list` y `retrieve`, bloqueando escritura).
2. **Enrutamiento centralizado en `routers.py`**: Uso de `DefaultRouter` de DRF para generar y gestionar automáticamente los patrones de URL RESTful.
3. **Seguridad y Permisos (`permission_classes`)**: Configuración de `IsAuthenticatedOrReadOnly` en los ViewSets (lectura pública permitida, escritura restringida a usuarios autenticados).
4. **Autenticación con JWT (`djangorestframework-simplejwt`)**:
   - Endpoints `/api/token/` (login para obtener par de tokens access/refresh) y `/api/token/refresh/`.
   - Autenticación mediante cabecera HTTP: `Authorization: Bearer <access_token>`.
   - Soporte opcional de autenticación por sesión (`SessionAuthentication`) en `/api-auth/` para la interfaz navegable (Browsable API).

---

## 👥 Integrantes
- Escobar Iván
- Ibarra Matías

---

## 🛠️ Instalación y Ejecución con `uv`

Este proyecto utiliza [`uv`](https://docs.astral.sh/uv/) como gestor de paquetes y entornos virtuales.

### 1. Clonar el repositorio
```bash
git clone https://github.com/IvanDanielEscobar/practico-drf.git
cd practico-drf/proyectoDFR
```

### 2. Sincronizar el entorno de dependencias
```bash
uv sync
```

### 3. Aplicar migraciones a la base de datos
```bash
uv run python src/manage.py migrate
```

### 4. Crear un usuario para obtener tokens JWT
Para probar la autenticación y realizar operaciones de escritura (POST, PUT, DELETE), crea un superusuario o usuario:
```bash
uv run python src/manage.py createsuperuser
```

### 5. Iniciar el servidor de desarrollo
```bash
uv run python src/manage.py runserver
```
El servidor estará accesible en `http://127.0.0.1:8000/`.

---

## 🔐 Autenticación y Seguridad

### 1. Obtener Token JWT
Envía una petición `POST /api/token/` con las credenciales:
```json
{
  "username": "tu_usuario",
  "password": "tu_password"
}
```
Respuesta:
```json
{
  "refresh": "eyJhbGciOi...",
  "access": "eyJhbGciOi..."
}
```

### 2. Usar el Token en Peticiones Protegidas
Para crear, editar o eliminar recursos, incluye la cabecera:
```http
Authorization: Bearer <access_token>
```
Si la petición no incluye el token o es inválido, la API responderá con `401 Unauthorized`.

---

## 📌 Endpoints de la API

La URL base es `http://127.0.0.1:8000/api/`.

### Autenticación JWT
-| Método | Endpoint | Descripción |
-| **POST** | `/api/token/` | Obtener token de acceso y refresh (Login) |
-| **POST** | `/api/token/refresh/` | Renovar token de acceso expirado |

### Recursos gestionados por `routers.py`
-| Tipo de ViewSet | Método | Endpoint | Descripción | Permisos |
-| **ModelViewSet** | **GET** / **POST** | `/api/ordenes/` | Listar órdenes / Crear orden con detalles anidados | GET: Público / POST: Auth |
-| **ModelViewSet** | **GET** / **PUT** / **PATCH** / **DELETE** | `/api/ordenes/<id>/` | Ver detalle / Editar / Borrar orden | GET: Público / PUT, DELETE: Auth |
-| **ModelViewSet** | **GET** / **POST** | `/api/clientes/` | Listar y crear clientes | GET: Público / POST: Auth |
-| **ModelViewSet** | **GET** / **PUT** / **PATCH** / **DELETE** | `/api/clientes/<id>/` | Ver detalle (con órdenes) / Editar / Borrar | GET: Público / PUT, DELETE: Auth |
-| **ReadOnlyModelViewSet** | **GET** | `/api/tecnicos/` | Listado de técnicos catálogo | Público |
-| **ReadOnlyModelViewSet** | **GET** | `/api/tecnicos/<id>/` | Detalle del técnico | Público (POST/PUT/DELETE bloqueados: 405) |
-| **ModelViewSet** | **GET** / **POST** | `/api/detalles/` | Listar / Crear detalles de órdenes | GET: Público / POST: Auth |
-| **ModelViewSet** | **GET** / **PUT** / **PATCH** / **DELETE** | `/api/detalles/<id>/` | Ver / Editar / Borrar detalle puntual | GET: Público / PUT, DELETE: Auth |

---

## 🧪 Pruebas con Clientes REST (Postman, Bruno, Thunder Client)

El repositorio incluye el archivo [`requests.http`](requests.http) con todas las peticiones listas para enviar:
1. **Paso 1**: Ejecuta la petición `0.1 Obtener Token` enviando tus credenciales de usuario.
2. **Paso 2**: Realiza peticiones de lectura sin token para validar que responde `200 OK`.
3. **Paso 3**: Prueba enviar un `POST` sin token para comprobar que el sistema de permisos responde `401 Unauthorized`.
4. **Paso 4**: Realiza peticiones de creación y edición enviando la cabecera `Authorization: Bearer {{accessToken}}` para comprobar el éxito (`201 Created` / `200 OK`).
5. **Paso 5**: Prueba enviar un `POST` a `/api/tecnicos/` para comprobar que `ReadOnlyModelViewSet` devuelve `405 Method Not Allowed`.