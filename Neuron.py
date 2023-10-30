import math
import random

class Neurona:
    def __init__(self, num_dendritas):
        # Inicializa los pesos utilizando la inicialización de Xavier
        self.peso = [random.uniform(-1, 1) * math.sqrt(1 / num_dendritas) for _ in range(num_dendritas)]
        self.umbral = 0.5  # Umbral de activación
        self.potencial = 0.0
        self.sinapsis_salientes = []

    def agregar_sinapsis_saliente(self, sinapsis):
        self.sinapsis_salientes.append(sinapsis)

    def generar_potencial_de_accion(self):
        self.potencial = self.funcion_activacion(self.potencial)

    def activar(self, entradas):
        if len(entradas) != len(self.peso):
            raise ValueError("Entradas no compatibles con la neurona")

        suma_ponderada = sum(w * x for w, x in zip(self.peso, entradas))
        self.potencial = suma_ponderada

        if self.potencial > self.umbral:
            self.generar_potencial_de_accion()

        for sinapsis in self.sinapsis_salientes:
            sinapsis.transmitir_potencial(self.potencial)

    def funcion_activacion(self, x):
        # Utiliza la función ReLU como función de activación
        return max(0, x)

    def sinapsis(self):
        return self.sinapsis_salientes
    

class Sinapsis:
    def __init__(self, neurona_presinaptica, neurona_postsinaptica, peso_sinaptico):
        self.neurona_presinaptica = neurona_presinaptica
        self.neurona_postsinaptica = neurona_postsinaptica
        self.peso_sinaptico = peso_sinaptico

    def transmitir_potencial(self, potencial):
        self.neurona_postsinaptica.potencial += potencial * self.peso_sinaptico

    def ajustar_peso_sinaptico(self):
        # Utiliza la regla de Hebb con signo para ajustar los pesos
        self.peso_sinaptico += self.neurona_presinaptica.potencial * self.neurona_postsinaptica.potencial



class RedNeuronal:
    def __init__(self, num_entradas, num_ocultas, num_salidas):
        self.num_entradas = num_entradas
        self.num_ocultas = num_ocultas
        self.num_salidas = num_salidas

        self.neuronas_ocultas = []
        self.neuronas_salidas = []

        self.crear_neuronas()

    def crear_neuronas(self):
        # Crear neuronas ocultas
        for _ in range(self.num_ocultas):
            neurona = Neurona(self.num_entradas)
            self.neuronas_ocultas.append(neurona)

        # Crear neuronas de salida
        for _ in range(self.num_salidas):
            neurona = Neurona(self.num_ocultas)
            self.neuronas_salidas.append(neurona)

        # Crear sinapsis entre las neuronas
        for neurona_oculta in self.neuronas_ocultas:
            for neurona_salida in self.neuronas_salidas:
                sinapsis = Sinapsis(neurona_oculta, neurona_salida, random.random())
                neurona_oculta.agregar_sinapsis_saliente(sinapsis)

    def activar(self, entradas):
        # Activar neuronas ocultas
        for neurona in self.neuronas_ocultas:
            neurona.activar(entradas)

        # Activar neuronas de salida
        for neurona in self.neuronas_salidas:
            neurona.activar([n.potencial for n in self.neuronas_ocultas])

    def sinapsis(self):
        sinapsis = []
        for neurona in self.neuronas_ocultas:
            sinapsis += neurona.sinapsis()

        for neurona in self.neuronas_salidas:
            sinapsis += neurona.sinapsis()

        return sinapsis

    def imprimir_red(self):
        print("Neuronas ocultas:")
        for i, neurona in enumerate(self.neuronas_ocultas, start=1):
            print("Neurona oculta #{}: {}".format(i, neurona.peso))

        print("Neuronas de salida:")
        for i, neurona in enumerate(self.neuronas_salidas, start=1):
            print("Neurona de salida #{}: {}".format(i, neurona.peso))

        print("Sinapsis:")

        for i, sinapsis in enumerate(self.sinapsis(), start=1):
            print("Sinapsis #{}: {}".format(i, sinapsis.peso_sinaptico))

    def entrenar(self, entradas, salidas):
        self.activar(entradas)
        self.imprimir_red()

        # Calcular error
        error = 0.0
        for neurona, salida in zip(self.neuronas_salidas, salidas):
            error += (salida - neurona.potencial) ** 2
        error /= len(self.neuronas_salidas)

        # Ajustar pesos de las sinapsis
        for sinapsis in self.sinapsis():
            sinapsis.ajustar_peso_sinaptico()

        return error
    
    def predecir(self, entradas):
        self.activar(entradas)
        return [neurona.potencial for neurona in self.neuronas_salidas]
    
    def entrenar_red(self, entradas, salidas, num_epocas):
        for epoca in range(num_epocas):
            error = 0.0
            for entrada, salida in zip(entradas, salidas):
                error += self.entrenar(entrada, salida)
            error /= len(entradas)
            print("Epoca #{}: Error = {}".format(epoca + 1, error))

if __name__ == "__main__":
    # AND
    entradas = [[0, 0], [0, 1], [1, 0], [1, 1],[0, 0], [0, 1], [1, 0], [1, 1]]
    salidas = [[0], [0], [0], [1],[0], [0], [0], [1]]

    red = RedNeuronal(2, 2, 1)
    red.entrenar_red(entradas, salidas, 10)

    print("Predicciones:")
    for entrada in entradas:
        print("{} => {}".format(entrada, red.predecir(entrada)))




