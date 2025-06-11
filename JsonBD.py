import json
from datetime import datetime
import mysql.connector

def exportar_productos_a_json():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="124578",
        database="tienda"
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nombreProducto,descripcionProducto,precioProducto,empresaProducto,cantidadProducto FROM tienda.productos")
    productos = cursor.fetchall()

    for producto in productos:
        for key, value in producto.items():
            if isinstance(value, datetime):
                producto[key] = value.isoformat()



    with open("productos.json", "w", encoding="utf-8") as f:
        json.dump(productos, f, ensure_ascii=False, indent=4)

    cursor.close()
    conn.close()


exportar_productos_a_json()
