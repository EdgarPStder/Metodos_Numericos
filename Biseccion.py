import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Evaluar la función ingresada por el usuario, con x como variable
def safe_eval_func(func_str, x):
    # Definimos un entorno seguro para eval
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

def bisection_iterations(func_str, a, b, e):
    iterations = []
    try:
        fa = safe_eval_func(func_str, a)
        fb = safe_eval_func(func_str, b)
    except Exception as err:
        messagebox.showerror("Error", f"No se pudo evaluar la función en los extremos: {err}")
        return None

    if fa * fb >= 0:
        messagebox.showinfo("Error", "La raíz no se encuentra en el intervalo o la función no cambia de signo.")
        return None

    while (b - a) > e:
        c = (a + b) / 2
        try:
            fc = safe_eval_func(func_str, c)
        except Exception as err:
            messagebox.showerror("Error", f"Error al evaluar la función en c={c}: {err}")
            return None
        iterations.append({"a": a, "b": b, "c": c, "f(c)": fc})
        if fc == 0:
            break
        elif fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    return iterations

def run_bisection():
    func_str = entry_func.get()
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        e = float(entry_e.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa números válidos en a, b y e.")
        return
    
    iter_data = bisection_iterations(func_str, a, b, e)
    if iter_data is None or len(iter_data) == 0:
        return
    
    # Limpiar tabla
    for row in tree.get_children():
        tree.delete(row)
        
    # Llenar tabla con iteraciones
    for i, it in enumerate(iter_data, 1):
        tree.insert("", "end", values=(i, f"{it['a']:.6f}", f"{it['b']:.6f}", f"{it['c']:.6f}", f"{it['f(c)']:.6f}"))
    
    raiz = iter_data[-1]['c']
    label_result.config(text=f"La raíz aproximada es: {raiz:.8f}")
    
    # Graficar la función
    x_vals = np.linspace(a, b, 400)
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
root.title("Método de Bisección con Función Personalizada")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)
#Caja de entrada para la función
tk.Label(frame_inputs, text="Función f(x):").grid(row=0, column=0)
entry_func = tk.Entry(frame_inputs, width=40)
entry_func.grid(row=0, column=1, columnspan=5)
entry_func.insert(0, "x**3 - x**2 + 2")
#Cajas de entrada para el punto a
tk.Label(frame_inputs, text="a:").grid(row=1, column=0)
entry_a = tk.Entry(frame_inputs, width=10)
entry_a.grid(row=1, column=1)
entry_a.insert(0, "-10")
#Cajas de entrada para el punto b
tk.Label(frame_inputs, text="b:").grid(row=1, column=2)
entry_b = tk.Entry(frame_inputs, width=10)
entry_b.grid(row=1, column=3)
entry_b.insert(0, "10")
#Caja de entrada para el error
tk.Label(frame_inputs, text="Error e:").grid(row=1, column=4)
entry_e = tk.Entry(frame_inputs, width=10)
entry_e.grid(row=1, column=5)
entry_e.insert(0, "0.01")
# Botón para calcular la raíz
btn_calc = tk.Button(root, text="Calcular Raíz", command=run_bisection)
btn_calc.pack(pady=5)
# Tabla para mostrar las iteraciones
columns = ("#", "a", "b", "c", "f(c)")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='center')
tree.pack(pady=10)
# Etiqueta para mostrar el resultado
label_result = tk.Label(root, text="La raíz aproximada es: ")
label_result.pack(pady=5)
# Configuración de la gráfica
fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()