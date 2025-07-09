"""
Módulo: clientes.py

Este módulo forma parte del sistema SkyRoute S.A. y gestiona todas las operaciones relacionadas
con los clientes de la aerolínea. Permite registrar, modificar, listar, dar de baja y eliminar clientes
así como también asociar números de teléfono a cada uno de ellos.

Las operaciones se realizan mediante conexión a una base de datos relacional.
"""

import re
from conexion_base_de_datos import obtener_conexion


def gestion_de_clientes():
    """
    Muestra un menú interactivo para la gestión de clientes.

    Permite:
    1. Listar clientes registrados
    2. Agregar un nuevo cliente
    3. Modificar datos de un cliente
    4. Marcar a un cliente como 'Inactivo'
    5. Salir del menú

    Utiliza funciones auxiliares para cada operación específica.
    """
    while True:
        print("GESTION DE CLIENTES")
        print("1. Listado de clientes")
        print("2. Agregar cliente")
        print("3. Modificar cliente")
        print("4. Cambiar estado de cliente a 'Inactivo'")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        try:
            if opcion == "1":
                listado_clientes()
            elif opcion == "2":
                agregar_cliente()
            elif opcion == "3":
                modificar_cliente()
            elif opcion == "4":
                cambiar_estado_de_cliente()
            elif opcion == "5":
                print("Saliendo de la gestión de clientes.") 
                break
            else:
                print("Opción no válida. Por favor, selecciona una opción del 1 al 5.")
        except Exception as e:
            print(f"Error en la gestión de clientes: {e}")


def agregar_telefono():
    """
    Solicita y valida un número de teléfono en formato XXX-XXXXXXX.

    Retorna:
        str: Número de teléfono validado.
    """
    telefono = input("Ingrese el número de teléfono del cliente (formato XXX-XXXXXXX): ").strip()

    while True:
        if re.match(r'^\d{3}-\d{7}$', telefono):
            break
        print("Teléfono inválido. Debe ser en formato XXX-XXXXXXX")
        telefono = input("Ingrese el número de teléfono del cliente (formato XXX-XXXXXXX): ").strip()

    return telefono


def listado_clientes():
    """
    Consulta y muestra en consola la lista de clientes registrados,
    incluyendo su nombre, apellido, DNI, email, dirección, teléfono y estado.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    print("A continuación se muestra la lista de los clientes.")

    try:
        consulta = """SELECT c.nombre_cliente, c.apellido_cliente, c.dni_cliente, 
                             c.email_cliente, c.dir_cliente, t.tel_cliente, c.estado_de_cliente
                      FROM clientes c 
                      JOIN telefonos t ON c.dni_cliente = t.dni_cliente;"""
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        for cliente in resultado:
            print(f"Nombre: {cliente[0]}, Apellido: {cliente[1]}, DNI: {cliente[2]}, Email: {cliente[3]}, Dirección: {cliente[4]}, Teléfono: {cliente[5]}, Estado: {cliente[6]}")
    except Exception as e:
        print(f"Error al consultar los clientes: {e}")
    finally:
        cursor.close()
        conexion.close()


def agregar_cliente():
    """
    Solicita los datos de un nuevo cliente, valida el formato y lo registra en la base de datos.
    También solicita el número de teléfono y lo registra en la tabla correspondiente.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    print("A continuación se muestra el formulario para agregar un cliente.")

    nombre = input("Ingrese el nombre del cliente: ").strip().title()
    apellido = input("Ingrese el apellido del cliente: ").strip().title()
    direccion = input("Ingrese la dirección del cliente: ").strip().title()

    while True:
        email = input("Ingrese el email del cliente: ").strip().lower()
        if re.match(r'^\S+@\S+\.\S+$', email):
            break
        print("Email inválido. Formato esperado: ejemplo@correo.com")

    while True:
        dni = input("Ingrese el DNI del cliente (formato 111.111.111): ").strip()
        if re.match(r'^\d{3}\.\d{3}\.\d{3}$', dni):
            break
        print("DNI inválido. Debe ser en formato 111.111.111")

    try: 
        consulta = """
            INSERT INTO clientes (dni_cliente, dir_cliente, nombre_cliente, apellido_cliente, email_cliente)
            VALUES (%s, %s, %s, %s, %s);
        """
        valores = (dni, direccion, nombre, apellido, email)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Cliente agregado correctamente.")
        
        telefono = agregar_telefono()
        consulta_telefono = """
            INSERT INTO telefonos (tel_cliente, dni_cliente)
            VALUES (%s, %s);
        """
        cursor.execute(consulta_telefono, (telefono, dni))
        conexion.commit()
        print("Teléfono agregado correctamente.")

    except Exception as e:
        print(f"Error al agregar el cliente: {e}")
    finally:
        cursor.close()
        conexion.close()


def modificar_cliente():
    """
    Permite modificar los datos de un cliente existente en la base de datos.
    Se identifica al cliente por su DNI y se puede modificar nombre, apellido, email, dirección o DNI.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        dni_cliente = input("Ingrese el DNI del cliente que desea modificar (formato 111.111.111): ").strip()
        consulta = "SELECT * FROM clientes WHERE dni_cliente = %s;"
        cursor.execute(consulta, (dni_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            print("Cliente no encontrado.")
            return

        print(f"DNI: {cliente[1]}, Nombre: {cliente[3]}, Apellido: {cliente[4]}, Email: {cliente[5]}, Dirección: {cliente[2]}")
        modificar = input("Escribe el dato que deseas modificar: nombre, apellido, dni, email o dirección: ").lower()

        if modificar == "nombre":
            nuevo_nombre = input("Ingrese el nuevo nombre: ").strip().title()
            cursor.execute("UPDATE clientes SET nombre_cliente = %s WHERE dni_cliente = %s;", (nuevo_nombre, dni_cliente))

        elif modificar == "apellido":
            nuevo_apellido = input("Ingrese el nuevo apellido: ").strip().title()
            cursor.execute("UPDATE clientes SET apellido_cliente = %s WHERE dni_cliente = %s;", (nuevo_apellido, dni_cliente))

        elif modificar == "dni":
            while True:
                nuevo_dni = input("Ingrese el nuevo DNI (formato 111.111.111): ").strip()
                if re.match(r'^\d{3}\.\d{3}\.\d{3}$', nuevo_dni):
                    break
                print("DNI inválido. Intente nuevamente.")
            cursor.execute("UPDATE clientes SET dni_cliente = %s WHERE dni_cliente = %s;", (nuevo_dni, dni_cliente))

        elif modificar in ["email", "mail"]:
            while True:
                nuevo_email = input("Ingrese el nuevo email: ").strip().lower()
                if re.match(r'^\S+@\S+\.\S+$', nuevo_email):
                    break
                print("Email inválido. Intente nuevamente.")
            cursor.execute("UPDATE clientes SET email_cliente = %s WHERE dni_cliente = %s;", (nuevo_email, dni_cliente))

        elif modificar in ["dirección", "direccion"]:
            nueva_direccion = input("Ingrese la nueva dirección: ").strip().title()
            cursor.execute("UPDATE clientes SET dir_cliente = %s WHERE dni_cliente = %s;", (nueva_direccion, dni_cliente))

        else:
            print("Opción no válida.")
            return

        conexion.commit()
        print(f"El cliente con DNI {dni_cliente} ha sido modificado correctamente.")
        cursor.execute("SELECT * FROM clientes WHERE dni_cliente = %s;", (dni_cliente,))
        cliente_modificado = cursor.fetchone()
        print("Datos actualizados:")
        print(f"DNI: {cliente_modificado[1]}, Nombre: {cliente_modificado[3]}, Apellido: {cliente_modificado[4]}, Email: {cliente_modificado[5]}, Dirección: {cliente_modificado[2]}")

    except Exception as e:
        print(f"Error al modificar el cliente: {e}")
    finally:
        cursor.close()
        conexion.close()


def cambiar_estado_de_cliente():
    """
    Cambia el estado de un cliente a 'Inactivo', previa confirmación del usuario.
    Requiere el DNI del cliente para identificarlo en la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        dni_cliente = input("Ingrese el DNI del cliente que desea marcar como 'Inactivo': ")
        cursor.execute("SELECT * FROM clientes WHERE dni_cliente = %s;", (dni_cliente,))
        cursor.fetchone()

        if cursor.rowcount > 0:
            confirmar = input("¿Está seguro de que desea marcar este cliente como 'Inactivo'? (Si/No): ")
            if confirmar.lower() in ["s", "si"]:
                cursor.execute("SELECT id_cliente FROM clientes WHERE dni_cliente = %s;", (dni_cliente,))
                resultado = cursor.fetchone()
                if resultado:
                    id_cliente = resultado[0]
                    cursor.execute("UPDATE clientes SET estado_de_cliente = 'Inactivo' WHERE id_cliente = %s;", (id_cliente,))
                    conexion.commit()
                    print(f"El cliente con DNI {dni_cliente} ha sido marcado como 'Inactivo'.")
            else:
                print("Operación cancelada.")
        else:
            print("No se encontró un cliente con ese DNI.")

    except Exception as e:
        print(f"Error al cambiar el estado del cliente: {e}")
    finally:
        cursor.close()
        conexion.close()


def eliminar_cliente():
    """
    Elimina un cliente de la base de datos de forma definitiva.
    Solo se debe utilizar en casos especiales, bajo consentimiento explícito del cliente.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        dni_cliente = input("Ingrese el DNI del cliente que desea eliminar: ")
        cursor.execute("SELECT * FROM clientes WHERE dni_cliente = %s;", (dni_cliente,))
        cliente = cursor.fetchone()

        if cliente:
            print(f"DNI: {cliente[1]}, Nombre: {cliente[3]}, Apellido: {cliente[4]}, Email: {cliente[5]}, Dirección: {cliente[2]}")
            confirmar = input("¿Está seguro de que desea eliminar este cliente? (s/n): ")
            if confirmar.lower() in ["s", "si"]:
                cursor.execute("DELETE FROM clientes WHERE dni_cliente = %s;", (dni_cliente,))
                conexion.commit()
                print(f"El cliente con DNI {dni_cliente} ha sido eliminado correctamente.")
            else:
                print("Operación cancelada.")
        else:
            print("No se encontró un cliente con ese DNI.")

    except Exception as e:
        print(f"Error al eliminar el cliente: {e}")
    finally:
        cursor.close()
        conexion.close()
