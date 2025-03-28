# -*- coding: utf-8 -*-
"""robot_pasillo_01.ipynb

Automatically generated by Colab.


"""

# =====================================================================
# Algoritmo de Iteración de Política
#
# =====================================================================
# _Aprendizaje por Refuerzo I
# _Maestria en Inteligencia Artificial
# _UBA
# _2025
# =====================================================================


'''

Robot limpiador de un pasillo
 _______
|_|_|_|_|

'''

import numpy as np

# Definición del entorno
NUM_ESTADOS = 4
ACCIONES = ['Izquierda', 'Derecha']
RECOMPENSA_NORMAL = -1
RECOMPENSA_TERMINAL = 0
FACTOR_DESCUENTO = 0.9

def transicion(estado, accion):
    """Determina el siguiente estado dado el estado actual y la acción."""
    if estado == 4:
        return 4  # En el estado terminal, permanece ahí
    if accion == 'Izquierda':
        return max(1, estado - 1)  # No puede ir a la izquierda desde el estado 1
    elif accion == 'Derecha':
        return min(NUM_ESTADOS, estado + 1) # No puede ir a la derecha desde el estado 4
    else:
        raise ValueError("Acción inválida")

def recompensa(estado, accion):
    """Retorna la recompensa para un estado y acción dados."""
    if estado == 4:
        return RECOMPENSA_TERMINAL
    else:
        return RECOMPENSA_NORMAL

def evaluacion_politica(politica, funcion_valor, tolerancia=1e-6):
    """Evalúa la política actual para determinar la función de valor."""
    iteraciones = 0
    while True:
        delta = 0
        iteraciones += 1
        funcion_valor_anterior = funcion_valor.copy() # Guarda la función de valor de la iteración anterior
        for estado in range(1, NUM_ESTADOS + 1):
            if estado == 4:
                continue  # No necesitamos evaluar el estado terminal
            accion = politica[estado - 1] # Ajuste de índice
            valor_anterior = funcion_valor[estado - 1] # Ajuste de índice

            siguiente_estado = transicion(estado, accion)
            recompensa_inmediata = recompensa(estado, accion)

            funcion_valor[estado - 1] = recompensa_inmediata + FACTOR_DESCUENTO * funcion_valor[siguiente_estado - 1] # Ajuste de índice
            delta = max(delta, abs(valor_anterior - funcion_valor[estado - 1]))

        if iteraciones <= 2:  # Imprime las primeras dos iteraciones
            print(f"    Evaluación Política - Iteración {iteraciones}: {funcion_valor}")

        if delta < tolerancia:
            break

    return funcion_valor

def mejora_politica(funcion_valor):
    """Mejora la política basada en la función de valor actual."""
    politica_estable = True
    nueva_politica = [None] * NUM_ESTADOS # Prealocamos la lista
    for estado in range(1, NUM_ESTADOS + 1):
        if estado == 4:
            nueva_politica[estado - 1] = None # Estado terminal
            continue

        valor_acciones = []
        for accion in ACCIONES:
            siguiente_estado = transicion(estado, accion)
            recompensa_inmediata = recompensa(estado, accion)
            valor_acciones.append(recompensa_inmediata + FACTOR_DESCUENTO * funcion_valor[siguiente_estado - 1])

        mejor_accion_indice = np.argmax(valor_acciones)
        mejor_accion = ACCIONES[mejor_accion_indice]

        if politica[estado - 1] != mejor_accion:
            politica_estable = False
        nueva_politica[estado - 1] = mejor_accion # Ajuste de índice

    return nueva_politica, politica_estable

# Inicialización
politica = ['Derecha', 'Izquierda', 'Derecha', None] # Política inicial (lista, no numpy array para facilitar el uso de strings)
funcion_valor = np.zeros(NUM_ESTADOS) # Función de valor inicial (numpy array para cálculos eficientes)


# Iteración de políticas
iteracion = 0
while True:
    iteracion = iteracion+1
    print(f"Iteración {iteracion}:")

    # 1. Evaluación de la política
    print("  Evaluación de la Política:")
    funcion_valor = evaluacion_politica(politica, funcion_valor)
    print("  Función de valor:", funcion_valor) # Imprime la función de valor después de la convergencia

    # 2. Mejora de la política
    nueva_politica, politica_estable = mejora_politica(funcion_valor)
    print("  Política:", politica)

    if politica_estable:
        print("\nPolítica óptima encontrada:")
        print("  Política:", politica)
        print("  Función de valor:", funcion_valor)
        break

    politica = nueva_politica[:] # Crea una copia para evitar problemas de referencia