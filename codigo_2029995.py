import pandas as pd
import numpy as np
import networkx as nx
from scipy.stats import norm

# Tiempos en semanas: a (optimista), m (probable), b (pesimista)
actividades = {
    'A': {'pred': [], 'a': 12, 'm': 20, 'b': 40},
    'B': {'pred': ['A'], 'a': 40, 'm': 52, 'b': 80},
    'C': {'pred': ['A'], 'a': 24, 'm': 36, 'b': 60},
    'D': {'pred': ['A'], 'a': 16, 'm': 24, 'b': 45},
    'E': {'pred': ['B', 'C'], 'a': 30, 'm': 45, 'b': 70},
    'F': {'pred': ['D', 'E'], 'a': 12, 'm': 20, 'b': 35},
    'G': {'pred': ['F'], 'a': 8, 'm': 12, 'b': 24},
    'H': {'pred': ['G'], 'a': 6, 'm': 8, 'b': 16},
    'I': {'pred': ['E'], 'a': 52, 'm': 70, 'b': 110},
    'J': {'pred': ['H', 'I'], 'a': 10, 'm': 16, 'b': 28},
    'K': {'pred': ['J'], 'a': 8, 'm': 12, 'b': 20}
}

# Tiempos esperados y varianza
for act, datos in actividades.items():
    a, m, b = datos['a'], datos['m'], datos['b']
    te = (a + 4*m + b) / 6
    var = ((b - a) / 6)**2
    actividades[act]['te'] = te
    actividades[act]['var'] = var
    print(f"Actividad {act}: te = {te:.2f} sem, var = {var:.2f}")

