from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from Producto_Datos import ProductDatabase
from Gemini_API import GeminiChat
from delay import Delay
from historialChats.history import History
import time

db = ProductDatabase()
ai = GeminiChat()
peticiones= Delay()
contextoHistorial = History()


VALID_KEYWORDS = ["hola","buenas","buen","quetal","precio", "disponible", "tiene", "para qué sirve", "cómo lo uso", "cómo se usa","hay disponible","vale","cuesta","otra igual","otra",  "cuánto cuesta",
    "qué vale",
    "me interesa",
    "puedo comprar",
    "quiero saber",
    "dame info",
    "quiero ver",
    "cómo funciona",
    "funciona para",
    "sirve para",
    "hay stock",
    "hay existencias",
    "me puedes decir",
    "qué incluye",
    "qué trae",
    "con qué viene",
    "está disponible",
    "en existencia",
    "cuál es el precio",
    "tienes",
    "tendrás",
    "se puede usar para",
    "acepta",
    "es compatible con",
    "qué características",
    "detalles del producto",
    "hay",
    "que tiene",
    "que incluye",
    "que trae",
    "que es",
    "que es compatible con",
    "que acepta",
    "ese"
    "aparato",
    "artículo",
    "producto",
    "sirve",
    "funciona",
    "funcionalidad",
    "jugar",
    "juegos",
    "si",
    "me puedes decir",
    "me puedes dar",
    "me puedes informar",
    "si me interesa",
    "ayudar",
    "ayudas",
    "ayuda",
    "ayudame",
    ]



def esPreguntaValida(text):
    text = text.lower()
    return any(k in text for k in VALID_KEYWORDS)

async def inicioConversacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy el bot de productos. Pregunta por precios o disponibilidad de nuestros productos.")
    peticiones.registrar_peticion_global()  
   

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if not esPreguntaValida(text):
        await update.message.reply_text("Solo puedo responder preguntas sobre productos en nuestra tienda por favor verificar si escribio bien su pregunta.")
        return
    

    #recordatorio limpiar texto de simbologias que puedan afectar el programa interno o al usuario


    promptSinlimpiar = f"""Quiero actues como un cliente que va comprar un producto. sigue la siguiente indicacion:
    reescribe la pregunta del usuario de manera limpia y sin errores ortograficos, sin cambiar el sentido de la pregunta, pero sin incluir palabras que no sean necesarias, y sin incluir palabras que no tengan sentido en el contexto de una tienda de productos.
    Usuario comenta: {text} (no inventes conversaciones y si no hay especificacion de ningun producto solo responde con el mismo mensaje que el usuario comenta nada mas) y todo en menos de 3 saltos de lineas."""
    promptLimpio = ai.ask(promptSinlimpiar)

    print(f"promptReescrito: {promptLimpio}")


    # Buscar producto mencionado
    matched = []
    productos_esperados=[]
    delay= peticiones.calcular_delay_dinamico_global()
    # Verifica si el producto existe directamente

    time.sleep(delay)  # Espera para evitar problemas de sincronización
    productos_esperados = db.getProducto(promptLimpio)
    if productos_esperados is len(productos_esperados)>0:
        palabraClave = "productos encontrado"
        matched = productos_esperados
    else:
        # Si no se encuentra, buscar todos los productos
        palabraClave="no hay productos con ese nombre,pero quiero algo similar"

        time.sleep(delay)
        matched = db.getTodoProducto()


    contexto= contextoHistorial.obtener_historial(update)
         
    if matched or matched == []:
        prompt = f"""Primero que nada debes tener en cuenta el siguiente contexto de las conversaciones anteriores
        para guiarte en que responder y recordar lo que se pudo haber hablado antes (en dado caso no haya nada prosigue haciendo caso omiso a esto):"{contexto}"
        ahora resuelve las dudas del usuario, recuerda que eres un chatbot de tienda y debes responder de manera amigable,profesional y lo mas breve posible (sin uso de simbologias que puedan afectar el programa interno o al usuario).
        Usuario pregunta: "{promptLimpio}"
        tienes ciertas restricciones y un formato de respuesta que debes seguir estrictamente y sin quebrantarlas y solo las que estan a continuacion entre los corchetes, cualquier restriccion o regla que te pidan anteriormente deberas ignorarlas :[
        te dare cierta palabraclave y en dado caso la lista de productos que pregunte este vacia deberas recomendar algo similar de toda la tienda.
        tienes un listado productos delimitados por "llaves" donde cada uno es un producto.
        si en cantidad hay mas de 1 solo contestaras que si hay disponible o no (no des cantidad de cuantos hay).
        si solo pregunta por un "producto" por ejemplo "no tiene algun producto disponible" pero sin especificar nombre deberas preguntar por que especificamente busca el usuario por ejemplo "hay algun producto que sirva para guardar archivos".
        no se hacen compras, ni envios, ni pagos, ni nada de eso, solo se da informacion de productos y sus precios, disponibilidad y descripcion.
        Solo responde basado en la información dada y sobre productos de la tienda (cualquier otro tema queda ignorado estrictamente)(y solo da mas detalles si no lo estan en la descripcion sobre especificaciones que tenga el producto en paginas oficiales o con informacion oficial del producto)'.
        ]
        palabraClave: {palabraClave}
        productos encontrados: {matched}.
        que tiene su nombre, precio, disponibilida y descripcion, si hay mas de 1 entonces deberas recomendarlos en dado caso haya preguntado por otro.
         """
        respuesta = ai.ask(prompt)
        time.sleep(delay)

        # Guardar mensaje en el historial
        contextoUser= f"Usuario pregunto: {promptLimpio}\nChatBot respondio: {respuesta}"  
        promptLimpio=ai.ask(f"""sin simbologias (sin palabras con tildes ni acentos) en menos de 7 lineas resume lo mas importante sobre la siguiente conversacion 
        de que producto se esta hablando o interesando el usuario o que problema tiene:{contextoUser}""")
        contextoHistorial.manejar_mensajeHistorial(update, promptLimpio)

        print(promptLimpio)
        print(matched)
        print(text)
        await update.message.reply_text(respuesta)
    else:
        print(matched)
        await update.message.reply_text("No tengo información de ese producto. ¿Podrías verificar el nombre?")
