-- ============================================
-- AguaParaíso - Schema SQL
-- Sistema ERP SmartPark Pro
-- ============================================

PRAGMA foreign_keys = ON;

-- ============================================
-- TABLA 1: ZONAS
-- ============================================
CREATE TABLE IF NOT EXISTS zonas (
    id_zona INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL CHECK(tipo IN ('Toboganes', 'Piscinas', 'RioLento', 'Restauracion', 'Servicios', 'VIP')),
    aforo_maximo INTEGER NOT NULL CHECK(aforo_maximo > 0),
    aforo_actual INTEGER NOT NULL DEFAULT 0 CHECK(aforo_actual >= 0),
    estado TEXT NOT NULL DEFAULT 'Abierta' CHECK(estado IN ('Abierta', 'Cerrada', 'Alerta')),
    hora_apertura TEXT NOT NULL,
    hora_cierre TEXT NOT NULL,
    fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    CHECK(aforo_actual <= aforo_maximo)
);

-- ============================================
-- TABLA 2: ATRACCIONES
-- ============================================
CREATE TABLE IF NOT EXISTS atracciones (
    id_atraccion INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('Adrenalina', 'Familia', 'Relax', 'Infantil')),
    altura_minima REAL NOT NULL DEFAULT 0.0 CHECK(altura_minima >= 0),
    aforo_maximo INTEGER NOT NULL CHECK(aforo_maximo > 0),
    estado TEXT NOT NULL DEFAULT 'Activa' CHECK(estado IN ('Activa', 'Cerrada', 'Mantenimiento')),
    id_zona INTEGER NOT NULL,
    fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (id_zona) REFERENCES zonas(id_zona) ON DELETE CASCADE
);

-- ============================================
-- TABLA 3: EMPLEADOS
-- ============================================
CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('Socorrista', 'Tecnico', 'Taquillero', 'Camarero', 'PersonalVIP', 'Vigilante', 'Limpiador', 'Administrativo', 'Enfermero')),
    categoria TEXT NOT NULL CHECK(categoria IN ('Junior', 'Senior', 'Jefe')),
    turno TEXT NOT NULL CHECK(turno IN ('Manana', 'Tarde', 'Mantenimiento')),
    estado TEXT NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo', 'Baja', 'Vacaciones')),
    id_zona INTEGER NOT NULL,
    sueldo_base REAL NOT NULL CHECK(sueldo_base > 0),
    fecha_alta TEXT NOT NULL DEFAULT (datetime('now')),
    contrato TEXT NOT NULL CHECK(contrato IN ('Fijo', 'Temporal')),
    FOREIGN KEY (id_zona) REFERENCES zonas(id_zona) ON DELETE RESTRICT
);

-- ============================================
-- TABLA 4: USUARIOS
-- ============================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('Admin', 'Encargado', 'Taquillero', 'Tecnico', 'Camarero', 'Enfermero')),
    id_empleado INTEGER NOT NULL UNIQUE,
    intentos_fallidos INTEGER NOT NULL DEFAULT 0 CHECK(intentos_fallidos >= 0),
    bloqueado INTEGER NOT NULL DEFAULT 0 CHECK(bloqueado IN (0, 1)),
    fecha_bloqueo TEXT,
    ultimo_acceso TEXT,
    fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
);

-- ============================================
-- TABLA 5: VISITANTES
-- ============================================
CREATE TABLE IF NOT EXISTS visitantes (
    id_visitante INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('Adulto', 'Nino', 'Residente')),
    fecha_visita TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================
-- TABLA 6: TICKETS
-- ============================================
CREATE TABLE IF NOT EXISTS tickets (
    id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
    localizador TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL CHECK(tipo IN ('Normal', 'Premium', 'TodoIncluido')),
    tipo_visitante TEXT NOT NULL CHECK(tipo_visitante IN ('Adulto', 'Nino', 'Residente')),
    precio_base REAL NOT NULL CHECK(precio_base > 0),
    iva REAL NOT NULL DEFAULT 10.0,
    precio_total REAL NOT NULL CHECK(precio_total > 0),
    fast_pass INTEGER NOT NULL DEFAULT 0 CHECK(fast_pass IN (0, 1)),
    fecha TEXT NOT NULL DEFAULT (datetime('now')),
    id_empleado INTEGER NOT NULL,
    id_visitante INTEGER,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE RESTRICT,
    FOREIGN KEY (id_visitante) REFERENCES visitantes(id_visitante) ON DELETE SET NULL
);

-- ============================================
-- TABLA 7: INVENTARIO
-- ============================================
CREATE TABLE IF NOT EXISTS inventario (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    id_zona INTEGER NOT NULL,
    stock_actual INTEGER NOT NULL DEFAULT 0 CHECK(stock_actual >= 0),
    stock_minimo INTEGER NOT NULL CHECK(stock_minimo > 0),
    precio_coste REAL NOT NULL CHECK(precio_coste > 0),
    precio_venta REAL NOT NULL CHECK(precio_venta > 0),
    proveedor TEXT NOT NULL,
    frecuencia_reposicion TEXT NOT NULL CHECK(frecuencia_reposicion IN ('Diario', 'Semanal', 'Mensual')),
    ultima_reposicion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    CHECK(precio_venta > precio_coste),
    FOREIGN KEY (id_zona) REFERENCES zonas(id_zona) ON DELETE RESTRICT
);

-- ============================================
-- TABLA 8: EVENTOS
-- ============================================
CREATE TABLE IF NOT EXISTS eventos (
    id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL CHECK(tipo IN ('Averia', 'Climatico', 'Sanitario', 'Stock', 'Aforo')),
    descripcion TEXT NOT NULL,
    id_zona INTEGER,
    estado TEXT NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo', 'Resuelto')),
    fecha_inicio TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_fin TEXT,
    id_empleado INTEGER,
    FOREIGN KEY (id_zona) REFERENCES zonas(id_zona) ON DELETE SET NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE SET NULL
);

-- ============================================
-- TABLA 9: NOMINAS
-- ============================================
CREATE TABLE IF NOT EXISTS nominas (
    id_nomina INTEGER PRIMARY KEY AUTOINCREMENT,
    id_empleado INTEGER NOT NULL,
    mes TEXT NOT NULL,
    sueldo_base REAL NOT NULL CHECK(sueldo_base > 0),
    horas_extra INTEGER NOT NULL DEFAULT 0 CHECK(horas_extra >= 0),
    bonus REAL NOT NULL DEFAULT 0.0 CHECK(bonus >= 0),
    descuentos REAL NOT NULL DEFAULT 0.0 CHECK(descuentos >= 0),
    irpf REAL NOT NULL CHECK(irpf > 0),
    tipo_contrato TEXT NOT NULL CHECK(tipo_contrato IN ('Fijo', 'Temporal')),
    total_neto REAL NOT NULL CHECK(total_neto > 0),
    fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE RESTRICT
);

-- ============================================
-- INDICES
-- ============================================
CREATE INDEX IF NOT EXISTS idx_atracciones_zona ON atracciones(id_zona);
CREATE INDEX IF NOT EXISTS idx_empleados_zona ON empleados(id_zona);
CREATE INDEX IF NOT EXISTS idx_tickets_fecha ON tickets(fecha);
CREATE INDEX IF NOT EXISTS idx_eventos_estado ON eventos(estado);
CREATE INDEX IF NOT EXISTS idx_inventario_zona ON inventario(id_zona);
CREATE INDEX IF NOT EXISTS idx_nominas_empleado ON nominas(id_empleado);