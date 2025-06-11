import os
import json

from datetime import datetime


class History:
    def __init__(self):
        self.base_dir = "historialChats"
        os.makedirs(self.base_dir, exist_ok=True)

    def manejar_mensajeHistorial(self, update, contexto):
        user_id = str(update.message.from_user.id)
        texto = contexto
        archivo_usuario = os.path.join(self.base_dir,f"historial_{user_id}.json")

        # Cargar historial existente o iniciar uno nuevo
        if os.path.exists(archivo_usuario):
            with open(archivo_usuario, "r") as f:
                historial = json.load(f)
        else:
            historial = []

        # Crear objeto del mensaje con timestamp
        nuevo_mensaje = {
            "usuarioID": update.message.from_user.id,
            "contexto": texto,
            "timestamp": datetime.now().isoformat()
        }

        # Añadir y mantener máximo 100 mensajes
        historial.append(nuevo_mensaje)
        if len(historial) > 100:
            historial = historial[-100:]  # conservar los últimos 100

        # Guardar historial actualizado
        with open(archivo_usuario, "w") as f:
            json.dump(historial, f, indent=2)

        
    def obtener_historial(self, update):
        user_id = str(update.message.from_user.id)
        archivo_usuario = os.path.join(self.base_dir, f"historial_{user_id}.json")

        if os.path.exists(archivo_usuario):
            with open(archivo_usuario, "r") as f:
                historial = json.load(f)
                historialContexto = []
                for contexto in historial:
                    historialContexto.append(contexto["contexto"])
            return historialContexto
        else:
            return []
