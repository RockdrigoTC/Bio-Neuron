import numpy as np
import matplotlib.pyplot as plt

class Neurona:
    def __init__(self, umbral=1.0, t_refractario=2, v_reset=0.0, v_decay=0.95):
        # Estado inicial de la neurona
        self.potencial = 0.0
        self.umbral = umbral
        self.t_refractario = t_refractario
        self.v_reset = v_reset
        self.v_decay = v_decay
        self.tiempo_refractario = 0

    def recibir_entrada(self, entrada):
        if self.tiempo_refractario == 0:
            self.potencial += entrada
        
        if self.potencial >= self.umbral:
            self.disparar()
            return True

    def paso_del_tiempo(self):
        if self.potencial >= self.umbral:
            self.potencial = self.v_reset

        if self.tiempo_refractario > 0:
            # Disminuir el tiempo restante del periodo refractario
            self.tiempo_refractario -= 1
        else:
            # Decaimiento natural del potencial de membrana
            self.potencial *= self.v_decay


    def disparar(self):
        self.tiempo_refractario = self.t_refractario
    
    def estado_actual(self):
        return self.potencial, self.tiempo_refractario
    
class NeuronaConPlasticidad(Neurona):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar la eficacia sináptica
        self.eficacia_sinaptica = 0.75
        # Historial de disparos para determinar LTP o LTD
        self.historial_disparos = []

    def recibir_entrada(self, entrada):
        # Ajustar la entrada por la eficacia sináptica
        entrada_ajustada = entrada * self.eficacia_sinaptica
        return super().recibir_entrada(entrada_ajustada)

    def disparar(self):
        super().disparar()
        # Registrar el disparo
        self.historial_disparos.append(True)
        # Implementar LTP
        if self.eficacia_sinaptica < 2.0:
            self.eficacia_sinaptica *= 1.05  # Aumentar la eficacia en un 20%

    def paso_del_tiempo(self):
        super().paso_del_tiempo()
        # Registrar la falta de disparo
        self.historial_disparos.append(False)
        # Aplicar LTD si procede
        if not self.historial_disparos[-1] and self.eficacia_sinaptica > 0.2:  # Si no hubo disparo en el último paso
            self.eficacia_sinaptica *= 0.95  # Disminuir la eficacia en un 5%

        # Mantener el historial de disparos a una longitud manejable
        if len(self.historial_disparos) > 100:  # Mantener los últimos 100 pasos
            self.historial_disparos.pop(0)


# Crear una instancia de la neurona
neurona = NeuronaConPlasticidad()

# Listas para almacenar los valores del potencial de membrana y los momentos de disparo
potencial = []
disparos = []

# Simular algunos pasos de tiempo con entradas variadas
entradas = np.random.uniform(0.01, 0.5, 1000)
for i, entrada in enumerate(entradas):
    print("Paso de tiempo: {}".format(i))
    print("Entrada: {}".format(entrada))
    print("Potencial de membrana: {}".format(neurona.estado_actual()[0]))
    print("Eficacia sináptica: {}".format(neurona.eficacia_sinaptica))
    print("Tiempo refractario: {}".format(neurona.estado_actual()[1]))

    if neurona.recibir_entrada(entrada):
        disparos.append(i)  # Guardar el índice del tiempo de disparo
    potencial.append(neurona.estado_actual()[0])
    neurona.paso_del_tiempo()

# Graficar el potencial de membrana de la neurona
plt.figure("Neurona", figsize=(10, 5))
plt.title("Potencial de Membrana de la Neurona")
plt.xlabel("Tiempo")
plt.ylabel("Potencial de Membrana")
plt.ylim(0.01, 1.1)
plt.plot(potencial)

# # Marcar el umbral de disparo
plt.plot([0, len(potencial)], [neurona.umbral, neurona.umbral], 'r--')

# # Marcar los momentos de disparo en la gráfica
# for d in disparos:
#     plt.plot(d, potencial[d], 'ro')
    

plt.show()


