# 🌊 AguaParaíso — SmartPark Pro

🌐 [English](README.en.md) · **Español**

Sistema ERP de escritorio para la gestión integral de un parque acuático temático. Proyecto final del módulo de Programación en el Instituto Tecnológico de Granada (2026).

## Capturas

| Inicio de sesión | Panel de control |
|:-:|:-:|
| <img src="docs/screenshots/sp-login.jpg" width="320" alt="Pantalla de inicio de sesión"> | <img src="docs/screenshots/sp-dashboard.jpg" width="480" alt="Panel de control con eventos activos"> |

| Módulo de taquilla | Módulo de reporting |
|:-:|:-:|
| <img src="docs/screenshots/sp-taquilla.jpg" width="480" alt="Venta de tickets con IVA y localizador"> | <img src="docs/screenshots/sp-reporting.jpg" width="480" alt="Ganancias por tipo de ticket"> |

## Módulos del sistema

- **Login:** autenticación con bcrypt y bloqueo tras 3 intentos fallidos.
- **Dashboard:** panel de control con resumen en tiempo real.
- **Taquilla:** venta de tickets con IVA del 10 % y localizador UUID.
- **Administrativo:** recursos humanos, altas y bajas, y nóminas con IRPF.
- **Logística:** control de inventario con alertas de stock bajo.
- **Eventos:** motor de eventos aleatorios automático cada 5 minutos.
- **Sanitario:** registro de incidentes sanitarios.
- **Zonas:** estado y aforo de las 6 zonas del parque.
- **Reporting:** estadísticas con JOIN, GROUP BY, SUM y AVG.

## Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.10 o superior (probado con 3.14) | Lenguaje principal |
| CustomTkinter | 5.2.2 | Interfaz gráfica |
| SQLite3 | Incluido en Python | Base de datos |
| bcrypt | 5.0.0 | Cifrado de contraseñas |
| python-dotenv | 1.2.2 | Variables de entorno |
| pytest, pytest-cov | 9.0.3, 7.1.0 | Tests unitarios y cobertura |

## Arquitectura MVC

- `models/`: clases Python con POO, herencia y encapsulamiento.
- `controllers/`: lógica de negocio.
- `views/`: interfaz gráfica con CustomTkinter.
- `database/`: conexión SQLite3 con patrón Singleton, y scripts SQL (`schema.sql`, `triggers.sql`, `seed.sql`).
- `utils/`: logger, seguridad, validadores, generadores y motor de eventos.
- `exceptions/`: jerarquía de excepciones propias.
- `scripts/`: `init_db.py` (crea la base de datos con datos de ejemplo) y `reset_db.py` (la restablece).
- `tests/`: tests de modelos, controladores y base de datos.

## Base de datos

9 tablas SQLite3: `zonas`, `atracciones`, `empleados`, `usuarios`, `visitantes`, `tickets`, `inventario`, `eventos` y `nominas`, con 7 triggers automáticos que mantienen la consistencia de los datos.

## Puesta en marcha

### Requisitos
- Python 3.10 o superior
- Git

### 1. Clonar el repositorio
```bash
git clone https://github.com/ZakariaeBouhaba/AguaParaiso.git
cd AguaParaiso
```

### 2. Crear y activar el entorno virtual
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate
```
En Windows, si PowerShell bloquea los scripts: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Crear el archivo de configuración
```bash
cp .env.example .env        # En Windows: copy .env.example .env
```
Abre `.env` y cambia `SECRET_KEY` por un valor propio.

### 5. Inicializar la base de datos (solo la primera vez)
```bash
python scripts/init_db.py
```

### 6. Ejecutar el sistema
```bash
python main.py
```

## Credenciales de demostración

> ⚠️ Estas cuentas existen solo para probar la aplicación. No uses estas contraseñas en un entorno real.

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | admin123 | Admin |
| maria.taquilla | admin123 | Taquillero |
| juan.taquilla | admin123 | Taquillero |
| antonio.tecnico | admin123 | Técnico |
| roberto.camarero | admin123 | Camarero |
| alejandro.enfermero | admin123 | Enfermero |

## Tests

```bash
pytest
pytest --cov        # con informe de cobertura
```

## Documentación

- 📄 [Memoria técnica (PDF)](docs/memoria_tecnica_Zakariae_Bouhaba.pdf)
- 🗄️ [Diagrama de la base de datos](docs/diagrama_bd.png)
- 🧩 [Diagrama de clases](docs/diagrama_clases.png)
- 🔁 [Diagrama de flujo MVC](docs/diagrama_flujo_mvc.png)
- 🔁 [Diagrama de flujo de AguaParaíso (PDF)](docs/diagrama_flujo_aguaparaiso.drawio.pdf)

## Autor

**Zakariae Bouhaba** — Estudiante de Desarrollo de Aplicaciones Web (Granada, España)

[Portfolio](https://zakariaebouhaba.github.io) · [LinkedIn](https://www.linkedin.com/in/zakariae-bouhaba-02472b3ba/) · [GitHub](https://github.com/ZakariaeBouhaba)
