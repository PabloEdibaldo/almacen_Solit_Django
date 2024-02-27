DELIMITER //
CREATE TRIGGER insertar_productos
AFTER INSERT ON sistemasolit_pedido
FOR EACH ROW
BEGIN
    DECLARE registro_id VARCHAR(250);
    SELECT id INTO registro_id FROM sistemasolit_productos WHERE nombre_producto = NEW.nombre;
    IF registro_id IS NULL THEN
        INSERT INTO sistemasolit_productos (id, nombre_producto, marca, modelo, stock, observaciones, fecha_ingreso, unidad_medida, empresa, proveedor, zona, stock_minimo)
        VALUES (NEW.id, NEW.nombre, NULL, NULL, NEW.cantidad, NULL, CURRENT_DATE, NULL, NULL, NULL, NULL, NULL);
    ELSE
        UPDATE sistemasolit_productos SET stock = stock + NEW.cantidad WHERE nombre_producto = NEW.nombre;
    END IF;
END;
//
DELIMITER ;
-------------------------------------------------------------------------------------------------------------------------
DELIMITER //
CREATE TRIGGER insert_producto_individual
AFTER INSERT ON sistemasolit_productos
FOR EACH ROW
BEGIN
DECLARE contador INT DEFAULT 0;
DECLARE limite INT;
SELECT stock INTO limite FROM sistemasolit_productos WHERE id = NEW.id;
WHILE contador < limite DO
INSERT INTO sistemasolit_productosindividuales (id, nombre_producto_individual, status, id_producto_id)
VALUES (NULL, NEW.nombre_producto, 1, NEW.id);
SET contador = contador + 1;
END WHILE;
END //
DELIMITER ;
-------------------------------------------------------------------------------------------------------------------------
DELIMITER //
CREATE TRIGGER update_producto
AFTER UPDATE ON sistemasolit_productos
FOR EACH ROW
BEGIN
DECLARE contador INT DEFAULT 0;
DECLARE limite INT;
SELECT stock INTO limite FROM sistemasolit_productos WHERE id = NEW.id;
    WHILE contador < limite - OLD.stock DO
    INSERT INTO sistemasolit_productosindividuales (id, nombre_producto_individual, status, id_producto_id)
    VALUES (NULL, NEW.nombre_producto, 1, NEW.id);
SET contador = contador + 1;
END WHILE;
END //
DELIMITER ;
-------------------------------------------------------------------------------------------------------------------------
DELIMITER //
CREATE TRIGGER delete_merma
AFTER DELETE ON sistemasolit_productosindividuales
FOR EACH ROW
BEGIN
    UPDATE sistemasolit_productos SET stock =  stock -1 WHERE id = OLD.id_producto_id;
END //
DELIMITER ;

-------------------------------------------------------------------------------------------------------------------------
DELIMITER //

CREATE TRIGGER actualizar_stock
AFTER UPDATE ON sistemasolit_reparto
FOR EACH ROW
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE total_productos INT;
    DECLARE producto_id VARCHAR(250);
    DECLARE cantidad INT;

    IF NEW.nombre_administrador IS NOT NULL THEN
        SET total_productos = JSON_LENGTH(JSON_EXTRACT(NEW.producto_cantidad, '$.productos'));

        WHILE i < total_productos DO
            SET producto_id = JSON_UNQUOTE(JSON_EXTRACT(NEW.producto_cantidad, CONCAT('$.productos[', i, '].nombre_producto')));
            SET cantidad = JSON_EXTRACT(NEW.producto_cantidad, CONCAT('$.productos[', i, '].cantidad'));


            UPDATE sistemasolit_productos
            SET stock = stock - cantidad
            WHERE nombre_producto = producto_id;

            SET i = i + 1;
        END WHILE;
    END IF;
END //

DELIMITER ;
----------------------------------------------------------------------------------------------------------------------------

DELIMITER //

CREATE TRIGGER insert_stock_minimo
AFTER UPDATE ON sistemasolit_productos
FOR EACH ROW
BEGIN
    DECLARE limite INT;
    SELECT stock_minimo INTO limite FROM sistemasolit_productos WHERE id=NEW.id ;

    IF NEW.stock <= limite AND limite IS NOT NULL THEN
        INSERT INTO sistemasolit_alerta (id, nombre_producto, stock_actual)
        VALUES(NULL, NEW.nombre_producto, NEW.stock);
    END IF;
END
//
DELIMITER ;
----------------------------------------------------------------------------------------------------------------------------
DELIMITER //

CREATE TRIGGER eliminar_alerta
AFTER UPDATE ON sistemasolit_productos
FOR EACH ROW
BEGIN
    DECLARE limite INT;
    DECLARE inicio INT;
    SELECT stock_minimo INTO limite FROM sistemasolit_productos WHERE id = NEW.id;
    SELECT stock INTO inicio FROM sistemasolit_productos WHERE id = NEW.id;
    IF inicio > limite AND limite IS NOT NULL THEN
        DELETE FROM sistemasolit_alerta WHERE nombre_producto = NEW.nombre_producto;
    END IF;
END //

DELIMITER ;
----------------------------------------------------------------------------------------------------------------------------
DELIMITER //

CREATE TRIGGER insert_carretes
AFTER INSERT ON sistemasolit_productosindividuales
FOR EACH ROW
BEGIN
    IF NEW.nombre_producto_individual LIKE '%carrete%' THEN
    INSERT INTO sistemasolit_carretes (id, metraje_inicial, metraje_usado, id_producto_individual_id, id_usuario_id)
    VALUES(NULL, 0, 0, NEW.id, NULL);
    END IF;
    END //
DELIMITER ;
----------------------------------------------------------------------------------------------------------------------------
DELIMITER //

CREATE TRIGGER delete_alertas
AFTER DELETE ON sistemasolit_productos
FOR EACH ROW
BEGIN
    DELETE FROM sistemasolit_alerta WHERE nombre_producto = OLD.nombre_producto;
END //

DELIMITER ;






