DELIMITER //
CREATE TRIGGER insertar_productos
AFTER INSERT ON sistemaSolit_pedido
FOR EACH ROW
BEGIN
    DECLARE productos_id INT;
    DECLARE contador1 INT DEFAULT 0;
    
    -- Verifica si el producto ya existe
    SELECT id INTO productos_id 
    FROM sistemaSolit_productos 
    WHERE modelo = NEW.modelo;

    -- Si el producto no existe, inserta uno nuevo
    IF productos_id IS NULL THEN
        INSERT INTO sistemaSolit_productos (
            nombre_producto, marca, modelo, stock, observaciones, fecha_ingreso, 
            unidad_medida, empresa, proveedor, zona, stock_minimo, imgProducto, 
            categoria, fecha_actualizacion, automatico_insert
        ) VALUES (
            NULL, NULL, NEW.modelo, NEW.cantidad, NEW.nombre, CURRENT_DATE(), 
            NEW.unidad, NULL, NULL, NULL, NULL, NULL, NULL, CURRENT_DATE(), 1
        );
    ELSE
        -- Si el producto existe, actualiza el stock
        UPDATE sistemaSolit_productos 
        SET stock = stock + NEW.cantidad,
            fecha_actualizacion = CURRENT_DATE()
        WHERE id = productos_id;
    END IF;
    
    -- Maneja las inserciones en la tabla de carretes
    IF NEW.unidad = 'bobina' THEN
        IF NEW.nombre LIKE '%cable utp%' OR NEW.nombre LIKE '%carrete%' THEN
            WHILE contador1 < NEW.cantidad DO
                INSERT INTO sistemaSolit_carretes (
                    metraje_inicial, metraje_usado, id_producto_id, 
                    id_usuario_id, luegarDeUso, descripcion
                ) VALUES (
                    0, 0, productos_id, NULL, NULL, NEW.nombre
                );
                SET contador1 = contador1 + 1;
            END WHILE;
        END IF;
    ELSEIF NEW.unidad = 'kilometro' THEN
        IF NEW.nombre LIKE '%kilometro%' THEN
            INSERT INTO sistemaSolit_carretes (
                metraje_inicial, metraje_usado, id_producto_id, 
                id_usuario_id, luegarDeUso, descripcion
            ) VALUES (
                NEW.cantidad * 1000, 0, productos_id, NULL, NULL, NEW.nombre
            );
        END IF;
    END IF;    
END;
//
DELIMITER ;
---------------------------------------------------------------------------------------------------
DELIMITER //
CREATE TRIGGER update_producto
AFTER UPDATE ON sistemaSolit_productos
FOR EACH ROW
BEGIN
    DECLARE contador INT DEFAULT 0;
    DECLARE limite INT;

    -- Obtén el nuevo stock del producto
    SELECT stock INTO limite 
    FROM sistemaSolit_productos 
    WHERE id = NEW.id;

    -- Inserta registros individuales basados en la diferencia de stock
    WHILE contador < limite - OLD.stock DO
        INSERT INTO sistemaSolit_productosindividuales (
            nombre_producto_individual, status, id_producto_id
        ) VALUES (
            IFNULL(NEW.observaciones, 'Sin observaciones'), 1, NEW.id
        );
        SET contador = contador + 1;
    END WHILE;
END;
//
DELIMITER ;
---------------------------------------------------------------------------------------------------
DELIMITER //
CREATE TRIGGER crear_producto_individual
AFTER INSERT ON sistemaSolit_productos
FOR EACH ROW
BEGIN
    DECLARE contador INT DEFAULT 0;

    -- Inserta productos individuales basados en el valor de automatico_insert
    IF NEW.automatico_insert = 1 THEN
        WHILE contador < NEW.stock DO
            INSERT INTO sistemaSolit_productosindividuales (
                nombre_producto_individual, status, id_producto_id
            ) VALUES (
                IFNULL(NEW.observaciones, 'Sin observaciones'), 1, NEW.id
            );
            SET contador = contador + 1;
        END WHILE;
    ELSEIF NEW.automatico_insert = 0 THEN
        WHILE contador < NEW.stock DO
            INSERT INTO sistemaSolit_productosindividuales (
                nombre_producto_individual, status, id_producto_id
            ) VALUES (
                IFNULL(NEW.nombre_producto, 'Producto sin nombre'), 1, NEW.id
            );
            SET contador = contador + 1;
        END WHILE;
    END IF;
END;
//
DELIMITER ;
---------------------------------------------------------------------------------------------------



