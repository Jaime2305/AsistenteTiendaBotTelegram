import time
from time import time as ahora  # evita conflicto con el módulo 'time'

class Delay:
    """Maneja el tráfico global y calcula delays dinámicos basados en la carga."""
    
    def __init__(self):
        self.trafico_global = []
        self.VENTANA_TIEMPO = 60        # tiempo para calcular carga (en segundos)
        self.MAX_PETICIONES = 200       # tráfico considerado "alto"
        self.SLEEP_MIN = 0.05           # mínimo delay
        self.SLEEP_MAX = 3              # máximo delay


    def registrar_peticion_global(self):
        t = ahora()
        self.trafico_global.append(t)
        # Elimina peticiones antiguas fuera de la ventana
        self.trafico_global[:] = [x for x in self.trafico_global if t - x < self.VENTANA_TIEMPO]

    def calcular_delay_dinamico_global(self):
        carga = len(self.trafico_global)
        factor_carga = min(carga / self.MAX_PETICIONES, 1.0)
        delay = self.SLEEP_MIN + (self.SLEEP_MAX - self.SLEEP_MIN) * factor_carga
        return delay
