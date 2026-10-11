# Métodos Numéricos con interfaz gráfica

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-3776AB?style=flat-square)

Implementaciones de métodos numéricos clásicos en **Python**, cada una con su propia **interfaz gráfica en Tkinter**. Se escribe la función, se configuran los parámetros y el programa muestra la tabla de iteraciones paso a paso y la gráfica de la función.

Desarrollado para la materia **Métodos Numéricos** (Ingeniería en Sistemas Computacionales, UAT — UAM Mante).

---

## Métodos incluidos

### Búsqueda de raíces

| Programa | Método | Entradas | Salida |
|---|---|---|---|
| [`biseccion.py`](src/biseccion.py) | Bisección | f(x), intervalo [a, b], error | Tabla de iteraciones, raíz aproximada y gráfica |
| [`secante.py`](src/secante.py) | Secante | f(x), x₀, x₁, error | Tabla de iteraciones, raíz aproximada y gráfica |
| [`newton_raphson.py`](src/newton_raphson.py) | Newton-Raphson | f(x), f'(x), x₀, error | Tabla de iteraciones, raíz aproximada y gráfica |

Las funciones se escriben con sintaxis de Python, por ejemplo `x**3 - 2*x - 5` o `exp(-x) - x`. Están disponibles `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `abs`, `pi` y `e`. La expresión se evalúa en un entorno restringido (sin acceso a funciones internas de Python).

### Álgebra lineal — [`matrices.py`](src/matrices.py)

Calculadora para dos matrices A y B de cualquier tamaño:

- **Operaciones básicas:** suma, resta y multiplicación.
- **Por matriz:** determinante, inversa e inversa por Gauss-Jordan.
- **Sistemas de ecuaciones lineales:** eliminación de Gauss simple y Gauss-Jordan (la última columna de la matriz se toma como vector de términos independientes).

---

## Instalación y uso

**Requisitos:** Python 3.10 o superior (Tkinter viene incluido en Windows y macOS; en Linux instala `python3-tk`).

```bash
git clone https://github.com/EdgarPStder/Metodos_Numericos.git
cd Metodos_Numericos

python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

Ejecuta el método que quieras:

```bash
python src/biseccion.py
python src/secante.py
python src/newton_raphson.py
python src/matrices.py
```

## Estructura

```
.
├── src/
│   ├── biseccion.py
│   ├── secante.py
│   ├── newton_raphson.py
│   └── matrices.py
├── requirements.txt
└── README.md
```

---

## Autor

**Edgar Gael Pesina Santander** — Ingeniería en Sistemas Computacionales, Universidad Autónoma de Tamaulipas.
GitHub: [@EdgarPStder](https://github.com/EdgarPStder)

## Licencia

Código bajo licencia [MIT](LICENSE).
