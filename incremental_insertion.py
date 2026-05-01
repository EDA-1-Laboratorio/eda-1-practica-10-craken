"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Estrategia incremental – Insertion sort instrumentado

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""

import time
import random

# ---------------------------------------------------------------------------
# Problema A – Insertion sort con métricas
# ---------------------------------------------------------------------------

def insertion_sort_metricas(arr: list) -> tuple:
	"""
	Ordena 'arr' usando insertion sort e instrumenta la ejecución.

	Retorna:
		(arreglo_ordenado, comparaciones, movimientos, tiempo_seg)

	Pistas:
		El bucle externo recorre i de 1 a n-1.
		'llave' = arr[i] es el elemento a insertar.
		El bucle interno (while) desplaza elementos mayores que 'llave' hacia
		la derecha; cada desplazamiento es un movimiento.
		Cuenta también la última comparación del while (la que falla).
		La colocación final de llave es un movimiento.
	"""
	arr = arr.copy()
	n = len(arr)
	comparaciones = 0
	movimientos   = 0
	inicio        = time.perf_counter()

	for i in range(1, n):
		llave = arr[i]
		j = i - 1

        # TODO: mientras j >= 0 y arr[j] > llave:
        #           - incrementa comparaciones
        #           - desplaza arr[j] a arr[j+1], incrementa movimientos
        #           - decrement j

        # TODO: cuenta la comparación que termina el while (si j >= 0)

        # TODO: coloca llave en arr[j + 1] e incrementa movimientos

		while j>=0 and llave<arr[j]:
			comparaciones+=1
			arr[j+1]=arr[j]
			j-=1
			movimientos+=1
		arr[j+1]=llave
		comparaciones+=1

	tiempo = time.perf_counter() - inicio
	return (arr, comparaciones, movimientos, tiempo)


# ---------------------------------------------------------------------------
# Problema B – Generación de escenarios
# ---------------------------------------------------------------------------

def generar_arreglo(n: int, escenario: str) -> list:
    """
    Genera un arreglo de tamaño n según el escenario indicado.

    Escenarios:
        'mejor'    -> ya ordenado de menor a mayor    (mejor caso: Θ(n))
        'peor'     -> inversamente ordenado            (peor caso:  Θ(n²))
        'promedio' -> aleatorio                        (caso promedio: Θ(n²))

    Pistas:
        list(range(n))           arreglo [0, 1, 2, ..., n-1]
        list(range(n, 0, -1))    arreglo [n, n-1, ..., 1]
        random.shuffle(arr)      mezcla in-place
    """
    if escenario == "mejor": 
        arr= list(range(n))
    elif escenario == "peor":
        arr= list(range(n-1,-1,-1))
    elif escenario == "promedio":
        arr= list(range(n))
        random.shuffle(arr)
    else:
       raise  ValueError("Escenario inválido")

    return arr
    
    # TODO: implementa los tres escenarios; lanza ValueError si escenario es inválido.


def medir_escenarios(tamanos: list) -> list:
    """
    Para cada tamaño en 'tamanos' evalúa los tres escenarios e imprime resultados.

    Retorna:
        Lista de dicts: {tamano, escenario, comparaciones, movimientos, tiempo}
    """
    resultados = []
    
    for n in tamanos:
        for escenario in ("mejor", "promedio", "peor"):
            arr = generar_arreglo(n, escenario)
            arr, c, m, t =insertion_sort_metricas(arr)
            diccionario={
				"tamaño": n,
				"escenario":escenario,
				"comparaciones": c,
				"movimientos": m,
				"tiempo": t
            }
            # TODO: llama a insertion_sort_metricas y guarda el resultado.
            # Estructura del dict:
            # {
            #   "tamano": n,
            #   "escenario": escenario,
            #   "comparaciones": ...,
            #   "movimientos": ...,
            #   "tiempo": ...
            # }
            resultados.append(diccionario) 
    return resultados


# ---------------------------------------------------------------------------
# Problema D – Versión híbrida (insertion sort + merge sort)
# ---------------------------------------------------------------------------

def _merge(izq: list, der: list) -> list:
    """Combina dos listas ordenadas en una sola."""
    merged = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            merged.append(izq[i])
            i += 1
        else:
            merged.append(der[j])
            j += 1
    merged.extend(izq[i:])
    merged.extend(der[j:])
    return merged
    # TODO: implementa la fusión estándar de merge sort.
    pass


def _merge_sort_hibrido(arr: list, umbral: int) -> list:
    """
    Divide 'arr' recursivamente.
    Si el subarreglo tiene tamaño <= umbral, usa insertion_sort_metricas.
    Si no, divide a la mitad y fusiona con _merge.
    """
    if len(arr) <= umbral:
        return insertion_sort_metricas(arr)[0]
        # TODO: retorna insertion_sort_metricas(arr)[0]
        pass
    mid = len(arr) // 2
    left_half = _merge_sort_hibrido(arr[:mid], umbral)
    right_half = _merge_sort_hibrido(arr[mid:], umbral)
    return _merge(left_half, right_half)
    # TODO: llama recursivamente y fusiona con _merge
    pass


def insertion_sort_hibrido(arr: list, umbral: int = 32) -> list:
    """
    Punto de entrada del ordenamiento híbrido.
    Retorna el arreglo ordenado.
    """
    arreglo = _merge_sort_hibrido(arr, umbral)
    return arreglo
    # TODO: llama a _merge_sort_hibrido
    pass


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    tamanos = [1000, 2000, 4000, 8000]
    print("Midiendo escenarios... (puede tardar unos segundos)\n")
    resultados = medir_escenarios(tamanos)

    if resultados:
        print(f"{'Tamaño':>8} {'Escenario':>10} {'Comps':>12} "
              f"{'Movs':>12} {'Tiempo (s)':>12}")
        print("-" * 60)
        for r in resultados:
            print(f"{r['tamaño']:>8} {r['escenario']:>10} "
                  f"{r['comparaciones']:>12} {r['movimientos']:>12} "
                  f"{r['tiempo']:>12.4f}")
    else:
        print("medir_escenarios aún no implementada.")
