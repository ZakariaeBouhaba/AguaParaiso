-- ============================================
-- AguaParaíso - Triggers SQL
-- Sistema ERP SmartPark Pro
-- ============================================

PRAGMA foreign_keys = ON;

-- ============================================
-- TRIGGER 1: Venta de ticket → incrementar aforo de El Muelle
-- ============================================
CREATE TRIGGER IF NOT EXISTS tr_ticket_incrementar_aforo
AFTER INSERT ON tickets
BEGIN
    UPDATE zonas
    SET aforo_actual = aforo_actual + 1
    WHERE nombre = 'El Muelle';
END;

-- ============================================
-- TRIGGER 2: Aforo maximo alcanzado → estado Alerta + evento automatico
-- ============================================
CREATE TRIGGER IF NOT EXISTS tr_zona_aforo_alerta
AFTER UPDATE OF aforo_actual ON zonas
WHEN NEW.aforo_actual >= NEW.aforo_maximo
BEGIN
    UPDATE zonas
    SET estado = 'Alerta'
    WHERE id_zona = NEW.id_zona;
    INSERT INTO eventos (tipo, descripcion, id_zona, estado)
    VALUES (
        'Aforo',
        'Aforo maximo alcanzado en zona: ' || NEW.nombre,
        NEW.id_zona,
        'Activo'
    );
END;

-- ============================================
-- TRIGGER 3: Evento de Aforo resuelto → zona vuelve a Abierta
-- ============================================
CREATE TRIGGER IF NOT EXISTS tr_aforo_resuelto_zona_abierta
AFTER UPDATE OF estado ON eventos
WHEN NEW.estado = 'Resuelto' AND OLD.estado = 'Activo' AND NEW.tipo = 'Aforo'
BEGIN
    UPDATE zonas
    SET estado = 'Abierta',
        aforo_actual = 0
    WHERE id_zona = NEW.id_zona;
END;

-- ============================================
-- TRIGGER 4: Stock bajo minimo → evento automatico
-- ============================================
CREATE TRIGGER IF NOT EXISTS tr_stock_bajo_minimo
AFTER UPDATE OF stock_actual ON inventario
WHEN NEW.stock_actual < NEW.stock_minimo
BEGIN
    INSERT INTO eventos (tipo, descripcion, id_zona, estado)
    VALUES (
        'Stock',
        'Stock bajo minimo: ' || NEW.nombre || ' (' || NEW.stock_actual || ' unidades)',
        NEW.id_zona,
        'Activo'
    );
END;

-- ============================================
-- TRIGGER 5: 3 intentos fallidos → bloquear usuario 15 minutos
-- ============================================
CREATE TRIGGER IF NOT EXISTS tr_bloquear_usuario
AFTER UPDATE OF intentos_fallidos ON usuarios
WHEN NEW.intentos_fallidos >= 3
BEGIN
    UPDATE usuarios
    SET bloqueado = 1,
        fecha_bloqueo = datetime('now')
    WHERE id_usuario = NEW.id_usuario;
END;

-- ============================================
-- TRIGGER 6: Evento resuelto → registrar fecha_fin automaticamente
-- ============================================
CREATE TRIGGER IF NOT EXISTS tr_evento_resuelto
AFTER UPDATE OF estado ON eventos
WHEN NEW.estado = 'Resuelto' AND OLD.estado = 'Activo'
BEGIN
    UPDATE eventos
    SET fecha_fin = datetime('now')
    WHERE id_evento = NEW.id_evento;
END;

-- ============================================
-- TRIGGER 7: Ticket vendido → actualizar ultimo_acceso del taquillero
-- ============================================
CREATE TRIGGER IF NOT EXISTS tr_actualizar_ultimo_acceso
AFTER INSERT ON tickets
BEGIN
    UPDATE usuarios
    SET ultimo_acceso = datetime('now')
    WHERE id_empleado = NEW.id_empleado;
END;