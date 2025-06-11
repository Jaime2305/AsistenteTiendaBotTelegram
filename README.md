Asistente de Tienda (solamente para consulta de existencia, precios o descripcion de productos)

Este bot con ayuda del API de gemini 2.0-flash procesa con multiples instrucciones (promts) lo que el usuario quiere preguntar para dar una mejor respuesta
por el momento es algo basico porque faltaria seguridad contra ataques DOS o DDOS por si quisieran saturar de peticiones automatizadas, tambien aun falta 
separar los "productos" mas especificamente en categorias para que en una lista muy grande no tenga que consultar con todos los productos sino una "pequeña" parte.


Para probarlo solo necesitan su token del API de telegram como de Gemini de la version gratuita de prueba (en el archivo "configuracion.py")

 Clona el repositorio:
```bash
git clone https://github.com/Jaime2305/AsistenteTiendaBotTelegram.git
cd AsistenteTiendaBotTelegram
