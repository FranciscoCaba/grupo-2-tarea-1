import time
import random

# ---------------------------
# Funciones Auxiliares
# ---------------------------
def is_safe(board, row, col):
    """
    Verifica si es seguro colocar una reina en (row, col)
    considerando la lista 'board' que contiene las columnas asignadas a cada fila.
    """
    for r, c in enumerate(board):
        if c == col or abs(c - col) == abs(row - r):
            return False
    return True

def board_to_string(board):
    """
    Convierte una solución (lista de columnas para cada fila) en una representación tipo tablero.
    Una casilla con reina se muestra con 'Q' y vacía con '.'.
    """
    if board is None:
        return "No se encontró solución."
    n = len(board)
    result = []
    for row in range(n):
        line = " ".join("Q" if board[row] == col else "." for col in range(n))
        result.append(line)
    return "\n".join(result)

# ---------------------------
# Algoritmo 1: Backtracking
# ---------------------------
def n_queens_backtracking(n, find_all=False):
    """
    Backtracking para el problema de las N-Reinas.
    Parámetros:
      - n: tamaño del tablero
      - find_all: Si es True, encuentra todas las soluciones; de lo contrario, se detiene en la primera.
    Retorna: (soluciones, estados_expandidos, tiempo_ejecución)
      - soluciones: lista de soluciones (cada solución es una lista de números que representan las columnas)
      - estados_expandidos: cantidad de asignaciones realizadas (nodos visitados)
      - tiempo_ejecución: tiempo de ejecución en segundos
    """
    solutions = []
    state_counter = 0

    def backtrack(row, board):
        nonlocal state_counter
        if row == n:
            solutions.append(board.copy())
            return not find_all  # Si se desea 1 solución se retorna True para detener la búsqueda.
        valid_options = [col for col in range(n) if is_safe(board, row, col)]
        if not valid_options:
            return False
        for col in valid_options:
            state_counter += 1
            board.append(col)
            stop = backtrack(row + 1, board)
            if stop and not find_all:
                return True
            board.pop()
        return False

    start_time = time.time()
    backtrack(0, [])
    elapsed = time.time() - start_time
    return solutions, state_counter, elapsed

# ---------------------------
# Algoritmo 2: Las Vegas
# ---------------------------
def n_queens_las_vegas(n, timeout=5):
    """
    Algoritmo de Las Vegas para N-Reinas.
    Se asigna un valor aleatorio que cumpla con las restricciones para cada fila.
    Si en algún momento no hay opciones, se retrocede.
    Parámetros:
      - n: tamaño del tablero
      - timeout: tiempo máximo en segundos para buscar solución.
    Retorna: (solución, estados_expandidos, tiempo_ejecución)
      - solución: una solución encontrada (lista de columnas) o None si no se encontró en el tiempo dado.
    """
    start_time = time.time()
    state_counter = [0]  # Lista para permitir modificación en la función interna.
    board = [None] * n
    solution_found = False

    def recursive_las_vegas(row):
        nonlocal solution_found
        if time.time() - start_time > timeout:
            return False
        if row == n:
            solution_found = True
            return True
        options = list(range(n))
        random.shuffle(options)
        for col in options:
            if is_safe(board[:row], row, col):
                board[row] = col
                state_counter[0] += 1
                if recursive_las_vegas(row + 1):
                    return True
        return False

    recursive_las_vegas(0)
    elapsed = time.time() - start_time
    return (board.copy() if solution_found else None), state_counter[0], elapsed

# ---------------------------
# Algoritmo 3: Heurístico (Mínimos Conflictos)
# ---------------------------
def n_queens_min_conflicts(n, timeout=5):
    """
    Algoritmo basado en la heurística de mínimos conflictos que termina según un tiempo máximo.
    Se parte de una asignación aleatoria y se modifica iterativamente la posición de las reinas con conflictos.
    Parámetros:
      - n: tamaño del tablero
      - timeout: tiempo máximo en segundos para buscar una solución.
    Retorna: (solución, estados_expandidos, tiempo_ejecución)
      - solución: la configuración de solución o None si no se alcanzó.
    """
    start_time = time.time()
    board = [random.randint(0, n-1) for _ in range(n)]
    state_counter = 0

    def count_conflicts(board, row, col):
        conflicts = 0
        for r in range(n):
            if r != row:
                if board[r] == col or abs(board[r] - col) == abs(r - row):
                    conflicts += 1
        return conflicts

    def total_conflicts(board):
        total = 0
        for row in range(n):
            total += count_conflicts(board, row, board[row])
        return total // 2

    while time.time() - start_time < timeout:
        state_counter += 1
        if total_conflicts(board) == 0:
            elapsed = time.time() - start_time
            return board, state_counter, elapsed
        conflicted = [row for row in range(n) if count_conflicts(board, row, board[row]) > 0]
        if not conflicted:
            continue
        row = random.choice(conflicted)
        conflict_counts = [count_conflicts(board, row, col) for col in range(n)]
        min_count = min(conflict_counts)
        best_moves = [col for col in range(n) if conflict_counts[col] == min_count]
        board[row] = random.choice(best_moves)
    elapsed = time.time() - start_time
    return None, state_counter, elapsed


# ---------------------------
# Interfaz de Terminal
# ---------------------------
def ejecutar_algoritmo():
    try:
        n = int(input("Ingrese el tamaño del tablero (N): "))
        if n <= 0:
            print("El valor de N debe ser un entero positivo.")
            return
    except ValueError:
        print("Valor inválido. Intente nuevamente.")
        return

    print("\nSeleccione el algoritmo a ejecutar:")
    print("1. Backtracking (1 solución)")
    print("2. Backtracking (todas las soluciones)")
    print("3. Las Vegas")
    print("4. Mínimos Conflictos")
    opcion = input("Opción [1-4]: ")

    if opcion == "1":
        solutions, states, elapsed = n_queens_backtracking(n, find_all=False)
        print(f"\nBacktracking (1 solución)")
        print(f"Tiempo: {elapsed:.4f} s")
        print(f"Estados expandidos: {states}")
        if solutions:
            print("Solución encontrada:")
            # print(board_to_string(solutions[0]))
        else:
            print("No se encontró solución.")
    elif opcion == "2":
        # Advertencia: Backtracking para todas las soluciones puede ser lento para valores grandes de N.
        solutions, states, elapsed = n_queens_backtracking(n, find_all=True)
        print(f"\nBacktracking (todas las soluciones)")
        print(f"Tiempo: {elapsed:.4f} s")
        print(f"Estados expandidos: {states}")
        if solutions:
            print(f"Cantidad de soluciones encontradas: {len(solutions)}")
            print("Ejemplo de solución:")
            # print(board_to_string(solutions[0]))
        else:
            print("No se encontró solución.")
    elif opcion == "3":
        solution, states, elapsed = n_queens_las_vegas(n)
        print(f"\nLas Vegas")
        print(f"Tiempo: {elapsed:.4f} s")
        print(f"Estados expandidos: {states}")
        if solution:
            print("Solución encontrada:")
            # print(board_to_string(solution))
        else:
            print("No se encontró solución en el tiempo dado.")
    elif opcion == "4":
        solution, states, elapsed = n_queens_min_conflicts(n)
        print(f"\nMínimos Conflictos")
        print(f"Tiempo: {elapsed:.4f} s")
        print(f"Estados expandidos (iteraciones): {states}")
        if solution:
            print("Solución encontrada:")
            # print(board_to_string(solution))
        else:
            print("No se encontró solución en el número máximo de iteraciones.")
    else:
        print("Opción inválida.")

def comparar_algoritmos():
    try:
        n = int(input("Ingrese el tamaño del tablero (N) para comparar algoritmos: "))
        if n <= 0:
            print("El valor de N debe ser un entero positivo.")
            return
    except ValueError:
        print("Valor inválido. Intente nuevamente.")
        return

    resultados = []

    # 1. Backtracking (1 solución)
    solutions, states, elapsed = n_queens_backtracking(n, find_all=False)
    resultados.append(("Backtracking (1 sol)", elapsed, states, "Sí" if solutions else "No"))

    # 2. Backtracking (todas soluciones) solo para N pequeños
    if n <= 10:
        solutions_all, states_all, elapsed_all = n_queens_backtracking(n, find_all=True)
        resultados.append(("Backtracking (todas)", elapsed_all, states_all, "Sí" if solutions_all else "No"))
    else:
        resultados.append(("Backtracking (todas)", None, None, "N/A"))

    # 3. Las Vegas
    solution_lv, states_lv, elapsed_lv = n_queens_las_vegas(n, timeout=5)
    resultados.append(("Las Vegas", elapsed_lv, states_lv, "Sí" if solution_lv else "No"))

    # 4. Mínimos Conflictos
    solution_mc, states_mc, elapsed_mc = n_queens_min_conflicts(n, timeout=5)
    resultados.append(("Mínimos Conflictos", elapsed_mc, states_mc, "Sí" if solution_mc else "No"))

    print("\nComparativa de algoritmos:")
    print("{:<25} {:<12} {:<20} {:<20}".format("Algoritmo", "Tiempo (s)", "Estados Expandidos", "Solución Encontrada"))
    print("-" * 80)
    for nombre, tiempo, estados, sol in resultados:
        tiempo_str = f"{tiempo:.4f}" if tiempo is not None else "Muy lento"
        estados_str = f"{estados}" if estados is not None else "N/A"
        print("{:<25} {:<12} {:<20} {:<20}".format(nombre, tiempo_str, estados_str, sol))

def menu():
    while True:
        print("\n==== PROBLEMA DE LAS N-REINAS ====")
        print("1. Ejecutar algoritmo individual")
        print("2. Comparar algoritmos")
        print("3. Salir")
        opcion = input("Seleccione una opción [1-3]: ")

        if opcion == "1":
            ejecutar_algoritmo()
        elif opcion == "2":
            comparar_algoritmos()
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# ---------------------------
# Función Principal
# ---------------------------
if __name__ == '__main__':
    menu()
