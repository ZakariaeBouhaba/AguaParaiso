# AguaParaiso — SmartPark Pro

Sistema ERP para la gestion integral de un parque acuatico tematico.
Desarrollado como proyecto final del modulo de Programacion.

**Instituto Tecnologico Granada · 2026**
**Autor: Zakariae Bouhaba**

---

## Requisitos previos

- Python 3.10 o superior instalado
- Git instalado

---

## Instalacion paso a paso

### 1. Clonar el repositorio
```bash
git clone https://github.com/ZakariaeBouhaba/AguaParaiso.git
cd AguaParaiso
```

### 2. Solo en Windows — habilitar scripts
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Escribe S y pulsa Enter para confirmar.

### 3. Crear entorno virtual
```bash
python -m venv venv
```

### 4. Activar entorno virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 5. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 6. Inicializar base de datos (solo la primera vez)
```bash
python scripts/init_db.py
```

### 7. Ejecutar el sistema
```bash
python main.py
```

---

## Credenciales de acceso

| Usuario | Contrasena | Rol |
|---------|-----------|-----|
| admin | admin123 | Admin |
| maria.taquilla | admin123 | Taquillero |
| juan.taquilla | admin123 | Taquillero |
| antonio.tecnico | admin123 | Tecnico |
| roberto.camarero | admin123 | Camarero |
| alejandro.enfermero | admin123 | Enfermero |

---

## Arquitectura MVC

- `models/` — Clases Python con POO, herencia y encapsulamiento
- `controllers/` — Logica de negocio
- `views/` — Interfaz grafica CustomTkinter
- `database/` — Conexion SQLite3 con Singleton
- `utils/` — Logger, Security, Validators, Generators, EventsEngine
- `exceptions/` — Jerarquia de excepciones custom

---

## Base de datos

9 tablas SQLite3: zonas, atracciones, empleados, usuarios, visitantes, tickets, inventario, eventos, nominas

7 triggers automaticos para garantizar la consistencia del sistema.

---

## Modulos del sistema

- Login — Autenticacion con bcrypt, bloqueo tras 3 intentos
- Dashboard — Panel de control con resumen en tiempo real
- Taquilla — Venta de tickets con IVA 10% y localizador UUID
- Administrativo — RRHH, altas/bajas, nominas con IRPF
- Logistica — Control de inventario con alertas de stock
- Eventos — Motor de eventos aleatorios automatico cada 5 minutos
- Sanitario — Registro de incidentes sanitarios
- Zonas — Estado y aforo de las 6 zonas del parque
- Reporting — Estadisticas con JOINs, GROUP BY, SUM, AVG

---

## Stack tecnologico

| Tecnologia | Version | Uso |
|-----------|---------|-----|
| Python | 3.10+ | Lenguaje principal |
| CustomTkinter | 5.2.2 | Interfaz grafica |
| SQLite3 | Incluido | Base de datos |
| bcrypt | 5.0.0 | Hash de contrasenas |
| python-dotenv | 1.2.2 | Variables de entorno |
| pytest | 9.0.3 | Tests unitarios |
