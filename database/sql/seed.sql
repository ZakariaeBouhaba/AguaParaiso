-- ============================================
-- AguaParaíso - Seed SQL
-- Sistema ERP SmartPark Pro
-- Contraseña de todos los usuarios: admin123
-- ============================================

PRAGMA foreign_keys = ON;

-- ============================================
-- ZONAS
-- ============================================
INSERT INTO zonas (nombre, tipo, aforo_maximo, aforo_actual, estado, hora_apertura, hora_cierre) VALUES
('Cascada del Trueno', 'Toboganes', 200, 0, 'Abierta', '10:00', '19:00'),
('Laguna Cristal', 'Piscinas', 400, 0, 'Abierta', '10:00', '19:00'),
('Rio Oasis', 'RioLento', 120, 0, 'Abierta', '10:30', '18:30'),
('El Chiringuito', 'Restauracion', 100, 0, 'Abierta', '09:30', '19:30'),
('El Muelle', 'Servicios', 999, 0, 'Abierta', '09:00', '18:00'),
('Paradise Club', 'VIP', 50, 0, 'Abierta', '10:00', '19:00');

-- ============================================
-- ATRACCIONES
-- ============================================
INSERT INTO atracciones (nombre, tipo, altura_minima, aforo_maximo, estado, id_zona) VALUES
-- Cascada del Trueno (id_zona = 1)
('Rayo Negro', 'Adrenalina', 1.40, 20, 'Activa', 1),
('Caida Libre', 'Adrenalina', 1.35, 15, 'Activa', 1),
('Cascada Familiar', 'Familia', 1.10, 40, 'Activa', 1),
('Mini Splash', 'Infantil', 0.00, 30, 'Activa', 1),
-- Laguna Cristal (id_zona = 2)
('Piscina de Olas', 'Familia', 1.10, 200, 'Activa', 2),
('Laguna Olimpica', 'Relax', 0.00, 80, 'Activa', 2),
('Charco Infantil', 'Infantil', 0.00, 50, 'Activa', 2),
-- Rio Oasis (id_zona = 3)
('Rio Individual', 'Relax', 0.00, 60, 'Activa', 3),
('Rio Doble', 'Familia', 0.00, 30, 'Activa', 3),
-- Paradise Club (id_zona = 6)
('Cabana Privada', 'Relax', 0.00, 4, 'Activa', 6),
('Cama Balinesa', 'Relax', 0.00, 2, 'Activa', 6),
('Villa Privada', 'Relax', 0.00, 10, 'Activa', 6);

-- ============================================
-- EMPLEADOS
-- ============================================
INSERT INTO empleados (nombre, rol, categoria, turno, estado, id_zona, sueldo_base, contrato) VALUES
-- El Muelle (id_zona = 5)
('Carlos Garcia Lopez', 'Administrativo', 'Jefe', 'Manana', 'Activo', 5, 2000.00, 'Fijo'),
('Maria Martinez Ruiz', 'Taquillero', 'Senior', 'Manana', 'Activo', 5, 1200.00, 'Temporal'),
('Juan Fernandez Diaz', 'Taquillero', 'Junior', 'Tarde', 'Activo', 5, 1200.00, 'Temporal'),
('Ana Lopez Sanchez', 'Vigilante', 'Senior', 'Manana', 'Activo', 5, 1300.00, 'Fijo'),
-- Cascada del Trueno (id_zona = 1)
('Pedro Ramirez Torres', 'Socorrista', 'Senior', 'Manana', 'Activo', 1, 1400.00, 'Temporal'),
('Laura Gomez Jimenez', 'Socorrista', 'Junior', 'Tarde', 'Activo', 1, 1400.00, 'Temporal'),
('Antonio Moreno Vega', 'Tecnico', 'Senior', 'Manana', 'Activo', 1, 1800.00, 'Fijo'),
-- Laguna Cristal (id_zona = 2)
('Carmen Ruiz Molina', 'Socorrista', 'Senior', 'Manana', 'Activo', 2, 1400.00, 'Temporal'),
('Miguel Santos Ortega', 'Socorrista', 'Junior', 'Manana', 'Activo', 2, 1400.00, 'Temporal'),
('Sofia Herrera Blanco', 'Socorrista', 'Junior', 'Tarde', 'Activo', 2, 1400.00, 'Temporal'),
-- Rio Oasis (id_zona = 3)
('Diego Castro Romero', 'Socorrista', 'Junior', 'Manana', 'Activo', 3, 1400.00, 'Temporal'),
('Isabel Navarro Gil', 'Socorrista', 'Junior', 'Tarde', 'Activo', 3, 1400.00, 'Temporal'),
-- El Chiringuito (id_zona = 4)
('Roberto Serrano Paz', 'Camarero', 'Senior', 'Manana', 'Activo', 4, 1100.00, 'Temporal'),
('Elena Campos Reyes', 'Camarero', 'Junior', 'Tarde', 'Activo', 4, 1100.00, 'Temporal'),
-- Paradise Club (id_zona = 6)
('Francisco Ibañez Mora', 'PersonalVIP', 'Senior', 'Manana', 'Activo', 6, 1500.00, 'Temporal'),
('Patricia Delgado Cruz', 'Camarero', 'Senior', 'Manana', 'Activo', 6, 1100.00, 'Temporal'),
-- Sanitario y limpieza (id_zona = 5)
('Alejandro Rios Vidal', 'Enfermero', 'Senior', 'Manana', 'Activo', 5, 1900.00, 'Fijo'),
('Beatriz Fuentes Alba', 'Enfermero', 'Junior', 'Tarde', 'Activo', 5, 1900.00, 'Fijo'),
('Manuel Vargas Soto', 'Limpiador', 'Junior', 'Manana', 'Activo', 5, 1050.00, 'Fijo'),
('Rosa Medina Pardo', 'Limpiador', 'Junior', 'Tarde', 'Activo', 5, 1050.00, 'Fijo');

-- ============================================
-- USUARIOS
-- Contraseña de todos: admin123
-- ============================================
INSERT INTO usuarios (username, password_hash, rol, id_empleado) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4oZ.7sKG4K', 'Admin', 1),
('maria.taquilla', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4oZ.7sKG4K', 'Taquillero', 2),
('juan.taquilla', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4oZ.7sKG4K', 'Taquillero', 3),
('antonio.tecnico', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4oZ.7sKG4K', 'Tecnico', 7),
('roberto.camarero', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4oZ.7sKG4K', 'Camarero', 13),
('alejandro.enfermero', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4oZ.7sKG4K', 'Enfermero', 17);

-- ============================================
-- VISITANTES (7 dias de datos)
-- ============================================
INSERT INTO visitantes (nombre, tipo, fecha_visita) VALUES
-- Dia 1: 2025-07-15
('Luis Perez Garcia', 'Adulto', '2025-07-15 10:30:00'),
('Sara Perez Garcia', 'Nino', '2025-07-15 10:30:00'),
('Marcos Jimenez Lopez', 'Adulto', '2025-07-15 11:00:00'),
('Paula Jimenez Lopez', 'Adulto', '2025-07-15 11:00:00'),
('Tomas Ruiz Fernandez', 'Adulto', '2025-07-15 11:30:00'),
('Lucia Ruiz Fernandez', 'Nino', '2025-07-15 11:30:00'),
('Jorge Santos Martinez', 'Residente', '2025-07-15 12:00:00'),
('Clara Santos Martinez', 'Residente', '2025-07-15 12:00:00'),
('Alberto Gomez Torres', 'Adulto', '2025-07-15 12:30:00'),
('Nuria Gomez Torres', 'Nino', '2025-07-15 12:30:00'),
-- Dia 2: 2025-07-16
('Fernando Ortiz Vega', 'Adulto', '2025-07-16 10:00:00'),
('Monica Ortiz Vega', 'Adulto', '2025-07-16 10:00:00'),
('Hugo Blanco Soto', 'Nino', '2025-07-16 10:30:00'),
('Eva Blanco Soto', 'Nino', '2025-07-16 10:30:00'),
('Raul Morales Cruz', 'Residente', '2025-07-16 11:00:00'),
('Silvia Morales Cruz', 'Residente', '2025-07-16 11:00:00'),
('Victor Pena Rios', 'Adulto', '2025-07-16 11:30:00'),
('Cristina Pena Rios', 'Adulto', '2025-07-16 11:30:00'),
('Pablo Torres Vidal', 'Adulto', '2025-07-16 12:00:00'),
('Alicia Torres Vidal', 'Nino', '2025-07-16 12:00:00'),
-- Dia 3: 2025-07-17
('Sergio Molina Ramos', 'Adulto', '2025-07-17 10:00:00'),
('Diana Molina Ramos', 'Adulto', '2025-07-17 10:00:00'),
('Andres Castro Gil', 'Nino', '2025-07-17 10:30:00'),
('Irene Castro Gil', 'Nino', '2025-07-17 10:30:00'),
('Oscar Navarro Paz', 'Residente', '2025-07-17 11:00:00'),
('Marta Navarro Paz', 'Residente', '2025-07-17 11:00:00'),
('Javier Campos Alba', 'Adulto', '2025-07-17 11:30:00'),
('Natalia Campos Alba', 'Adulto', '2025-07-17 11:30:00'),
('Ruben Herrera Soto', 'Adulto', '2025-07-17 12:00:00'),
('Carmen Herrera Soto', 'Nino', '2025-07-17 12:00:00'),
-- Dia 4: 2025-07-18
('David Romero Cruz', 'Adulto', '2025-07-18 10:00:00'),
('Vanesa Romero Cruz', 'Adulto', '2025-07-18 10:00:00'),
('Adrian Serrano Gil', 'Nino', '2025-07-18 10:30:00'),
('Paula Serrano Gil', 'Nino', '2025-07-18 10:30:00'),
('Ignacio Vega Mora', 'Residente', '2025-07-18 11:00:00'),
('Pilar Vega Mora', 'Residente', '2025-07-18 11:00:00'),
('Hector Santos Rios', 'Adulto', '2025-07-18 11:30:00'),
('Leticia Santos Rios', 'Adulto', '2025-07-18 11:30:00'),
('Samuel Ortega Diaz', 'Adulto', '2025-07-18 12:00:00'),
('Julia Ortega Diaz', 'Nino', '2025-07-18 12:00:00'),
-- Dia 5: 2025-07-19
('Carlos Blanco Torres', 'Adulto', '2025-07-19 10:00:00'),
('Sofia Blanco Torres', 'Adulto', '2025-07-19 10:00:00'),
('Mario Reyes Vidal', 'Nino', '2025-07-19 10:30:00'),
('Ana Reyes Vidal', 'Nino', '2025-07-19 10:30:00'),
('Guillermo Pardo Cruz', 'Residente', '2025-07-19 11:00:00'),
('Rocio Pardo Cruz', 'Residente', '2025-07-19 11:00:00'),
('Alvaro Fuentes Paz', 'Adulto', '2025-07-19 11:30:00'),
('Elena Fuentes Paz', 'Adulto', '2025-07-19 11:30:00'),
-- Dia 6: 2025-07-20 (VIP)
('Ricardo Ibañez Mora', 'Adulto', '2025-07-20 10:00:00'),
('Beatriz Ibañez Mora', 'Adulto', '2025-07-20 10:00:00'),
('Lorenzo Delgado Ruiz', 'Adulto', '2025-07-20 10:30:00'),
('Claudia Delgado Ruiz', 'Adulto', '2025-07-20 10:30:00'),
-- Dia 7: 2025-07-21
('Nicolas Garcia Vega', 'Adulto', '2025-07-21 10:00:00'),
('Patricia Garcia Vega', 'Adulto', '2025-07-21 10:00:00'),
('Gonzalo Ruiz Blanco', 'Nino', '2025-07-21 10:30:00'),
('Daniela Ruiz Blanco', 'Nino', '2025-07-21 10:30:00'),
('Emilio Torres Soto', 'Residente', '2025-07-21 11:00:00'),
('Mercedes Torres Soto', 'Residente', '2025-07-21 11:00:00');

-- ============================================
-- TICKETS
-- Precios base:
-- Adulto Normal 25€ → total 27.50€
-- Nino Normal 15€ → total 16.50€
-- Adulto Premium 45€ → total 49.50€
-- Nino Premium 28€ → total 30.80€
-- Adulto TodoIncluido 65€ → total 71.50€
-- Nino TodoIncluido 40€ → total 44.00€
-- Residente Normal 18€ → total 19.80€
-- VIP Cabana 120€ → total 132.00€
-- VIP Villa 350€ → total 385.00€
-- Fast Pass añadido al precio base +28€
-- ============================================
INSERT INTO tickets (localizador, tipo, tipo_visitante, precio_base, iva, precio_total, fast_pass, fecha, id_empleado, id_visitante) VALUES
-- Dia 1
('AGP-2025-0001', 'Normal', 'Adulto', 25.00, 10.0, 27.50, 0, '2025-07-15 10:30:00', 2, 1),
('AGP-2025-0002', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-15 10:30:00', 2, 2),
('AGP-2025-0003', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-15 11:00:00', 2, 3),
('AGP-2025-0004', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-15 11:00:00', 2, 4),
('AGP-2025-0005', 'TodoIncluido', 'Adulto', 65.00, 10.0, 71.50, 1, '2025-07-15 11:30:00', 3, 5),
('AGP-2025-0006', 'TodoIncluido', 'Nino', 40.00, 10.0, 44.00, 1, '2025-07-15 11:30:00', 3, 6),
('AGP-2025-0007', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-15 12:00:00', 3, 7),
('AGP-2025-0008', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-15 12:00:00', 3, 8),
('AGP-2025-0009', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-15 12:30:00', 2, 9),
('AGP-2025-0010', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-15 12:30:00', 2, 10),
-- Dia 2
('AGP-2025-0011', 'TodoIncluido', 'Adulto', 65.00, 10.0, 71.50, 1, '2025-07-16 10:00:00', 2, 11),
('AGP-2025-0012', 'TodoIncluido', 'Adulto', 65.00, 10.0, 71.50, 1, '2025-07-16 10:00:00', 2, 12),
('AGP-2025-0013', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-16 10:30:00', 3, 13),
('AGP-2025-0014', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-16 10:30:00', 3, 14),
('AGP-2025-0015', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-16 11:00:00', 2, 15),
('AGP-2025-0016', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-16 11:00:00', 2, 16),
('AGP-2025-0017', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-16 11:30:00', 3, 17),
('AGP-2025-0018', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-16 11:30:00', 3, 18),
('AGP-2025-0019', 'Normal', 'Adulto', 25.00, 10.0, 27.50, 0, '2025-07-16 12:00:00', 2, 19),
('AGP-2025-0020', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-16 12:00:00', 2, 20),
-- Dia 3
('AGP-2025-0021', 'Normal', 'Adulto', 25.00, 10.0, 27.50, 0, '2025-07-17 10:00:00', 2, 21),
('AGP-2025-0022', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-17 10:00:00', 2, 22),
('AGP-2025-0023', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-17 10:30:00', 3, 23),
('AGP-2025-0024', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-17 10:30:00', 3, 24),
('AGP-2025-0025', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-17 11:00:00', 2, 25),
('AGP-2025-0026', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-17 11:00:00', 2, 26),
('AGP-2025-0027', 'TodoIncluido', 'Adulto', 65.00, 10.0, 71.50, 1, '2025-07-17 11:30:00', 3, 27),
('AGP-2025-0028', 'TodoIncluido', 'Adulto', 65.00, 10.0, 71.50, 1, '2025-07-17 11:30:00', 3, 28),
('AGP-2025-0029', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-17 12:00:00', 2, 29),
('AGP-2025-0030', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-17 12:00:00', 2, 30),
-- Dia 4
('AGP-2025-0031', 'Normal', 'Adulto', 25.00, 10.0, 27.50, 0, '2025-07-18 10:00:00', 2, 31),
('AGP-2025-0032', 'Normal', 'Adulto', 25.00, 10.0, 27.50, 0, '2025-07-18 10:00:00', 2, 32),
('AGP-2025-0033', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-18 10:30:00', 3, 33),
('AGP-2025-0034', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-18 10:30:00', 3, 34),
('AGP-2025-0035', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-18 11:00:00', 2, 35),
('AGP-2025-0036', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-18 11:00:00', 2, 36),
('AGP-2025-0037', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-18 11:30:00', 3, 37),
('AGP-2025-0038', 'TodoIncluido', 'Adulto', 65.00, 10.0, 71.50, 1, '2025-07-18 11:30:00', 3, 38),
('AGP-2025-0039', 'Normal', 'Adulto', 25.00, 10.0, 27.50, 0, '2025-07-18 12:00:00', 2, 39),
('AGP-2025-0040', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-18 12:00:00', 2, 40),
-- Dia 5
('AGP-2025-0041', 'TodoIncluido', 'Adulto', 65.00, 10.0, 71.50, 1, '2025-07-19 10:00:00', 2, 41),
('AGP-2025-0042', 'TodoIncluido', 'Adulto', 65.00, 10.0, 71.50, 1, '2025-07-19 10:00:00', 2, 42),
('AGP-2025-0043', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-19 10:30:00', 3, 43),
('AGP-2025-0044', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-19 10:30:00', 3, 44),
('AGP-2025-0045', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-19 11:00:00', 2, 45),
('AGP-2025-0046', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-19 11:00:00', 2, 46),
('AGP-2025-0047', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-19 11:30:00', 3, 47),
('AGP-2025-0048', 'Premium', 'Adulto', 45.00, 10.0, 49.50, 0, '2025-07-19 11:30:00', 3, 48),
-- Dia 6 VIP
('AGP-2025-0049', 'TodoIncluido', 'Adulto', 120.00, 10.0, 132.00, 1, '2025-07-20 10:00:00', 2, 49),
('AGP-2025-0050', 'TodoIncluido', 'Adulto', 120.00, 10.0, 132.00, 1, '2025-07-20 10:00:00', 2, 50),
('AGP-2025-0051', 'TodoIncluido', 'Adulto', 350.00, 10.0, 385.00, 1, '2025-07-20 10:30:00', 2, 51),
('AGP-2025-0052', 'TodoIncluido', 'Adulto', 350.00, 10.0, 385.00, 1, '2025-07-20 10:30:00', 2, 52),
-- Dia 7
('AGP-2025-0053', 'Normal', 'Adulto', 25.00, 10.0, 27.50, 0, '2025-07-21 10:00:00', 2, 53),
('AGP-2025-0054', 'Normal', 'Adulto', 25.00, 10.0, 27.50, 0, '2025-07-21 10:00:00', 2, 54),
('AGP-2025-0055', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-21 10:30:00', 3, 55),
('AGP-2025-0056', 'Normal', 'Nino', 15.00, 10.0, 16.50, 0, '2025-07-21 10:30:00', 3, 56),
('AGP-2025-0057', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-21 11:00:00', 2, 57),
('AGP-2025-0058', 'Normal', 'Residente', 18.00, 10.0, 19.80, 0, '2025-07-21 11:00:00', 2, 58);

-- ============================================
-- INVENTARIO
-- ============================================
INSERT INTO inventario (nombre, id_zona, stock_actual, stock_minimo, precio_coste, precio_venta, proveedor, frecuencia_reposicion) VALUES
-- Cascada del Trueno (id_zona = 1)
('Colchonetas', 1, 25, 20, 15.00, 20.00, 'AquaSupply S.L.', 'Semanal'),
('Cascos infantiles', 1, 35, 30, 10.00, 15.00, 'AquaSupply S.L.', 'Mensual'),
('Repuestos mecanicos', 1, 12, 10, 50.00, 75.00, 'TecnoAqua S.L.', 'Mensual'),
-- Laguna Cristal (id_zona = 2)
('Flotadores piscina', 2, 60, 50, 8.00, 12.00, 'AquaSupply S.L.', 'Semanal'),
('Chalecos salvavidas', 2, 45, 40, 25.00, 30.00, 'SafeWater S.L.', 'Mensual'),
('Producto de cloro', 2, 25, 20, 12.00, 18.00, 'ChemPark S.L.', 'Semanal'),
-- Rio Oasis (id_zona = 3)
('Flotadores individuales', 3, 70, 60, 8.00, 12.00, 'AquaSupply S.L.', 'Semanal'),
('Flotadores dobles', 3, 35, 30, 14.00, 20.00, 'AquaSupply S.L.', 'Semanal'),
-- El Chiringuito (id_zona = 4) — Agua botella con stock bajo minimo para probar trigger
('Agua botella', 4, 85, 100, 0.50, 2.50, 'Distribuciones Sol S.L.', 'Diario'),
('Refresco lata', 4, 120, 100, 1.00, 3.50, 'Distribuciones Sol S.L.', 'Diario'),
('Cerveza', 4, 100, 80, 1.20, 4.50, 'Distribuciones Sol S.L.', 'Diario'),
('Hamburguesa', 4, 60, 50, 3.00, 12.00, 'Distribuciones Sol S.L.', 'Diario'),
('Bocadillo', 4, 50, 40, 2.00, 7.00, 'Distribuciones Sol S.L.', 'Diario'),
('Helado', 4, 100, 80, 0.80, 3.50, 'IcePro S.L.', 'Diario'),
('Snack', 4, 80, 60, 0.50, 2.50, 'Distribuciones Sol S.L.', 'Diario'),
-- El Muelle (id_zona = 5)
('Toalla', 5, 120, 100, 5.00, 15.00, 'TextilPark S.L.', 'Semanal'),
('Crema solar', 5, 60, 50, 4.00, 12.00, 'SunCare S.L.', 'Semanal'),
('Banador', 5, 40, 30, 8.00, 35.00, 'AguaParaiso Merch', 'Mensual'),
('Souvenir pequeño', 5, 250, 200, 3.00, 10.00, 'AguaParaiso Merch', 'Mensual'),
('Souvenir grande', 5, 100, 80, 6.00, 18.00, 'AguaParaiso Merch', 'Mensual'),
-- Paradise Club (id_zona = 6)
('Bebida premium', 6, 60, 50, 8.00, 12.00, 'LuxDrinks S.L.', 'Diario'),
('Toalla VIP', 6, 35, 30, 12.00, 18.00, 'TextilPark S.L.', 'Semanal'),
('Amenities', 6, 50, 40, 6.00, 10.00, 'LuxCare S.L.', 'Semanal');

-- ============================================
-- EVENTOS
-- ============================================
INSERT INTO eventos (tipo, descripcion, id_zona, estado, fecha_inicio, fecha_fin, id_empleado) VALUES
('Averia', 'Fallo mecanico en Rayo Negro, requiere revision tecnica', 1, 'Resuelto', '2025-07-14 11:00:00', '2025-07-14 13:30:00', 7),
('Climatico', 'Tormenta leve, cierre temporal de zonas exteriores', NULL, 'Resuelto', '2025-07-13 16:00:00', '2025-07-13 17:30:00', 1),
('Stock', 'Stock bajo minimo: Agua botella (85 unidades)', 4, 'Resuelto', '2025-07-14 09:00:00', '2025-07-14 10:00:00', 1),
('Sanitario', 'Visitante con mareo leve atendido en enfermeria', NULL, 'Resuelto', '2025-07-14 14:00:00', '2025-07-14 14:30:00', 17),
('Averia', 'Fuga de agua en tuberia Rio Oasis', 3, 'Activo', '2025-07-15 09:30:00', NULL, 7),
('Stock', 'Stock bajo minimo: Agua botella (85 unidades)', 4, 'Activo', '2025-07-21 08:00:00', NULL, NULL),
('Climatico', 'Ola de calor extrema, protocolo de hidratacion activado', NULL, 'Activo', '2025-07-21 12:00:00', NULL, NULL),
('Sanitario', 'Visitante con golpe de calor atendido en enfermeria', NULL, 'Activo', '2025-07-21 13:30:00', NULL, 17);

-- ============================================
-- NOMINAS (junio y julio 2025)
-- Formula: total_neto = (sueldo_base + horas_extra*9 + bonus - descuentos) * (1 - irpf/100)
-- ============================================
INSERT INTO nominas (id_empleado, mes, sueldo_base, horas_extra, bonus, descuentos, irpf, tipo_contrato, total_neto) VALUES
-- Junio 2025
-- Carlos Admin Jefe: (2000 + 5*9 + 200) * 0.76 = 2245 * 0.76 = 1706.20
(1, '2025-06', 2000.00, 5, 200.00, 0.00, 24.0, 'Fijo', 1706.20),
-- Maria Taquillero Senior: (1200 + 0 + 200) * 0.85 = 1400 * 0.85 = 1190.00
(2, '2025-06', 1200.00, 0, 200.00, 0.00, 15.0, 'Temporal', 1190.00),
-- Juan Taquillero Junior: (1200 + 2*9 + 200) * 0.85 = 1418 * 0.85 = 1205.30
(3, '2025-06', 1200.00, 2, 200.00, 0.00, 15.0, 'Temporal', 1205.30),
-- Pedro Socorrista Senior: (1400 + 3*9 + 200) * 0.85 = 1627 * 0.85 = 1382.95
(5, '2025-06', 1400.00, 3, 200.00, 0.00, 15.0, 'Temporal', 1382.95),
-- Antonio Tecnico Senior: (1800 + 8*9 + 200) * 0.80 = 2072 * 0.80 = 1657.60
(7, '2025-06', 1800.00, 8, 200.00, 0.00, 20.0, 'Fijo', 1657.60),
-- Roberto Camarero Senior: (1100 + 0 + 200 - 50) * 0.85 = 1250 * 0.85 = 1062.50
(13, '2025-06', 1100.00, 0, 200.00, 50.00, 15.0, 'Temporal', 1062.50),
-- Francisco PersonalVIP Senior: (1500 + 0 + 200) * 0.80 = 1700 * 0.80 = 1360.00
(15, '2025-06', 1500.00, 0, 200.00, 0.00, 20.0, 'Temporal', 1360.00),
-- Alejandro Enfermero Senior: (1900 + 2*9 + 200) * 0.80 = 2118 * 0.80 = 1694.40
(17, '2025-06', 1900.00, 2, 200.00, 0.00, 20.0, 'Fijo', 1694.40),
-- Manuel Limpiador Junior: (1050 + 0 + 200) * 0.85 = 1250 * 0.85 = 1062.50
(19, '2025-06', 1050.00, 0, 200.00, 0.00, 15.0, 'Fijo', 1062.50),
-- Julio 2025
-- Carlos Admin Jefe: (2000 + 8*9 + 200) * 0.76 = 2272 * 0.76 = 1726.72
(1, '2025-07', 2000.00, 8, 200.00, 0.00, 24.0, 'Fijo', 1726.72),
-- Maria Taquillero Senior: (1200 + 4*9 + 200) * 0.85 = 1436 * 0.85 = 1220.60
(2, '2025-07', 1200.00, 4, 200.00, 0.00, 15.0, 'Temporal', 1220.60),
-- Juan Taquillero Junior: (1200 + 6*9 + 200) * 0.85 = 1454 * 0.85 = 1235.90
(3, '2025-07', 1200.00, 6, 200.00, 0.00, 15.0, 'Temporal', 1235.90),
-- Pedro Socorrista Senior: (1400 + 5*9 + 200) * 0.85 = 1645 * 0.85 = 1398.25
(5, '2025-07', 1400.00, 5, 200.00, 0.00, 15.0, 'Temporal', 1398.25),
-- Antonio Tecnico Senior: (1800 + 10*9 + 200) * 0.80 = 2090 * 0.80 = 1672.00
(7, '2025-07', 1800.00, 10, 200.00, 0.00, 20.0, 'Fijo', 1672.00),
-- Roberto Camarero Senior: (1100 + 2*9 + 200) * 0.85 = 1318 * 0.85 = 1120.30
(13, '2025-07', 1100.00, 2, 200.00, 0.00, 15.0, 'Temporal', 1120.30),
-- Francisco PersonalVIP Senior: (1500 + 3*9 + 200) * 0.80 = 1727 * 0.80 = 1381.60
(15, '2025-07', 1500.00, 3, 200.00, 0.00, 20.0, 'Temporal', 1381.60),
-- Alejandro Enfermero Senior: (1900 + 4*9 + 200) * 0.80 = 2136 * 0.80 = 1708.80
(17, '2025-07', 1900.00, 4, 200.00, 0.00, 20.0, 'Fijo', 1708.80),
-- Manuel Limpiador Junior: (1050 + 0 + 200) * 0.85 = 1250 * 0.85 = 1062.50
(19, '2025-07', 1050.00, 0, 200.00, 0.00, 15.0, 'Fijo', 1062.50);