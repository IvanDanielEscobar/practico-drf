# Práctico 2 - Django REST Framework (DRF)

API REST desarrollada con Django y Django REST Framework para la gestión de órdenes de trabajo, clientes, técnicos y detalles de servicio.

En esta segunda entrega se incorporaron:
1. **Nuevo Modelo Relacionado**: `DetalleOrden`, con relación `ForeignKey` a `Orden`.
2. **Serializers Anidados (Nested Serializers)**: Serialización completa de `Cliente`, `Tecnico` y la lista de `DetalleOrden` dentro de cada `Orden` (lectura y creación/edición anidada).
3. **Vistas Basadas en Clases (CBV)**: Migración de las vistas previas a *Concrete Generic Views* (`generics.ListCreateAPIView` y `generics.RetrieveUpdateDestroyAPIView`) de DRF.

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

### 4. Ejecutar tests automatizados
```bash
uv run python src/manage.py test ordenes
```

### 5. Iniciar el servidor de desarrollo
```bash
uv run python src/manage.py runserver
```
El servidor estará accesible en `http://127.0.0.1:8000/`.

---

## 📌 Endpoints de la API

La URL base es `http://127.0.0.1:8000/api/`.

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| **GET** / **POST** | `/api/ordenes/` | Listar órdenes (con datos anidados) / Crear orden (soporta items anidados) |
| **GET** / **PUT** / **PATCH** / **DELETE** | `/api/ordenes/<id>/` | Ver detalle, actualizar o eliminar una orden |
| **GET** / **POST** | `/api/clientes/` | Listar y crear clientes |
| **GET** / **PUT** / **PATCH** / **DELETE** | `/api/clientes/<id>/` | Ver detalle (incluye sus órdenes), editar o borrar cliente |
| **GET** / **POST** | `/api/tecnicos/` | Listar y crear técnicos |
| **GET** / **PUT** / **PATCH** / **DELETE** | `/api/tecnicos/<id>/` | Ver detalle, editar o borrar técnico |
| **GET** / **POST** | `/api/detalles/` | Listar y crear detalles de órdenes directamente |
| **GET** / **PUT** / **PATCH** / **DELETE** | `/api/detalles/<id>/` | Ver detalle, editar o borrar un ítem individual |

---

## 📦 Ejemplo de Creación con Serializers Anidados

Petición `POST /api/ordenes/`:
```json
{
  "numeroOrden": 2001,
  "cliente_id": 1,
  "tecnico_id": 1,
  "direccion": "Bv. Chacabuco",
  "altura": 450,
  "tarea": "Instalación de fibra óptica y switches",
  "descripcion": "Instalación en planta alta",
  "estado": "PENDIENTE",
  "detalles": [
    {
      "descripcion": "Switch Gigabit 24 Puertos",
      "cantidad": 1,
      "precio_unitario": "185000.00"
    },
    {
      "descripcion": "Patchcord UTP 2m",
      "cantidad": 10,
      "precio_unitario": "3500.00"
    }
  ]
}
```

Respuesta `201 Created` recibida (con relaciones y subtotales calculados):
```json
{
  "id": 1,
  "numeroOrden": 2001,
  "cliente": {
    "id": 1,
    "nombre": "Empresa Alfa S.A.",
    "telefono": "3514001122",
    "email": "contacto@empresaalfa.com"
  },
  "tecnico": {
    "id": 1,
    "nombre": "Lucas Gomez",
    "categoria": "INSTALACIONES",
    "activo": true
  },
  "direccion": "Bv. Chacabuco",
  "altura": 450,
  "tarea": "Instalación de fibra óptica y switches",
  "descripcion": "Instalación en planta alta",
  "estado": "PENDIENTE",
  "detalles": [
    {
      "id": 1,
      "descripcion": "Switch Gigabit 24 Puertos",
      "cantidad": 1,
      "precio_unitario": "185000.00",
      "subtotal": "185000.00"
    },
    {
      "id": 2,
      "descripcion": "Patchcord UTP 2m",
      "cantidad": 10,
      "precio_unitario": "3500.00",
      "subtotal": "35000.00"
    }
  ],
  "timestamp": "2026-09-14T14:30:00Z",
  "updateTimestamp": "2026-09-14T14:30:00Z"
}
```

---

## 🧪 Pruebas con Clientes REST (Postman, Bruno, Thunder Client)

El repositorio incluye el archivo [`requests.http`](requests.http) con todas las peticiones listas para enviar:
- En **VS Code**: Instalar la extensión **Thunder Client** o **REST Client** y ejecutar directamente desde el archivo `requests.http`.
- En **Postman / Bruno**: Puedes importar el archivo `requests.http` o copiar los payloads y endpoints documentados arriba.