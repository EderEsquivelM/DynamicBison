# =================================================================
# Eder Abisai Esquivel Maldonado
# 2029995
# Jueves 23 de abril 2026
# Producto Integrador de Aprendizaje: Investigación de Operaciones
#
# Proyecto PERT para el diseño y lanzamiento al mercado de un nuevo 
# modelo de vehículo eléctrico (Caso 12)
#
# Declaro que este código es de mi autoría y ha sido desarrollado
# bajo los criterios de integridad académica de la FCFM
# =================================================================

import pandas as pd        # Manejo de tablas y DataFrames
import numpy as np         # Operaciones matemáticas (raíz cuadrada)
from scipy.stats import norm  # Distribución normal para calcular probabilidades

# -----------------------------------------------------------------
# 1. DEFINICIÓN DE ACTIVIDADES
# Cada actividad tiene:
#   pred -> lista de actividades que deben terminar antes
#   a    -> tiempo optimista (mejor escenario)
#   m    -> tiempo más probable (escenario normal)
#   b    -> tiempo pesimista (peor escenario)
# Los tiempos estan en semanas
# -----------------------------------------------------------------
actividades = {
    'A': {'desc': 'Definición de Requerimientos y Diseño Conceptual', 'pred': [], 'a': 12, 'm': 20, 'b': 40},
    'B': {'desc': 'Diseño del Tren Motriz y Tren de Potencia', 'pred': ['A'], 'a': 40, 'm': 52, 'b': 80},
    'C': {'desc': 'Desarrollo del Pack de Baterías y Gestión Térmica (BMS)', 'pred': ['A'], 'a': 24, 'm': 36, 'b': 60},
    'D': {'desc': 'Arquitectura de Software y Conectividad (OTA)', 'pred': ['A'], 'a': 16, 'm': 24, 'b': 45},
    'E': {'desc': 'Diseño de Chasis y Carrocería (BIW)', 'pred': ['B', 'C'], 'a': 30, 'm': 45, 'b': 70},
    'F': {'desc': 'Integración de Prototipos Alpha (Mulas de Prueba)', 'pred': ['D', 'E'], 'a': 12, 'm': 20, 'b': 35},
    'G': {'desc': 'Pruebas de Seguridad y Crash Test (NCAP)', 'pred': ['F'], 'a': 8, 'm': 12, 'b': 24},
    'H': {'desc': 'Homologación y Certificación Ambiental (WLTP/EPA)', 'pred': ['G'], 'a': 6, 'm': 8, 'b': 16},
    'I': {'desc': 'Instalación y Utillaje de la Línea de Ensamblaje', 'pred': ['E'], 'a': 52, 'm': 70, 'b': 110},
    'J': {'desc': 'Producción de Pre-serie y Auditoría de Calidad', 'pred': ['H', 'I'], 'a': 10, 'm': 16, 'b': 28},
    'K': {'desc': 'Lanzamiento al Mercado y Logística de Distribución', 'pred': ['J'], 'a': 8, 'm': 12, 'b': 20}
}

# -----------------------------------------------------------------
# 2. TIEMPOS ESPERADOS Y VARIANZA 
# Fórmula PERT:
#   te  = (a + 4m + b) / 6  -> promedio ponderado
#   var = ((b - a) / 6)^2    -> dispersión del tiempo
# Los resultados se agregan al diccionario de cada actividad
# -----------------------------------------------------------------
print("\n===== Análisis de Tiempos Esperados =====")
for act, datos in actividades.items():
    a, m, b = datos['a'], datos['m'], datos['b']
    
    te  = (a + 4*m + b) / 6        # Tiempo esperado
    var = ((b - a) / 6)**2         # Varianza
    
    actividades[act]['te']  = te   # Se guarda en el diccionario
    actividades[act]['var'] = var
    print(f"Actividad {act}: te = {te:.2f} sem, var = {var:.2f}")

# -----------------------------------------------------------------
# 3. PASADA HACIA ADELANTE (ES y EF)
# ES (Early Start)  -> inicio más temprano posible
# EF (Early Finish) -> fin más temprano posible
#
# Regla: ES = máximo EF de todas las predecesoras
#        EF = ES + te
# Si no tiene predecesoras, ES = 0 (inicia al principio)
# -----------------------------------------------------------------
for act in actividades:
    predecesoras = actividades[act]['pred']
    
    if not predecesoras:
        actividades[act]['ES'] = 0  # Primera actividad, empieza en 0
    else:
        # Espera a que termine la predecesora que acabe más tarde
        actividades[act]['ES'] = max([actividades[p]['EF'] for p in predecesoras])
    
    actividades[act]['EF'] = actividades[act]['ES'] + actividades[act]['te']

# La duración total es el EF más grande de todas las actividades
duracionProyecto = max([datos['EF'] for datos in actividades.values()])

# -----------------------------------------------------------------
# 4. PASADA HACIA ATRÁS (LS, LF y Holgura)
# LF (Late Finish) -> fin más tardío sin retrasar el proyecto
# LS (Late Start)  -> inicio más tardío sin retrasar el proyecto
# Holgura          -> tiempo de margen antes de volverse crítica
#
# Regla: LF = mínimo LS de todas las sucesoras
#        LS = LF - te
#        Holgura = LS - ES
# Si no tiene sucesoras, LF = duración total del proyecto
# -----------------------------------------------------------------
for act in reversed(list(actividades.keys())):
    # Busca todas las actividades que dependen de 'act'
    sucesoras = [k for k, v in actividades.items() if act in v['pred']]
    
    if not sucesoras:
        actividades[act]['LF'] = duracionProyecto  # Última actividad
    else:
        # Debe terminar antes de que empiece la sucesora más urgente
        actividades[act]['LF'] = min([actividades[s]['LS'] for s in sucesoras])
    
    actividades[act]['LS']      = actividades[act]['LF'] - actividades[act]['te']
    actividades[act]['Holgura'] = actividades[act]['LS'] - actividades[act]['ES']

# -----------------------------------------------------------------
# 5. RUTA CRÍTICA
# Son las actividades con Holgura = 0
# Se usa < 0.001 como tolerancia por errores de punto flotante
# Un retraso en cualquiera de estas actividades retrasa todo el proyecto
# -----------------------------------------------------------------
rutaCritica = [act for act, datos in actividades.items() if datos['Holgura'] < 0.001]

print("\n===== Ruta Crítica y Holguras =====")
# Se seleccionan solo las columnas relevantes para mostrar
df_resultados = pd.DataFrame(actividades).T[['desc', 'ES', 'EF', 'LS', 'LF', 'Holgura']]
print(df_resultados.round(2))

print(f"\nDuración total esperada del proyecto: {duracionProyecto:.2f} semanas")
print(f"Ruta Crítica: {' -> '.join(rutaCritica)}")

# -----------------------------------------------------------------
# 6. ANÁLISIS PROBABILÍSTICO 
# Se calcula la probabilidad de terminar antes de la meta (156 sem)
#
# varianzaCritica -> suma de varianzas solo de actividades críticas
# desvStd         -> desviación estándar = raíz de la varianza total
# z               -> cuántas desviaciones estándar está la meta
#                   del tiempo esperado (valor estandarizado)
# norm.cdf(z)     -> área bajo la curva normal a la izquierda de z
#                   = probabilidad de terminar en <= meta semanas
# -----------------------------------------------------------------
print("\n===== Análisis Probabilístico =====")
varianzaCritica = sum([actividades[act]['var'] for act in rutaCritica])
desvStd         = np.sqrt(varianzaCritica)
meta            = 156  # Semanas objetivo del proyecto

z            = (meta - duracionProyecto) / desvStd  # Puntaje Z
probabilidad = norm.cdf(z)                          # Probabilidad acumulada

print(f"Varianza de la Ruta Crítica: {varianzaCritica:.2f}")
print(f"Probabilidad de éxito (terminar en {meta} semanas): {probabilidad*100:.2f}%")