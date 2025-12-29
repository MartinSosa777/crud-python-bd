#CREAR UNA BASE DE DATOS INVENTARIO.DB CON ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA X
#REGISTRAR PRODUCTOS X
#VISUALIZAR DATOS X
# ACTUALIZAR DATOS X
# ELIMINAR DATOS POR ID X
# BUSQUEDA DE PRODUCTOS POR ID X
# REPORTE DE PRODUCTOS =< LIMITE DEL USUARIO
#INTERFAZ CON UN MENU PRINCIPAL X

import sqlite3
from colorama import Fore, init


#MOSTRAR PRODUCTOS
def mostrar_productos(con):
    sql_mostrar="SELECT * FROM inventario"
    try:
        cursor=con.cursor()
        cursor.execute(sql_mostrar)
        productos=cursor.fetchall()

        if not productos:
            print(Fore.RED + "No existen los productos en la tabla")
            init(autoreset=True)
        else:
            for prod in productos:
                print(prod)
        return productos
    
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al intentar mostrar los productos: {e}")
        init(autoreset=True)


#INSERTAR DATOS C
def crear_productos(con):
    nombre_producto=input("Ingresa el producto a agregar: ")
    descripcion_producto=input("Describi el producto deseado: ")
    cantidad_producto=int(input("Ingresa la cantidad del producto: "))
    precio_producto=float(input("Ingresa el precio del producto: "))
    categoria_producto=(input("Ingresa en que categoria entra el producto: "))
    productos=(nombre_producto,descripcion_producto,cantidad_producto,precio_producto,categoria_producto)
    sql_insertar="INSERT INTO inventario(nombre, descripcion, cantidad, precio, categoria) VALUES(?,?,?,?,?)"

    try:
        cursor=con.cursor()
        cursor.execute(sql_insertar,productos)
        con.commit()
        print(Fore.GREEN + "Producto agregado")
        init(autoreset=True)

    except sqlite3.Error as e:
        print(Fore.RED + f"Error al intentar crear un producto {e}")
        init(autoreset=True)



#LEER DATOS R
def buscar_producto(con):
    try:
        id_buscado = int(input("Ingresá el ID del producto que querés buscar: "))
        cursor = con.cursor()
        cursor.execute("SELECT * FROM inventario WHERE id = ?", (id_buscado,))
        producto = cursor.fetchone()

        if producto:
            print("Fore.GREEN + \nProducto encontrado:")
            init(autoreset=True)
            print(producto)
        else:
            print(Fore.RED +"No existe un producto con ese id.")
            init(autoreset=True)

    except ValueError:
        print(Fore.RED + "Ingresa un número valido.")
        init(autoreset=True)
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al buscar el producto: {e}")
        init(autoreset=True)

#ACTUALIZAR DATOS U
def actualizar_productos(con):
    try:
        id_actualizar = int(input("Ingresa el id del producto a actualizar: "))
        nuevo_precio = float(input("Ingresa el nuevo precio: "))
    except ValueError:
        print(Fore.RED + "Id o precio invalido.")
        init(autoreset=True)
        return

    producto_a_actualizar = "UPDATE inventario SET precio = ? WHERE id = ?"
    try:
        cursor = con.cursor()
        cursor.execute(producto_a_actualizar, (nuevo_precio, id_actualizar))
        con.commit()

        if cursor.rowcount > 0:
            print(Fore.GREEN +"Producto actualizado")
            init(autoreset=True)
        else:
            print(Fore.RED + "No se pudo actualizar el producto.")
            init(autoreset=True)

    except sqlite3.Error as e:
        print(Fore.RED + f"Error al intentar actualizar el producto: {e}")
        init(autoreset=True)
        
#ELiMINAR DATOS D    
def eliminar_productos(con):
    try:
        id_a_eliminar=int(input("Ingresa el id del producto a eliminar: "))
        
        producto_a_eliminar="DELETE FROM inventario WHERE id=?"
        cursor=con.cursor()
        cursor.execute(producto_a_eliminar,(id_a_eliminar,))
        con.commit()

        if cursor.rowcount > 0:
            print(Fore.GREEN + "Producto eliminado correctamente.")
            init(autoreset=True)
        else:
            print(Fore.RED + "No se pudo eliminar el producto.")
            init(autoreset=True)

    except ValueError:
        print(Fore.RED +"Ingresa un número valido.")
        init(autoreset=True)
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al intentar eliminar el producto: {e}")
        init(autoreset=True)

#GENERAR REPORTE
def reporte_productos(conexion):
    try:
        limite = int(input("Ingresá el límite de productos a mostrar: "))
        if limite <= 0:
            print(Fore.RED + "El límite debe ser mayor a 0.")
            init(autoreset=True)
            return
    except ValueError:
        print(Fore.RED + "Ingresa un número válido.")
        init(autoreset=True)
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM inventario LIMIT ?", (limite,))
        filas = cursor.fetchall()
        if not filas:
            print(Fore.RED + "No hay productos para mostrar.")
            init(autoreset=True)
            return
        print(f"Mostrando hasta {limite} productos:")
        for prod in filas:
            print(f"ID:{prod[0]} | {prod[1].title()} | {prod[2]} | Cant:{prod[3]} | ${prod[4]} | {prod[5]}")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al generar reporte: {e}")
        init(autoreset=True)

#CONEXION CON LA BASE DE DATOS
def crear_conexion(database):
    con=None

    try:
        con = sqlite3.connect(database)
        print(f"Conexion exitosa a {database}")
    except sqlite3.Error as e:
        print(f"Error al intentar conectar a {e}")
    
    return con

#CREACION DE LA TABLA
def crear_tabla(con):
    sql_crear_tabla="""
    CREATE TABLE IF NOT EXISTS inventario(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT
);
"""
    try:
        cursor=con.cursor()
        cursor.execute(sql_crear_tabla)
        con.commit()
        print("Tabla creada")

    except sqlite3.Error as e:
     print(f"Error al crear la tabla {e}") 
con = crear_conexion("./proyecto_final/inventario.db")
crear_tabla(con)

while True:
    print("¡Menu!")
    print("A. Buscar un producto")
    print("B. Agregar un producto")
    print("C. Eliminar un producto")
    print("D. Mostrar todos los productos")
    print("E. Actualizar un producto")
    print("F. Reporte de productos")
    print("X. Salir")

    opcion = input("Elegí una opción: ").upper()

    match opcion:
        case "A":
            buscar_producto(con)
        case "B":
            crear_productos(con)
        case "C":
            eliminar_productos(con)
        case "D":
            mostrar_productos(con)
        case "E":
            actualizar_productos(con)
        case "F":
            reporte_productos(con)
        case "X":
            print("Fin de la compra.")
            break
        case _:
            print("Opción incorrecta, intentá de nuevo.")








