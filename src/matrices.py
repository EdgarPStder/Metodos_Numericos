import tkinter as tk
from tkinter import messagebox
import numpy as np

# Función para leer una matriz desde un área de texto
def leer_matriz(area, nombre="Matriz"):
    try:
        texto = area.get("1.0", tk.END).strip()
        if not texto:
            raise ValueError(f"{nombre} está vacía.")
        filas = texto.split("\n")
        matriz = [list(map(float, fila.split())) for fila in filas]
        return np.array(matriz)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return None

# Operaciones básicas
def sumar_matrices(A, B):
    if A.shape != B.shape:
        messagebox.showerror("Error", "Las matrices deben tener las mismas dimensiones para sumarlas.")
        return None
    return A + B

def restar_matrices(A, B):
    if A.shape != B.shape:
        messagebox.showerror("Error", "Las matrices deben tener las mismas dimensiones para restarlas.")
        return None
    return A - B

def multiplicar_matrices(A, B):
    if A.shape[1] != B.shape[0]:
        messagebox.showerror("Error", "El número de columnas de A debe coincidir con el número de filas de B.")
        return None
    return A @ B

def mostrar_operacion(operacion):
    resultado.config(state="normal")
    resultado.delete("1.0", tk.END)

    A = leer_matriz(matrizA, "Matriz A")
    B = leer_matriz(matrizB, "Matriz B")

    if A is None or B is None:
        resultado.config(state="disabled")
        return

    if operacion == "suma":
        R = sumar_matrices(A, B)
    elif operacion == "resta":
        R = restar_matrices(A, B)
    elif operacion == "multiplicacion":
        R = multiplicar_matrices(A, B)
    else:
        R = None

    if R is not None:
        texto = "\n".join(" ".join(f"{val:.2f}" for val in fila) for fila in R)
        resultado.insert(tk.END, texto)

    resultado.config(state="disabled")

# Funciones de operaciones individuales
def operar_matriz(area, nombre, operacion):
    resultado.config(state="normal")
    resultado.delete("1.0", tk.END)
    A = leer_matriz(area, nombre)
    if A is None:
        resultado.config(state="disabled")
        return

    try:
        if operacion == "det":
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz debe ser cuadrada para calcular la determinante.")
            valor = np.linalg.det(A)
            resultado.insert(tk.END, f"Determinante de {nombre}: {valor:.2f}")

        elif operacion == "inv":
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz debe ser cuadrada para invertirla.")
            inversa = np.linalg.inv(A)
            texto = "\n".join(" ".join(f"{val:.2f}" for val in fila) for fila in inversa)
            resultado.insert(tk.END, f"Inversa de {nombre}:\n{texto}")

        elif operacion == "invgj":
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz debe ser cuadrada para invertirla.")
            n = A.shape[0]
            AI = np.hstack([A, np.identity(n)])
            for i in range(n):
                if AI[i][i] == 0:
                    for j in range(i + 1, n):
                        if AI[j][i] != 0:
                            AI[[i, j]] = AI[[j, i]]
                            break
                AI[i] = AI[i] / AI[i][i]
                for j in range(n):
                    if i != j:
                        AI[j] = AI[j] - AI[i] * AI[j][i]
            inv = AI[:, n:]
            texto = "\n".join(" ".join(f"{val:.2f}" for val in fila) for fila in inv)
            resultado.insert(tk.END, f"Inversa (Gauss-Jordan) de {nombre}:\n{texto}")

        elif operacion == "sistema_gj":
            if A.shape[1] != A.shape[0] + 1:
                raise ValueError("Debe ingresar una matriz aumentada (n x n+1).")
            n = A.shape[0]
            M = A.astype(float)
            for i in range(n):
                if M[i][i] == 0:
                    for j in range(i + 1, n):
                        if M[j][i] != 0:
                            M[[i, j]] = M[[j, i]]
                            break
                M[i] = M[i] / M[i][i]
                for j in range(n):
                    if i != j:
                        M[j] = M[j] - M[i] * M[j][i]
            soluciones = M[:, -1]
            texto = "\n".join(f"x{i+1} = {sol:.2f}" for i, sol in enumerate(soluciones))
            resultado.insert(tk.END, f"Solución (Gauss-Jordan) de {nombre}:\n{texto}")

        elif operacion == "sistema_gs":
            if A.shape[1] != A.shape[0] + 1:
                raise ValueError("Debe ingresar una matriz aumentada (n x n+1).")
            n = A.shape[0]
            M = A.astype(float)
            for i in range(n):
                for j in range(i + 1, n):
                    factor = M[j][i] / M[i][i]
                    M[j] = M[j] - factor * M[i]
            x = np.zeros(n)
            for i in reversed(range(n)):
                x[i] = (M[i][-1] - np.dot(M[i][i+1:n], x[i+1:n])) / M[i][i]
            texto = "\n".join(f"x{i+1} = {val:.2f}" for i, val in enumerate(x))
            resultado.insert(tk.END, f"Solución (Gauss simple) de {nombre}:\n{texto}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    resultado.config(state="disabled")

def limpiar():
    resultado.config(state="normal")
    resultado.delete("1.0", tk.END)
    resultado.config(state="disabled")

# Ventana principal
root = tk.Tk()
root.title("Calculadora de Matrices")
root.geometry("1000x600")

frame_grid = tk.Frame(root)
frame_grid.pack(pady=10)

#función para crear paneles de entrada de matrices
def panel_matriz(titulo, col):
    tk.Label(frame_grid, text=titulo, font=("Arial", 14)).grid(row=0, column=col, padx=10, pady=5)
    area = tk.Text(frame_grid, height=10, width=30, font=("Arial", 12))
    area.grid(row=1, column=col, padx=10, pady=5)
    return area


# Paneles de entrada para matrices A y B
matrizA = panel_matriz("Matriz A:", 0)
matrizB = panel_matriz("Matriz B:", 2)

#panel resultado
tk.Label(frame_grid, text="Resultado:", font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=5)
resultado = tk.Text(frame_grid, height=10, width=30, font=("Arial", 12), state="disabled")
resultado.grid(row=1, column=1, padx=10, pady=5)



# Botones centrales

tk.Button(frame_grid, text="Sumar", width=15, font=("Arial", 12),
          command=lambda: mostrar_operacion("suma")).grid(row=2, column=1, padx=10, pady=5)

tk.Button(frame_grid, text="Restar", width=15, font=("Arial", 12),
          command=lambda: mostrar_operacion("resta")).grid(row=3, column=1, padx=10, pady=5)

tk.Button(frame_grid, text="Multiplicar", width=15, font=("Arial", 12),
          command=lambda: mostrar_operacion("multiplicacion")).grid(row=4, column=1, padx=10, pady=5)

tk.Button(frame_grid, text="Limpiar", width=15, font=("Arial", 12),
          command=limpiar).grid(row=5, column=1, padx=10, pady=5)

# Botones para matriz A
frame_izquierda = tk.Frame(root)
frame_izquierda.pack(padx=20)
tk.Button(frame_grid, text="Determinante A", width=20, font=("Arial", 12),
          command=lambda: operar_matriz(matrizA, "Matriz A", "det")).grid(row=2, column=0, padx=10)
tk.Button(frame_grid, text="Inversa A", width=20, font=("Arial", 12),
          command=lambda: operar_matriz(matrizA, "Matriz A", "inv")).grid(row=3, column=0, padx=10)
tk.Button(frame_grid, text="Inversa A (Gauss-Jordan)", width=20, font=("Arial", 12),
          command=lambda: operar_matriz(matrizA, "Matriz A", "invgj")).grid(row=4, column=0, padx=10)
tk.Button(frame_grid, text="Sistema A (Gauss-Jordan)", width=20, font=("Arial", 12),
            command=lambda: operar_matriz(matrizA, "Matriz A", "sistema_gj")).grid(row=5, column=0, padx=10)
tk.Button(frame_grid, text="Sistema A (Gauss simple)", width=20, font=("Arial", 12),
            command=lambda: operar_matriz(matrizA, "Matriz A", "sistema_gs")).grid(row=6, column=0, padx=10)

# Botones para matriz B
frame_derecha = tk.Frame(root)
frame_derecha.pack(side=tk.RIGHT, padx=20)
tk.Button(frame_grid, text="Determinante B", width=20, font=("Arial", 12),
          command=lambda: operar_matriz(matrizB, "Matriz B", "det")).grid(row=2, column=2, padx=10)
tk.Button(frame_grid, text="Inversa B", width=20, font=("Arial", 12),
          command=lambda: operar_matriz(matrizB, "Matriz B", "inv")).grid(row=3, column=2, padx=10)
tk.Button(frame_grid, text="Inversa B (Gauss-Jordan)", width=20, font=("Arial", 12),
          command=lambda: operar_matriz(matrizB, "Matriz B", "invgj")).grid(row=4, column=2, padx=10)
tk.Button(frame_grid, text="Sistema B (Gauss-Jordan)", width=20, font=("Arial", 12),
            command=lambda: operar_matriz(matrizB, "Matriz B", "sistema_gj")).grid(row=5, column=2, padx=10)
tk.Button(frame_grid, text="Sistema B (Gauss simple)", width=20, font=("Arial", 12),
            command=lambda: operar_matriz(matrizB, "Matriz B", "sistema_gs")).grid(row=6, column=2, padx=10)

root.mainloop()