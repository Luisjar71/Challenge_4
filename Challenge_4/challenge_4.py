import heapq # Proporciona una implementación de cola de prioridad basada en montículos, 
             # utilizada para la lista de nodos abiertos en el algoritmo A*
import numpy as np
import random

# Clase para representar un nodo en el mapa
class Node:
    def __init__(self, x, y, costo, padre=None):
        self.x = x
        self.y = y
        self.costo = costo
        self.padre = padre
        self.heurisitica = 0
        self.costo_total = 0

    def __lt__(self, otro): #Método especial para comparar nodos basado en total_cost, necesario para que heapq pueda ordenar los nodos.
        return self.costo_total < otro.costo_total

class RouteCalculator:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = np.zeros((filas, columnas), dtype=int)

    def heurisitica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def obstaculos(self, x, y, tipo_obstaculo):
        if 0 <= x < self.filas and 0 <= y < self.columnas:
            self.mapa[x, y] = tipo_obstaculo

    def obstaculo_agua(self, count):
        agregado = 0
        while agregado < count:
            x = random.randint(0, self.filas - 1)
            y = random.randint(0, self.columnas - 1)
            if self.mapa[x, y] == 0:  # Asegurando que no se sobreponen obstáculos
                self.mapa[x, y] = 2
                agregado += 1

    def display_mapa(self, inicio=None, end=None, camino=None):
        symbols = {0: "  ", 1: "##", 2: "~~", 'S': " E", 'E': " S", 'P': "**"}
        print("  " + " ".join(f"{j:2}" for j in range(self.columnas)))
        print(" +" + "---" * self.columnas + "+")
        for i in range(self.filas):
            print(f"{i:2}|", end="")
            for j in range(self.columnas):
                if (i, j) == inicio:
                    print(symbols['S'], end=" ")
                elif (i, j) == end:
                    print(symbols['E'], end=" ")
                elif camino and (i, j) in camino:
                    print(symbols['P'], end=" ")
                else:
                    print(symbols[self.mapa[i, j]], end=" ")
            print("|")
        print(" +" + "---" * self.columnas + "+")

    
    def get_vecinos(self, node):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [Node(node.x + dx, node.y + dy, node.costo, node)
                for dx, dy in directions
                if 0 <= node.x + dx < self.filas and 0 <= node.y + dy < self.columnas]

    def encontrar_camino(self, inicio, end):
        lista_abierta = []
        lista_cerrada = set()
        nodo_inicio = Node(inicio[0], inicio[1], 0)
        nodo_inicio.heurisitica = self.heurisitica(inicio, end)
        nodo_inicio.costo_total = nodo_inicio.heurisitica

        heapq.heappush(lista_abierta, nodo_inicio)

        while lista_abierta:
            nodo_actual = heapq.heappop(lista_abierta)
            lista_cerrada.add((nodo_actual.x, nodo_actual.y))

            if (nodo_actual.x, nodo_actual.y) == end:
                return self.reconstruir_camino(nodo_actual)

            for vecino in self.get_vecinos(nodo_actual):
                if (vecino.x, vecino.y) in lista_cerrada or self.mapa[vecino.x, vecino.y] == 1:
                    continue

                vecino.costo = nodo_actual.costo + 1
                if self.mapa[vecino.x, vecino.y] == 2:  
                    vecino.costo += 2
                vecino.heurisitica = self.heurisitica((vecino.x, vecino.y), end)
                vecino.costo_total = vecino.costo + vecino.heurisitica

                heapq.heappush(lista_abierta, vecino)

        return None

    def reconstruir_camino(self, node):
        camino = []
        while node:
            camino.append((node.x, node.y))
            node = node.padre
        return camino[::-1]

def get_coordenadas(prompt, max_filas, max_columnas):
    while True:
        try:
            x, y = map(int, input(prompt).split(','))
            if 0 <= x < max_filas and 0 <= y < max_columnas:
                return x, y
            print(f"Coordenadas fuera de rango. Deben estar entre 0 y {max_filas-1} para las filas y entre 0 y {max_columnas-1} para las columnas.")
        except ValueError:
            print("Formato incorrecto. Por favor, ingrese las coordenadas en el formato x,y.")

def main():
    filas, columnas = 10, 10
    route_calculator = RouteCalculator(filas, columnas)

    num_obstaculos = int(input("¿Cuántos edificios (obstáculos intransitables) desea agregar? "))
    for _ in range(num_obstaculos):
        obstaculo = get_coordenadas("Ingrese las coordenadas del edificio (formato x,y): ", filas, columnas)
        route_calculator.obstaculos(obstaculo[0], obstaculo[1], 1)

    route_calculator.obstaculo_agua(10)

    print("Mapa con obstáculos:")
    route_calculator.display_mapa()

    inicio = get_coordenadas("Ingrese las coordenadas del punto de partida (formato x,y): ", filas, columnas)
    end = get_coordenadas("Ingrese las coordenadas del destino final (formato x,y): ", filas, columnas)

    if route_calculator.mapa[inicio[0], inicio[1]] == 0 and route_calculator.mapa[end[0], end[1]] == 0:
        camino = route_calculator.encontrar_camino(inicio, end)
        print("\nMapa actualizado con la ruta:")
        route_calculator.display_mapa(inicio, end, camino)
        if camino:
            print("Ruta encontrada:", camino)
        else:
            print("No se encontró una ruta.")
    else:
        print("Coordenadas no válidas o corresponden a un obstáculo.")

if __name__ == "__main__":
    main()
