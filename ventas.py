"""
Módulo: ventas.py

Este módulo gestiona las operaciones de venta de pasajes dentro del sistema SkyRoute S.A.
Permite registrar nuevas ventas, anular ventas recientes, y listar ventas activas o anuladas
de acuerdo al cliente. También registra los arrepentimientos de compra asociados a anulaciones.

Cada operación se conecta a la base de datos relacional mediante el módulo de conexión.
"""

from datetime import datetime, timedelta
import re
from conexion_base_de_datos import obtener_conexion


def gestion_de_ventas():
    """
    Muestra un menú de opciones para gestionar ventas.

    Opciones disponibles:
    1. Agregar venta
    2. Anular venta (dentro de los 2 minutos desde la compra)
    3. Listar ventas activas o anuladas
    4. Salir del menú de ventas
    """
    while True: 
        print("GESTION DE VENTAS")
        print("1. Agregar venta")
        print("2. Anular venta")
        print("3. Listar ventas ")
        print("4. Salir")
        opcion = input("Selecciona una opción del 1 al 4: ")
   
        try:
            if opcion == "1":
                agregar_venta()
            elif opcion == "2":
                anular_venta()
            elif opcion == "3":
                listar_ventas()
            elif opcion == "4":
                print("Saliendo de la gestión de ventas.")
                return
            else:
                print("Opción no válida. Por favor, selecciona una opción del 1 al 4.")
        except Exception as e:
            print(f"Error en la gestión de ventas: {e}")


def agregar_venta():
    """
    Registra una nueva venta en el sistema.

    Pasos:
    - Muestra los destinos disponibles.
    - Solicita y valida el DNI del cliente.
    - Verifica que el cliente exista y esté activo.
    - Solicita la cantidad de tickets y el ID del destino.
    - Registra la venta en la base de datos.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        print("A continuación se muestra la lista de destinos y sus precios.")
        cursor.execute("""
            SELECT ciudades.nombre_ciudad AS Ciudad, ciudades.pais AS Pais, ciudades.costo_base AS Precio, destinos.id_destino 
            FROM destinos 
            JOIN ciudades ON ciudades.id_ciudad = destinos.id_ciudad;
        """)
        destinos = cursor.fetchall()
        for destino in destinos:
            print(f"ID Destino: {destino[3]}, Ciudad: {destino[0]}, País: {destino[1]}, Precio: {destino[2]}")

        if not destinos:
            print("\nNo hay destinos registrados.")
            return

        print("\nA continuación se muestra el formulario para agregar una venta.")

        while True:
            dni_cliente = input("Ingrese el DNI del cliente (formato 111.111.111): ")
            if re.match(r'^\d{3}\.\d{3}\.\d{3}$', dni_cliente):
                break
            print("DNI inválido. Debe ser en formato 111.111.111")

        cursor.execute("SELECT * FROM clientes WHERE dni_cliente = %s;", (dni_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            print("\nCliente no encontrado. Por favor, registre al cliente antes de agregar una venta.")
            return
        elif cliente[6] == "Inactivo":
            print("\nEl cliente está inactivo. No se puede realizar la venta.")
            return

        cantidad_de_tickets = int(input("\nIngrese la cantidad de tickets por comprar: "))
        id_destino = int(input("\nIngrese el ID del destino: "))

        cursor.execute("""
            INSERT INTO ventas (fecha_de_compra, id_destino, cantidad_de_tickets, dni_cliente)
            VALUES (NOW(), %s, %s, %s);
        """, (id_destino, cantidad_de_tickets, dni_cliente))
        conexion.commit()

        print("\nVenta agregada correctamente.")

    except Exception as e:
        print(f"\nError al agregar la venta: {e}")

    finally:
        cursor.close()
        conexion.close()


def anular_venta():
    """
    Permite anular una venta dentro de los primeros 2 minutos posteriores a su creación.

    Pasos:
    - Se solicitan el DNI y el ID de la venta.
    - Se verifica que la venta sea activa y reciente.
    - Se actualiza el estado de la venta a 'Anulada'.
    - Se registra el arrepentimiento en la tabla correspondiente.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        dni_cliente = input("Ingrese su DNI para verificar si tiene ventas activas (formato 111.111.111): ")
        cursor.execute("""
            SELECT id_venta, fecha_de_compra, id_destino, cantidad_de_tickets 
            FROM ventas 
            WHERE dni_cliente = %s AND estado_de_venta = 'Activa';
        """, (dni_cliente,))
        ventas_activas = cursor.fetchall()

        if not ventas_activas:
            print("No tiene ventas activas para anular.")
            return

        print("\nVentas activas:")
        for venta in ventas_activas:
            print(f"ID Venta: {venta[0]}, Fecha de Compra: {venta[1]}, ID Destino: {venta[2]}, Tickets: {venta[3]}")

        id_venta_anular = input("\nIngrese el ID de la venta que desea anular: ")

        venta_seleccionada = next((venta for venta in ventas_activas if str(venta[0]) == id_venta_anular), None)

        if not venta_seleccionada:
            print("ID de venta no válido.")
            return

        fecha_compra = venta_seleccionada[1]
        tiempo_transcurrido = datetime.now() - fecha_compra

        if tiempo_transcurrido > timedelta(minutes=2):
            print("No se puede anular la venta, han pasado más de 2 minutos desde su compra.")
            return

        cursor.execute("UPDATE ventas SET estado_de_venta = 'Anulada' WHERE id_venta = %s;", (id_venta_anular,))
        conexion.commit()
        print("Venta anulada correctamente.")

        motivo_arrepentimiento = input("Ingrese el motivo del arrepentimiento: ")
        cursor.execute("""
            INSERT INTO arrepentimientos (fecha_hora_arrepentimiento, motivo_arrepentimiento, id_venta)
            VALUES (NOW(), %s, %s);
        """, (motivo_arrepentimiento, id_venta_anular))
        conexion.commit()

    except Exception as e:
        print(f"Error al anular la venta: {e}")

    finally:
        cursor.close()
        conexion.close()


def listar_ventas():
    """
    Muestra un listado de las ventas activas o anuladas según indique el usuario.

    Pasos:
    - Solicita el DNI del cliente.
    - Solicita si desea ver ventas 'activas' o 'anuladas'.
    - Recupera y muestra las ventas correspondientes desde la base de datos.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        dni_cliente = input("Ingrese el DNI del cliente para listar sus ventas: ")
        opcion = input("¿Desea listar las ventas activas o anuladas?: ").strip().lower()

        if opcion in ["activa", "activas"]:
            cursor.execute("SELECT * FROM ventas WHERE estado_de_venta = 'Activa' AND dni_cliente = %s;", (dni_cliente,))
        elif opcion in ["anulada", "anuladas"]:
            cursor.execute("SELECT * FROM ventas WHERE estado_de_venta = 'Anulada' AND dni_cliente = %s;", (dni_cliente,))
        else:
            print("Opción no válida. Por favor, ingrese 'activa' o 'anulada'.")
            return

        ventas = cursor.fetchall()

        if not ventas:
            print(f"No hay ventas {opcion}.")
            return

        print(f"A continuación se muestran las ventas {opcion}:")
        for venta in ventas:
            print(f"ID Venta: {venta[0]}, Fecha de Compra: {venta[1]}, ID Destino: {venta[2]}, Cantidad de Tickets: {venta[3]}, Estado de venta: {venta[4]}, DNI Cliente: {venta[5]}")

    except Exception as e:
        print(f"Error al listar las ventas {opcion}: {e}")

    finally:
        cursor.close()
        conexion.close()
