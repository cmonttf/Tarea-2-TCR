import itertools
import numpy as np

def reduccion_sp(matriz_incidencia, confiabilidades_enlace):
    num_nodos = len(matriz_incidencia)
    
    nodos_conectados = {0, num_nodos - 1}
    
    cambios = True
    while cambios:
        cambios = False
        for i in range(num_nodos):
            for j in range(num_nodos):
                if i in nodos_conectados and matriz_incidencia[i][j] == 1:
                    if j not in nodos_conectados:
                        nodos_conectados.add(j)
                        cambios = True
    
    indices_conectados = sorted(list(nodos_conectados))
    matriz_reducida = matriz_incidencia[indices_conectados][:, indices_conectados]
    
    # Obtener las confiabilidades correspondientes a los nodos reducidos
    confiabilidades_reducidas = np.array([confiabilidades_enlace[i] for i in indices_conectados])

    return matriz_reducida, confiabilidades_reducidas

def generar_mps(matriz_reducida):
    num_nodos = len(matriz_reducida)
    conjuntos_mps = []

    for i in range(num_nodos):
        for j in range(num_nodos):
            if matriz_reducida[i, j] == 1:
                conjuntos_mps.append((i, j))

    return conjuntos_mps


def principio_exclusion_inclusion(confiabilidades, conjuntos):
    confiabilidad = 0
    num_nodos_reducidos = int(np.sqrt(len(confiabilidades)))  # Suponemos que es una matriz cuadrada

    for i in range(1, len(conjuntos) + 1):
        for combinacion in itertools.combinations(conjuntos, i):
            producto = 1
            for nodo_inicio, nodo_fin in combinacion:
                if nodo_inicio < num_nodos_reducidos and nodo_fin < num_nodos_reducidos:
                    producto *= confiabilidades[nodo_inicio * num_nodos_reducidos + nodo_fin]
            if i % 2 == 1:
                confiabilidad += producto
            else:
                confiabilidad -= producto
    return confiabilidad

def calcular_confiabilidad(matriz_incidencia, confiabilidades_enlace):
    matriz_reducida, confiabilidades_reducidas = reduccion_sp(matriz_incidencia, confiabilidades_enlace)
    conjuntos_mps = generar_mps(matriz_reducida)

    # Extraer las confiabilidades correspondientes a los nodos reducidos
    confiabilidades_reducidas = confiabilidades_enlace[np.where(np.sum(matriz_reducida, axis=0) > 0)[0]]

    confiabilidad = principio_exclusion_inclusion(confiabilidades_reducidas, conjuntos_mps)

    intervalo_1 = principio_exclusion_inclusion(confiabilidades_reducidas, conjuntos_mps[:2])
    intervalo_2 = principio_exclusion_inclusion(confiabilidades_reducidas, conjuntos_mps[2:6])

    return confiabilidad, intervalo_1, intervalo_2


# Lectura de datos
matrix_incidencia = np.genfromtxt('dataset/matrix_incid_5_7.csv', delimiter=',')
vector_conf = np.genfromtxt('dataset/vector_conf_5_7.csv', delimiter=',')

# Reducción SP
matriz_reducida, confiabilidades_reducidas = reduccion_sp(matrix_incidencia, vector_conf)

# Cálculo de confiabilidad
resultado = calcular_confiabilidad(matriz_reducida, confiabilidades_reducidas)

# Cantidad de nodos y enlaces post reducción SP
num_nodos_reducidos, num_enlaces_reducidos = matriz_reducida.shape

# Cálculo de MPS post reducción SP
conjuntos_mps_reducidos = generar_mps(matriz_reducida)

# Información adicional
print(f"Cantidad de nodos (post reducción SP): {num_nodos_reducidos}")
print(f"Cantidad de enlaces (post reducción SP): {num_enlaces_reducidos}")
print(f"Cantidad de MPS post reducción SP: {len(conjuntos_mps_reducidos)}")
print(f"Confiabilidad: {resultado[0]}")
print(f"Intervalo de confianza 1: {resultado[1]}")
print(f"Intervalo de confianza 2: {resultado[2]}")
