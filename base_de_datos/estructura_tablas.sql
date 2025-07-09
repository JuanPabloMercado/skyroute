-- Script consolidado de creación de base de datos: SkyRoute S.A.
-- Autor: Juan Pablo Mercado
-- Base de datos: prog_unidos

-- Crear y seleccionar base de datos
CREATE DATABASE IF NOT EXISTS prog_unidos;
USE prog_unidos;

-- Tabla CLIENTES
CREATE TABLE clientes ( 
    id_cliente INT NOT NULL AUTO_INCREMENT,
    dni_cliente VARCHAR(50) NOT NULL UNIQUE,
    dir_cliente VARCHAR(50),
    nombre_cliente VARCHAR(100),
    apellido_cliente VARCHAR(100),
    email_cliente VARCHAR(100),
    estado_de_cliente VARCHAR(10) DEFAULT 'Activo',
    PRIMARY KEY (id_cliente)
);

-- Tabla TELEFONOS
CREATE TABLE telefonos (
    id_telefono INT NOT NULL AUTO_INCREMENT,
    tel_cliente VARCHAR(50) NOT NULL,
    dni_cliente VARCHAR(50),
    PRIMARY KEY (id_telefono),
    CONSTRAINT fk_dni_cliente FOREIGN KEY (dni_cliente) REFERENCES clientes(dni_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabla CIUDADES
CREATE TABLE ciudades(
    id_ciudad INT NOT NULL AUTO_INCREMENT,
    nombre_ciudad VARCHAR(50) NOT NULL,
    provincia VARCHAR(50),
    pais VARCHAR(50),
    costo_base FLOAT,
    PRIMARY KEY (id_ciudad)
);

-- Tabla DESTINOS
CREATE TABLE destinos (
    id_destino INT NOT NULL AUTO_INCREMENT,
    id_ciudad INT NOT NULL,
    PRIMARY KEY (id_destino),
    FOREIGN KEY(id_ciudad) REFERENCES ciudades(id_ciudad)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabla VENTAS
CREATE TABLE ventas (
    id_venta INT NOT NULL AUTO_INCREMENT,
    fecha_de_compra DATETIME NOT NULL,
    id_destino INT NOT NULL,
    cantidad_de_tickets INT,
    estado_de_venta VARCHAR(10) DEFAULT 'Activa',
    dni_cliente VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_venta),
    FOREIGN KEY(id_destino) REFERENCES destinos(id_destino)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(dni_cliente) REFERENCES clientes(dni_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabla ARREPENTIMIENTOS
CREATE TABLE arrepentimientos (
    id_arrepentimiento INT NOT NULL AUTO_INCREMENT,
    fecha_hora_arrepentimiento DATETIME NOT NULL,
    motivo_arrepentimiento TEXT,
    id_venta INT NOT NULL,
    PRIMARY KEY (id_arrepentimiento),
    FOREIGN KEY(id_venta) REFERENCES ventas(id_venta)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
