"""
Módulo principal: main.py

Este archivo contiene la lógica principal de ejecución del sistema SkyRoute S.A.
Desde aquí se invocan los módulos encargados de la gestión de clientes, ventas y destinos.

Actúa como interfaz de usuario en consola, permitiendo la navegación por el sistema.
"""

from clientes import gestion_de_clientes, listado_clientes, agregar_cliente, modificar_cliente, eliminar_cliente
from destinos import gestion_de_destinos, registrar_destino, listar_destinos, modificar_destino, eliminar_destino
from ventas import gestion_de_ventas, agregar_venta, anular_venta
from conexion_base_de_datos import obtener_conexion


def main():
    """
    Función principal del sistema.

    Presenta un menú por consola con las siguientes opciones:
    1. Gestión de clientes (registro, edición, baja)
    2. Compra o anulación de tickets (ventas)
    3. Gestión de destinos (registro, listado, edición, eliminación)
    4. Salir del sistema

    Permanece en ejecución hasta que el usuario seleccione la opción de salida.
    """
    while True:
        print("MENU PRINCIPAL")
        print("1. Gestión de clientes")
        print("2. Compra, o anulación, de Tickets")
        print("3. Gestión de destinos")
        print("4. Salir.")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            gestion_de_clientes()
        elif opcion == "2":
            gestion_de_ventas()
        elif opcion == "3":
            gestion_de_destinos()
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
