
# Diccionario de Datos — SkyRoute S.A.

##  Tabla: `clientes`

| Campo              | Tipo de dato   | PK  | FK  | Nulo | Valor por defecto | Descripción                                     |
|--------------------|----------------|-----|-----|------|-------------------|------------------------------------------------|
| id_cliente         | INT            | ✅  |     | ❌   | AUTO_INCREMENT    | Identificador único del cliente                |
| dni_cliente        | VARCHAR(50)    |     |     | ❌   |                   | Documento de identidad, valor único            |
| dir_cliente        | VARCHAR(50)    |     |     | ✅   |                   | Dirección del cliente                          |
| nombre_cliente     | VARCHAR(100)   |     |     | ❌   |                   | Nombre del cliente                             |
| apellido_cliente   | VARCHAR(100)   |     |     | ❌   |                   | Apellido del cliente                           |
| email_cliente      | VARCHAR(100)   |     |     | ✅   |                   | Correo electrónico del cliente                 |
| estado_de_cliente  | VARCHAR(10)    |     |     | ✅   | 'Activo'          | Estado lógico del cliente (Activo/Inactivo)    |

##  Tabla: `telefonos`

| Campo           | Tipo de dato   | PK  | FK  | Nulo | Valor por defecto | Descripción                                     |
|------------------|----------------|-----|-----|------|-------------------|------------------------------------------------|
| id_telefono      | INT            | ✅  |     | ❌   | AUTO_INCREMENT    | ID único por número de teléfono                |
| tel_cliente      | VARCHAR(50)    |     |     | ❌   |                   | Número de teléfono                             |
| dni_cliente      | VARCHAR(50)    |     | ✅  | ❌   |                   | Relacionado con el DNI del cliente             |

##  Tabla: `ciudades`

| Campo          | Tipo de dato   | PK  | FK  | Nulo | Valor por defecto | Descripción              |
|----------------|----------------|-----|-----|------|-------------------|--------------------------|
| id_ciudad      | INT            | ✅  |     | ❌   | AUTO_INCREMENT    | Identificador de ciudad  |
| nombre_ciudad  | VARCHAR(50)    |     |     | ❌   |                   | Nombre de la ciudad      |
| provincia      | VARCHAR(50)    |     |     | ✅   |                   | Provincia de la ciudad   |
| pais           | VARCHAR(50)    |     |     | ✅   |                   | País                     |
| costo_base     | FLOAT          |     |     | ✅   |                   | Costo asociado al destino|

##  Tabla: `destinos`

| Campo        | Tipo de dato   | PK  | FK  | Nulo | Valor por defecto | Descripción                            |
|--------------|----------------|-----|-----|------|-------------------|----------------------------------------|
| id_destino   | INT            | ✅  |     | ❌   | AUTO_INCREMENT    | Identificador del destino              |
| id_ciudad    | INT            |     | ✅  | ❌   |                   | Ciudad asociada al destino             |

##  Tabla: `ventas`

| Campo               | Tipo de dato   | PK  | FK  | Nulo | Valor por defecto | Descripción                                      |
|---------------------|----------------|-----|-----|------|-------------------|-------------------------------------------------|
| id_venta            | INT            | ✅  |     | ❌   | AUTO_INCREMENT    | Identificador único de la venta                 |
| fecha_de_compra     | DATETIME       |     |     | ❌   |                   | Fecha y hora en la que se realiza la venta      |
| id_destino          | INT            |     | ✅  | ❌   |                   | Destino adquirido en la venta                   |
| cantidad_de_tickets | INT            |     |     | ❌   |                   | Cantidad de pasajes comprados                   |
| estado_de_venta     | VARCHAR(10)    |     |     | ✅   | 'Activa'          | Estado lógico de la venta (Activa/Anulada)      |
| dni_cliente         | VARCHAR(50)    |     | ✅  | ❌   |                   | Cliente asociado a la venta                     |

## Tabla: `arrepentimientos`

| Campo                      | Tipo de dato   | PK  | FK  | Nulo | Valor por defecto | Descripción                                 |
|----------------------------|----------------|-----|-----|------|-------------------|---------------------------------------------|
| id_arrepentimiento         | INT            | ✅  |     | ❌   | AUTO_INCREMENT    | Identificador único del arrepentimiento     |
| fecha_hora_arrepentimiento| DATETIME       |     |     | ❌   |                   | Fecha y hora del arrepentimiento registrado |
| motivo_arrepentimiento     | TEXT           |     |     | ✅   |                   | Motivo escrito por el cliente               |
| id_venta                   | INT            |     | ✅  | ❌   |                   | Venta asociada al arrepentimiento           |
