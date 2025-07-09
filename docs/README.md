# SkyRoute S.A.

SkyRoute S.A. es un proyecto educativo interdisciplinario que integra contenidos de Programación y Bases de Datos. Se trata de un sistema de gestión de compras de una aerolínea internacional, diseñado para ejecutarse desde consola y demostrar la interconexión funcional entre módulos técnicos.

---

## Objetivo

El objetivo principal de SkyRoute es simular, mediante código Python y una base de datos MySQL, un sistema real de gestión de clientes, destinos y ventas de pasajes. La finalidad es aplicar conocimientos teóricos en un entorno práctico y cohesionado.

---

## Funcionalidades

- Registro y modificación de clientes.
- Asociación de múltiples teléfonos por cliente.
- Registro de ventas de tickets.
- Gestión de arrepentimientos de compra (anulación dentro de los 2 minutos).
- Administración de destinos nacionales e internacionales.
- Interacción directa con base de datos MySQL.

---

## Estructura de Carpetas

```
skyroute/
│
├── main.py
├── clientes.py
├── ventas.py
├── destinos.py
├── config.py
├── conexion_base_de_datos.py
│
├── base_de_datos/
│   ├── estructura_tablas.sql
│   └── modelo_entidad_relacion.png
│
├── docs/
│   └── documentacion_tecnica.pdf
│
├── diagrams/
│   ├── flujo_general.png
│   └── flujo_clientes.png
│
├── requirements.txt
└── README.md
```

---

## Requisitos del sistema

- Python 3.10 o superior
- MySQL Server (8.0 recomendado)
- Editor de código como VS Code o PyCharm

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecución

1. Tener el servidor MySQL activo.
2. Ejecutar el script `estructura_tablas.sql` dentro de tu gestor SQL para crear las tablas.
3. Ajustar los datos de conexión en `config.py` si es necesario.
4. Iniciar el programa con:

```bash
python main.py
```

---

## Base de Datos

El sistema está basado en una estructura relacional que incluye las siguientes tablas:

- `clientes`
- `telefonos`
- `ventas`
- `destinos`
- `ciudades`
- `arrepentimientos`

El diseño contempla integridad referencial, claves foráneas y normalización hasta 3FN.

---

## Casos de uso simples

### ✔ Registrar un cliente
- El sistema solicita nombre, apellido, DNI, email, dirección y teléfono.
- Valida formato de DNI (111.111.111), teléfono e email.
- Inserta datos en `clientes` y `telefonos`.

### ✔ Realizar una venta
- Selección de destino.
- Validación del cliente.
- Registro automático con fecha y cantidad de tickets.

### ✔ Anular una venta
- Solo posible dentro de los 2 minutos de realizada.
- Cambia estado a “Anulada” y guarda arrepentimiento.

---

## Licencia

Este proyecto es de uso educativo. Puede ser adaptado y reutilizado con fines didácticos.

---

## Autor

Desarrollado por **Juan Pablo Mercado**  
Técnicatura en Ciencia de Datos e Inteligencia Artificial  
Instituto Superior Politécnico Córdoba (ISPC) – 2025
