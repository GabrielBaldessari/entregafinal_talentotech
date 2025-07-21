import sqlite3
import colorama

# Activar colorama
colorama.init(autoreset=True)

# Conexión a la base de datos
conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT
)
""")
conexion.commit()

# Agregar producto
def registrar_producto():
    try:
        nombre = input("Nombre: ").strip()
        descripcion = input("Descripción: ").strip()
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        categoria = input("Categoría: ").strip()

        cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                       (nombre, descripcion, cantidad, precio, categoria))
        conexion.commit()
        print(colorama.Fore.GREEN + "Producto guardado.")
    except Exception as e:
        print(colorama.Fore.RED + f"Error al guardar: {e}")

# Ver todos los productos
def mostrar_productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    if productos:
        print(colorama.Fore.CYAN + "\nLista de productos:")
        for p in productos:
            print(f"ID: {p[0]} | Nombre: {p[1]} | Cantidad: {p[3]} | Precio: ${p[4]} | Categoría: {p[5]}")
    else:
        print(colorama.Fore.YELLOW + "No hay productos cargados.")

# Actualizar un producto
def actualizar_producto():
    try:
        id_prod = int(input("ID del producto a actualizar: "))
        nombre = input("Nuevo nombre: ")
        descripcion = input("Nueva descripción: ")
        cantidad = int(input("Nueva cantidad: "))
        precio = float(input("Nuevo precio: "))
        categoria = input("Nueva categoría: ")

        cursor.execute("""
            UPDATE productos 
            SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=?
            WHERE id=?
        """, (nombre, descripcion, cantidad, precio, categoria, id_prod))
        conexion.commit()

        if cursor.rowcount:
            print(colorama.Fore.GREEN + "Producto actualizado.")
        else:
            print(colorama.Fore.YELLOW + "No se encontró ese ID.")
    except Exception as e:
        print(colorama.Fore.RED + f"Error al actualizar: {e}")

# Eliminar producto
def eliminar_producto():
    try:
        id_prod = int(input("ID del producto a eliminar: "))
        cursor.execute("DELETE FROM productos WHERE id=?", (id_prod,))
        conexion.commit()

        if cursor.rowcount:
            print(colorama.Fore.GREEN + "Producto eliminado.")
        else:
            print(colorama.Fore.YELLOW + "No existe ese ID.")
    except Exception as e:
        print(colorama.Fore.RED + f"Error al eliminar: {e}")

# Buscar producto
def buscar_producto():
    print("Buscar por:")
    print("1. ID")
    print("2. Nombre")
    print("3. Categoría")
    opcion = input("Elegí una opción: ")

    if opcion == "1":
        valor = input("ID: ")
        cursor.execute("SELECT * FROM productos WHERE id=?", (valor,))
    elif opcion == "2":
        valor = input("Nombre: ").strip()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + valor + '%',))
    elif opcion == "3":
        valor = input("Categoría: ").strip()
        cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", ('%' + valor + '%',))
    else:
        print("Opción no válida.")
        return

    resultado = cursor.fetchall()
    if resultado:
        for p in resultado:
            print(f"ID: {p[0]} | Nombre: {p[1]} | Cantidad: {p[3]} | Precio: ${p[4]} | Categoría: {p[5]}")
    else:
        print(colorama.Fore.YELLOW + "No se encontraron productos.")

# Reporte de productos con poco stock
def reporte_stock_bajo():
    try:
        limite = int(input("Mostrar productos con cantidad menor o igual a: "))
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
        productos = cursor.fetchall()
        if productos:
            print(colorama.Fore.MAGENTA + "Productos con poco stock:")
            for p in productos:
                print(f"ID: {p[0]} | Nombre: {p[1]} | Cantidad: {p[3]}")
        else:
            print("No hay productos con tan poca cantidad.")
    except Exception as e:
        print(colorama.Fore.RED + f"Error al mostrar: {e}")

# Menú principal
def menu():
    while True:
        print("\n=== MENÚ ===")
        print("1. Agregar producto")
        print("2. Ver productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Ver productos con poco stock")
        print("7. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            reporte_stock_bajo()
        elif opcion == "7":
            print("Chau, gracias por usar el programa 👋")
            break
        else:
            print(colorama.Fore.RED + "Opción no válida.")

# Iniciar programa
if __name__ == "__main__":
    menu()
    conexion.close()

                
    