import math
import random

class Neurona:
    def __init__(self, num_dendritas):
        self.peso = [0.0] * num_dendritas
        self.umbral = 0.0
        self.potencial = 0.0
        self.sinapsis_salientes = []

    def agregar_sinapsis_saliente(self, sinapsis):
        self.sinapsis_salientes.append(sinapsis)

    def activar(self, entradas):
        if len(entradas) != len(self.peso):
            raise ValueError("Entradas no compatibles con la neurona")

        suma_ponderada = sum(w * x for w, x in zip(self.peso, entradas))
        self.potencial = suma_ponderada
        self.potencial = self.funcion_activacion(self.potencial)

        for sinapsis in self.sinapsis_salientes:
            sinapsis.transmitir_potencial(self.potencial)

    def funcion_activacion(self, x):
        return 1 / (1 + math.exp(-x))

    def sinapsis(self):
        return self.sinapsis_salientes

class Sinapsis:
    def __init__(self, neurona_presinaptica, neurona_postsinaptica, peso_sinaptico):
        self.neurona_presinaptica = neurona_presinaptica
        self.neurona_postsinaptica = neurona_postsinaptica
        self.peso_sinaptico = peso_sinaptico
        self.tasa_aprendizaje = 0.1  # Tasa de aprendizaje para ajustar los pesos

    def transmitir_potencial(self, potencial_presinaptico):
        self.neurona_postsinaptica.activar([potencial_presinaptico * self.peso_sinaptico])

    def ajustar_peso_sinaptico(self):
        # Plasticidad sináptica
        delta_peso = self.tasa_aprendizaje * self.neurona_presinaptica.potencial
        self.peso_sinaptico += delta_peso

# Crear una neurona con 3 dendritas (entradas)
neurona1 = Neurona(10)
neurona2 = Neurona(10)
neurona3 = Neurona(10)

# Crear dos sinapsis que se conectan a las neuronas
sinapsis1 = Sinapsis(neurona1, neurona2, 0.6)  # neurona1 -> sinapsis1 -> neurona2
sinapsis2 = Sinapsis(neurona2, neurona3, 0.2)  # neurona2 -> sinapsis2 -> neurona3

# Agregar las sinapsis a las neuronas
neurona1.agregar_sinapsis_saliente(sinapsis1)
neurona2.agregar_sinapsis_saliente(sinapsis2)

num_activaciones = 10
for i in range(num_activaciones):
    print(f"Iteración {i + 1}:")
    entrada = [random.randint(0, 1) for _ in range(10)]  # Genera una entrada aleatoria
    neurona1.activar(entrada)
    print("Entrada: ", entrada)
    print("Potencial de la neurona 3: ", neurona3.potencial)
    print("Potencial de la neurona 2: ", neurona2.potencial)
    print("Potencial de la neurona 1: ", neurona1.potencial)
    print()
