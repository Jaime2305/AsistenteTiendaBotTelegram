import json

class ProductDatabase:
    def __init__(self, datos="productos.json"):
        self.datos = datos
        self.productos = self.cargarProductos()

    def cargarProductos(self):
        with open(self.datos, "r", encoding="utf-8") as datos:
            return json.load(datos)


    def getProducto(self, texto_usuario):
        coincidencias = []
        palabras = texto_usuario.lower().split()

        for producto in self.productos:
         nombre_producto = producto["nombreProducto"].lower()

             # Si alguna palabra del usuario aparece en el nombre del producto
         if any(palabra in nombre_producto for palabra in palabras):
            coincidencias.append(producto)

        return coincidencias
       

    def getTodoProducto(self):
        return self.productos
