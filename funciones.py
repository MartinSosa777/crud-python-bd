import sqlite3
from colorama import Fore, Back, init

#INSERTAR DATOS C
def crear_productos(conexion, producto):
    sql_insertar=f"INSERT INTO inventario(nombre, descripcion, cantidad, precio, categoria) VALUES(?,?,?,?,?)"
    try:
        cursor=conexion.cursor()
        cursor.execute(sql_insertar,producto)
        conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al intentar crear un registro {e}")


#LEER DATOS R
def buscar_producto(conexion):
    try:
        id_buscado = int(input("Ingresá el ID del producto que querés buscar: "))

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM inventario WHERE id = ?", (id_buscado,))
        producto = cursor.fetchone()

        if producto:
            print("\nProducto encontrado:")
            print(producto)
        else:
            print("No existe un producto con ese ID.")

    except ValueError:
        print("Debés ingresar un número.")
    except sqlite3.Error as e:
        print(f"Error al buscar producto: {e}")

#UPDATE U
def actualizar_productos(conexion, id_producto):
    sql="UPDATE inventario SET precio = ? WHERE id = ?"
    try:
        cursor=conexion.cursor()
        cursor.execute(sql,(id_producto))
        conexion.commit()
        if cursor.rowcount > 0:
            print(f"Producto actualizado")
        else:
            print(f"No se pudo actualizar el producto")

    except sqlite3.Error as e:
        print(f"Error al intentar mostrar los registros {e}")


#DELETE D
def eliminar_productos(conexion,id_producto):
    sql="DELETE FROM inventario WHERE id= ?"
    try:
        cursor=conexion.cursor()
        cursor.execute(sql,(id_producto,))
        if cursor.rowcount > 0:
            print(f"Producto eliminado")
        else:
            print(f"No se pudo eliminar el producto")

    except sqlite3.Error as e:
        print(f"Error al intentar mostrar los registros {e}")

#GENERAR REPORTE
def reporte_productos(conexion):
    try:
        limite = int(input("Ingresá el límite de productos a mostrar: "))
        if limite <= 0:
            print("El límite debe ser mayor a 0.")
            return
    except ValueError:
        print("Ingresa un número válido.")
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM inventario LIMIT ?", (limite,))
        filas = cursor.fetchall()
        if not filas:
            print("No hay productos para mostrar.")
            return
        print(f"Mostrando hasta {limite} productos:")
        for prod in filas:
            print(f"ID:{prod[0]} | {prod[1].title()} | {prod[2]} | Cant:{prod[3]} | ${prod[4]} | {prod[5]}")
    except sqlite3.Error as e:
        print(f"Error al generar reporte: {e}")