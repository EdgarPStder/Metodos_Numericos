import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Evaluar la función ingresada por el usuario
def safe_eval_func(func_str, x):
    allowed_names = {
        "x": x,
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
        "abs": abs,
        "pi": np.pi,
        "e": np.e,
    }
    try:
        return eval(func_str, {"__builtins__": None}, allowed_names)
    except Exception as ex:
        raise ValueError(f"Error al evaluar la función: {ex}")

# Método de la secante
def secant_iterations(func_str, x0, x1, e, max_iter=100):
    iterations = []
    try:
        f_x0 = safe_eval_func(func_str, x0)
        f_x1 = safe_eval_func(func_str, x1)
    except Exception as err:
        messagebox.showerror("Error", f"No se pudo evaluar la función en los puntos iniciales: {err}")
        return None

    for i in range(max_iter):
        if f_x1 - f_x0 == 0:
            messagebox.showerror("Error", "División por cero en la fórmula de la secante.")
            return None

        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        f_x2 = safe_eval_func(func_str, x2)

        iterations.append({"x0": x0, "x1": x1, "x2": x2, "f(x2)": f_x2})

        if abs(f_x2) < e:
            break

        x0, f_x0 = x1, f_x1
        x1, f_x1 = x2, f_x2

    return iterations

# Ejecutar método de la secante y mostrar resultados
def run_secant():
    func_str = entry_func.get()
    try:
        x0 = float(entry_a.get())
        x1 = float(entry_b.get())
        e = float(entry_e.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa números válidos en x0, x1 y e.")
        return
    
    iter_data = secant_iterations(func_str, x0, x1, e)
    if iter_data is None or len(iter_data) == 0:
        return
    
    for row in tree.get_children():
        tree.delete(row)
        
    for i, it in enumerate(iter_data, 1):
        tree.insert("", "end", values=(i, f"{it['x0']:.6f}", f"{it['x1']:.6f}", f"{it['x2']:.6f}", f"{it['f(x2)']:.6f}"))
    
    raiz = iter_data[-1]['x2']
    label_result.config(text=f"La raíz aproximada es: {raiz:.8f}")
    
    x_vals = np.linspace(x0, x1, 400)
    try:
        y_vals = safe_eval_func(func_str, x_vals)
    except Exception as err:
        messagebox.showerror("Error", f"No se pudo graficar la función: {err}")
        return
    
    ax.clear()
    ax.plot(x_vals, y_vals, label=f"f(x) = {func_str}")
    ax.axhline(0, color='black', linewidth=0.7)
    ax.axvline(raiz, color='red', linestyle='--', label=f"Raíz ~ {raiz:.6f}")
    ax.legend()
    ax.grid(True)
    canvas.draw()

# Ventana principal
root = tk.Tk()
root.title("Método de la Secante con Función Personalizada")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)
#Cajas de entrada para la función
tk.Label(frame_inputs, text="Función f(x):").grid(row=0, column=0)
entry_func = tk.Entry(frame_inputs, width=40)
entry_func.grid(row=0, column=1, columnspan=5)
entry_func.insert(0, "x**3 - x**2 + 2")
#Cajas de entrada para el punto x0
tk.Label(frame_inputs, text="x0:").grid(row=1, column=0)
entry_a = tk.Entry(frame_inputs, width=10)
entry_a.grid(row=1, column=1)
entry_a.insert(0, "-10")
#Cajas de entrada para el punto x1
tk.Label(frame_inputs, text="x1:").grid(row=1, column=2)
entry_b = tk.Entry(frame_inputs, width=10)
entry_b.grid(row=1, column=3)
entry_b.insert(0, "10")
#Cajas de entrada para el error
tk.Label(frame_inputs, text="Error e:").grid(row=1, column=4)
entry_e = tk.Entry(frame_inputs, width=10)
entry_e.grid(row=1, column=5)
entry_e.insert(0, "0.01")
#Botón para calcular la raíz
btn_calc = tk.Button(root, text="Calcular Raíz", command=run_secant)
btn_calc.pack(pady=5)
#Tabla para mostrar iteraciones
columns = ("#", "x0", "x1", "x2", "f(x2)")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='center')
tree.pack(pady=10)
#Etiqueta para mostrar el resultado
label_result = tk.Label(root, text="La raíz aproximada es: ")
label_result.pack(pady=5)
#Configuración de la gráfica
fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
