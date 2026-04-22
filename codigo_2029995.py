import pandas as pd
import numpy as np
import networkx as nx
from scipy.stats import norm

# Definición de Datos
# Tiempos en semanas: a (optimista), m (probable), b (pesimista)
actividades = {
    'ID': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
    'Predecesoras': [[], ['A'], ['A'], ['A'], ['B', 'C'], ['D', 'E'], ['F'], ['G'], ['E'], ['H', 'I'], ['J']],
    'a': [12, 40, 24, 16, 30, 12, 8, 6, 52, 10, 8],
    'm': [20, 52, 36, 24, 45, 20, 12, 8, 70, 16, 12],
    'b': [40, 80, 60, 45, 70, 35, 24, 16, 110, 28, 20]
}

df = pd.DataFrame(actividades)

# Cálculos
# Tiempo Esperado (te) y Varianza (var)
df['te'] = (df['a'] + 4*df['m'] + df['b']) / 6
df['var'] = ((df['b'] - df['a']) / 6)**2

print("--- Tabla de Tiempos Esperados ---")
print(df[['ID', 'te', 'var']].round(2))


