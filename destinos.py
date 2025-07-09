"""
Módulo: destinos.py

Este módulo forma parte del sistema SkyRoute S.A. y se encarga de la gestión de destinos
ofrecidos por la aerolínea. Las operaciones incluyen el registro de nuevos destinos, 
visualización de los existentes, modificación y eliminación de destinos.

Cada destino está asociado a una ciudad, y cada ciudad contiene datos como provincia, país y costo base.
Todas las operaciones se realizan a través de la base de datos mediante conexión SQL.
"""

from conexion_base_de_datos import obtener_conexion


def gestion_de_destinos():
    """
    Muestra un menú interactivo para gestionar destinos turísticos.

    Opciones disponibles:
    1. Registrar nuevo destino
    2. Listar destinos registrados
    3. Modificar destino existente
    4. Eliminar destino
    5. Salir del menú
    """
    while True:
        print("\nGESTIÓN DE DESTINOS")
        print("1. Registrar nuevo destino")
        print("2. Listar destinos")
        print("3. Modificar destino")
        print("4. Eliminar destino")
        print("5. Salir del menú de destinos")

        opcion = input("Selecciona una opción: ")

        try:
            if opcion == "1":
                registrar_destino()
            elif opcion == "2":
                listar_destinos()
            elif opcion == "3":
                modificar_destino()
            elif opcion == "4":
                eliminar_destino()
            elif opcion == "5":
                print("Saliendo del menú de gestión de destinos.")
                break
            else:
                print("Opción no válida.")
        except Exception as e:
            print(f"Error en la gestión de destinos: {e}")


def registrar_destino():
    """
    Registra un nuevo destino en la base de datos.

    - Solicita al usuario los datos de ciudad, provincia, país y costo base.
    - Verifica si la ciudad ya existe. Si no existe, la registra.
    - Registra el destino asociado a esa ciudad.
    """
    print("A continuación se muestra el formulario para agregar un destino.")

    nombre_ciudad = input("Ingrese el nombre del destino: ").strip().title()
    provincia = input("Ingrese la provincia de destino: ").strip().title()
    pais = input("Ingrese el país de destino: ").strip().title()
    precio = float(input("Ingrese el precio del destino: "))

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id_ciudad FROM ciudades 
            WHERE nombre_ciudad = %s AND provincia = %s AND pais = %s;
        """, (nombre_ciudad, provincia, pais))
        ciudad = cursor.fetchone()

        if ciudad:
            id_ciudad = ciudad[0]
            print("La ciudad ya estaba registrada. Se usará como parte del nuevo destino.")
        else:
            cursor.execute("""
                INSERT INTO ciudades (nombre_ciudad, provincia, pais, costo_base)
                VALUES (%s, %s, %s, %s);
            """, (nombre_ciudad, provincia, pais, precio))
            conexion.commit()
            cursor.execute("SELECT LAST_INSERT_ID();")
            id_ciudad = cursor.fetchone()[0]
            print("Ciudad registrada correctamente.")

        cursor.execute("INSERT INTO destinos (id_ciudad) VALUES (%s);", (id_ciudad,))
        conexion.commit()
        print("Destino registrado exitosamente.")

    except Exception as e:
        print(f"Error al registrar el destino: {e}")
    finally:
        cursor.close()
        conexion.close()


def listar_destinos():
    """
    Lista todos los destinos registrados en la base de datos, incluyendo:
    - ID del destino
    - Nombre de ciudad
    - Provincia
    - País
    - Costo base
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT destinos.id_destino, ciudades.nombre_ciudad, ciudades.provincia, ciudades.pais, ciudades.costo_base
            FROM destinos
            JOIN ciudades ON destinos.id_ciudad = ciudades.id_ciudad;
        """)
        destinos = cursor.fetchall()

        if destinos:
            print("Lista de destinos disponibles:")
            for destino in destinos:
                print(f"ID Destino: {destino[0]}, Ciudad: {destino[1]}, Provincia: {destino[2]}, País: {destino[3]}, Costo: {destino[4]}")
        else:
            print("No hay destinos registrados.")

    except Exception as e:
        print(f"Error al listar los destinos: {e}")
    finally:
        cursor.close()
        conexion.close()


def modificar_destino():
    """
    Permite modificar los datos de un destino existente.

    Pasos:
    - Muestra los destinos registrados.
    - Permite modificar ciudad, provincia, país o costo base.
    - Aplica el cambio sobre la ciudad asociada al destino.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT d.id_destino, c.nombre_ciudad, c.provincia, c.pais, c.costo_base
            FROM destinos d
            JOIN ciudades c ON d.id_ciudad = c.id_ciudad;
        """)
        destinos = cursor.fetchall()

        if not destinos:
            print("No hay destinos registrados.")
            return

        print("Lista de destinos:")
        for destino in destinos:
            print(f"ID Destino: {destino[0]}, Ciudad: {destino[1]}, Provincia: {destino[2]}, País: {destino[3]}, Costo: {destino[4]}")

        id_destino = int(input("Ingrese el ID del destino que desea modificar: "))

        cursor.execute("SELECT id_ciudad FROM destinos WHERE id_destino = %s;", (id_destino,))
        resultado = cursor.fetchone()

        if not resultado:
            print("No se encontró el destino.")
            return

        id_ciudad = resultado[0]

        modificar = input("¿Qué desea modificar: ciudad, provincia, país o costo base?: ").strip().lower()

        if modificar == "ciudad":
            ciudad = input("Ingresa el nuevo nombre de la ciudad: ").strip().title()
            cursor.execute("UPDATE ciudades SET nombre_ciudad = %s WHERE id_ciudad = %s;", (ciudad, id_ciudad))
        elif modificar == "provincia":
            provincia = input("Ingresa la nueva provincia: ").strip().title()
            cursor.execute("UPDATE ciudades SET provincia = %s WHERE id_ciudad = %s;", (provincia, id_ciudad))
        elif modificar in ["pais", "país"]:
            pais = input("Ingresa el nuevo país: ").strip().title()
            cursor.execute("UPDATE ciudades SET pais = %s WHERE id_ciudad = %s;", (pais, id_ciudad))
        elif modificar in ["costo base", "costo"]:
            costo_base = float(input("Ingresa el nuevo costo base: "))
            cursor.execute("UPDATE ciudades SET costo_base = %s WHERE id_ciudad = %s;", (costo_base, id_ciudad))
        else:
            print("Opción no válida.")
            return

        conexion.commit()
        print(f"Destino con ID {id_destino} modificado correctamente.")

    except Exception as e:
        print(f"Error al modificar el destino: {e}")
    finally:
        cursor.close()
        conexion.close()


def eliminar_destino():
    """
    Elimina un destino y su ciudad asociada de la base de datos.

    Pasos:
    - Muestra los destinos disponibles.
    - Solicita el ID del destino a eliminar.
    - Elimina primero el registro en la tabla 'destinos' y luego en 'ciudades'.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT d.id_destino, c.id_ciudad, c.nombre_ciudad, c.provincia, c.pais, c.costo_base
            FROM destinos d
            JOIN ciudades c ON d.id_ciudad = c.id_ciudad;
        """)
        destinos = cursor.fetchall()

        if not destinos:
            print("No hay destinos registrados.")
            return

        print("Lista de destinos:")
        for destino in destinos:
            print(f"ID Destino: {destino[0]}, Ciudad: {destino[2]}, Provincia: {destino[3]}, País: {destino[4]}, Costo: {destino[5]}")

        id_destino = int(input("Ingrese el ID del destino que desea eliminar: "))

        destino_seleccionado = next((d for d in destinos if d[0] == id_destino), None)

        if not destino_seleccionado:
            print("ID de destino no válido.")
            return

        id_ciudad = destino_seleccionado[1]

        cursor.execute("DELETE FROM destinos WHERE id_destino = %s;", (id_destino,))
        cursor.execute("DELETE FROM ciudades WHERE id_ciudad = %s;", (id_ciudad,))
        conexion.commit()

        print(f"Destino con ID {id_destino} eliminado correctamente.")

    except Exception as e:
        print(f"Error al eliminar el destino: {e}")
    finally:
        cursor.close()
        conexion.close()
