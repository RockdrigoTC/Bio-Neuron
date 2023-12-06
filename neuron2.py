import numpy as np
import matplotlib.pyplot as plt

class Neurona:
    def __init__(self, umbral=0.5, t_refractario=2, v_reset=0.0, v_decay=0.95, eficacia_sinaptica=0.5):
        # Estado inicial de la neurona
        self.potencial = 0.0
        self.umbral = umbral
        self.t_refractario = t_refractario
        self.v_reset = v_reset
        self.v_decay = v_decay
        self.tiempo_refractario = 0
        self.eficacia_sinaptica = eficacia_sinaptica
        self.historial_disparos = []

    def recibir_entrada(self, entrada):
        if self.tiempo_refractario == 0:
            self.potencial += entrada * self.eficacia_sinaptica
        
        if self.potencial >= self.umbral:
            self.disparar()
            return True
        # Registrar la falta de disparo
        self.historial_disparos.append(False)

    def paso_del_tiempo(self):
        if self.potencial >= self.umbral:
            self.potencial = self.v_reset

        if self.tiempo_refractario > 0:
            # Disminuir el tiempo restante del periodo refractario
            self.tiempo_refractario -= 1
        else:
            # Decaimiento natural del potencial de membrana
            self.potencial *= self.v_decay

        # Aplicar LTD si procede
        if not self.historial_disparos[-1] and self.eficacia_sinaptica > 0.5:  # Si no hubo disparo en la ultima entrada
            self.eficacia_sinaptica *= 0.96  # Disminuir la eficacia
        if self.eficacia_sinaptica < 0.5:
            self.eficacia_sinaptica = 0.5

        if len(self.historial_disparos) > 10: 
            self.historial_disparos.pop(0)


    def disparar(self):
        self.tiempo_refractario = self.t_refractario
        # Registrar el disparo
        self.historial_disparos.append(True)
        # Implementar LTP
        if self.eficacia_sinaptica < 1.5:
            self.eficacia_sinaptica *= 1.09  # Aumentar la eficacia
        if self.eficacia_sinaptica > 1.5:
            self.eficacia_sinaptica = 1.5
    
    def estado_actual(self):
        return self.potencial, self.eficacia_sinaptica, self.tiempo_refractario
    

# Crear una instancia de la neurona
neurona = Neurona()

# Listas para almacenar los valores del potencial de membrana y los momentos de disparo
potencial = []
disparos = []
efica_sinaptica = []

# Simular algunos pasos de tiempo con entradas variadas
entradas = np.random.uniform(0.1, 0.9, 100)
for i, entrada in enumerate(entradas):
    neurona.recibir_entrada(entrada)
    potencial.append(neurona.estado_actual()[0])
    efica_sinaptica.append(neurona.estado_actual()[1])
    neurona.paso_del_tiempo()

# Graficar el potencial de membrana de la neurona y las entradas
plt.figure("Neurona", figsize=(10, 5))
plt.title("Potencial de Membrana de la Neurona")
plt.xlabel("Tiempo")
plt.ylabel("Potencial de Membrana")
plt.ylim(0.01, 1.6)
plt.plot([0, len(potencial)], [neurona.umbral, neurona.umbral], 'r--')

#plt.plot(entradas, 'b', label="Entrada")
plt.plot(potencial, 'g', label="Potencial de Membrana")
plt.plot(efica_sinaptica, 'm', label="Eficacia Sináptica")
#plt.scatter(disparos, [neurona.umbral] * len(disparos), c='r', label="Disparo")
plt.legend(loc="upper left")

plt.show()


