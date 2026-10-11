import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Evaluar función segura
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

# Método Newton-Raphson
def newton_raphson_iterations(func_str, deriv_str, x0, e, max_iter=100):
    iterations = []
    for i in range(max_iter):
        try:
            fx = safe_eval_func(func_str, x0)
            dfx = safe_eval_func(deriv_str, x0)
        except Exception as err:
            messagebox.showerror("Error", f"Error al evaluar en x = {x0}: {err}")
            return None
        
        if dfx == 0:
            messagebox.showerror("Error", f"Derivada cero en x = {x0}, no se puede continuar.")
            return None

        x1 = x0 - fx / dfx
        iterations.append({"x": x0, "f(x)": fx, "f'(x)": dfx})

        if abs(fx) < e:
            break

        x0 = x1
    return iterations

# Ejecutar Newton-Raphson
def run_newton_raphson():
    func_str = entry_func.get()
    deriv_str = entry_deriv.get()
    try:
        x0 = float(entry_x0.get())
        e = float(entry_e.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")
        return

    iter_data = newton_raphson_iterations(func_str, deriv_str, x0, e)
    if iter_data is None or len(iter_data) == 0:
        return

    for row in tree.get_children():
        tree.delete(row)

    for i, it in enumerate(iter_data, 1):
        tree.insert("", "end", values=(i, f"{it['x']:.6f}", f"{it['f(x)']:.6f}", f"{it['f\'(x)']:.6f}"))

    raiz = iter_data[-1]['x']
    label_result.config(text=f"La raíz aproximada es: {raiz:.8f}")

    x_vals = np.linspace(x0 - 10, x0 + 10, 400)
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

# Interfaz principal
root = tk.Tk()
root.title("Método de Newton-Raphson con Función Personalizada")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)
#Cajas de entrada para la función
tk.Label(frame_inputs, text="Función f(x):").grid(row=0, column=0)
entry_func = tk.Entry(frame_inputs, width=40)
entry_func.grid(row=0, column=1, columnspan=4)
entry_func.insert(0, "x**3 - x**2 + 2")
#Cajas de entrada para la derivada
tk.Label(frame_inputs, text="Derivada f'(x):").grid(row=1, column=0)
entry_deriv = tk.Entry(frame_inputs, width=40)
entry_deriv.grid(row=1, column=1, columnspan=4)
entry_deriv.insert(0, "3*x**2 - 2*x")
#Cajas de entrada para el punto inicial x0
tk.Label(frame_inputs, text="x0:").grid(row=2, column=0)
entry_x0 = tk.Entry(frame_inputs, width=10)
entry_x0.grid(row=2, column=1)
entry_x0.insert(0, "1")
#Cajas de entrada para el error
tk.Label(frame_inputs, text="Error e:").grid(row=2, column=2)
entry_e = tk.Entry(frame_inputs, width=10)
entry_e.grid(row=2, column=3)
entry_e.insert(0, "0.01")
#Botón para calcular la raíz
btn_calc = tk.Button(root, text="Calcular Raíz", command=run_newton_raphson)
btn_calc.pack(pady=5)
#Tabla para mostrar iteraciones
columns = ("#", "x_n", "f(x_n)", "f'(x_n)")
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
