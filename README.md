# 🌊 AguaParaíso — SmartPark Pro

Sistema ERP para la gestión integral de un parque acuático temático.
Desarrollado como proyecto final del módulo de Programación.

**Instituto Tecnológico Granada · 2026**
**Autor: Zakariae Bouhaba**

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio
```bash
git clone <url-repositorio>
cd AguaParaiso
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
```

### 5. Inicializar base de datos
```bash
python scripts/init_db.py
```

### 6. Ejecutar el sistema
```bash
python main.py
```

---

## 🔑 Credenciales de prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Admin |
| maria.taquilla | admin123 | Taquillero |
| juan.taquilla | admin123 | Taquillero |
| antonio.tecnico | admin123 | Tecnico |
| roberto.camarero | admin123 | Camarero |
| alejandro.enfermero | admin123 | Enfermero |

---

## 🏗️ Arquitectura

El sistema sigue el patrón **MVC** con separación total entre capas:

- `models/` — Clases Python con POO, herencia y encapsulamiento
- `controllers/` — Lógica de negocio
- `views/` — Interfaz gráfica CustomTkinter
- `database/` — Conexión SQLite3 con Singleton
- `utils/` — Logger, Security, Validators, Generators, EventsEngine
- `exceptions/` — Jerarquía de excepciones custom

---

## 🗄️ Base de datos

9 tablas SQLite3 con integridad referencial:
`zonas`, `atracciones`, `empleados`, `usuarios`, `visitantes`, `tickets`, `inventario`, `eventos`, `nominas`

7 triggers automáticos para garantizar la consistencia del sistema.

---

## 🎟️ Módulos del sistema

- **Login** — Autenticación con bcrypt, bloqueo tras 3 intentos
- **Dashboard** — Panel de control con resumen en tiempo real
- **Taquilla** — Venta de tickets con IVA 10% y localizador UUID
- **Administrativo** — RRHH, altas/bajas, cálculo de nóminas con IRPF
- **Logística** — Control de inventario con alertas de stock
- **Eventos** — Motor de eventos aleatorios con probabilidades
- **Sanitario** — Registro de incidentes sanitarios
- **Zonas** — Estado y aforo de las 6 zonas del parque
- **Reporting** — Estadísticas con JOINs, GROUP BY, SUM, AVG

---

## 📁 Estructura del proyecto


---

## ⚙️ Stack tecnológico

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| Python | 3.10+ | Lenguaje principal |
| CustomTkinter | 5.2.2 | Interfaz gráfica |
| SQLite3 | Incluido | Base de datos |
| bcrypt | 5.0.0 | Hash de contraseñas |
| python-dotenv | 1.2.2 | Variables de entorno |
| pytest | 9.0.3 | Tests unitarios |