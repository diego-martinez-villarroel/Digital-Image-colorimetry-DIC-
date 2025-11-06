import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#ESTADISTICAS PARA FESCN
#CONCENTRACIÓN NOMINAL (real) 
c_nominal = np.array([2*10**-5,4*10**-5,6*10**-5,8*10**-5,10*10**-5]) # total r,g,b 

r = np.array([210.46386667, 212.92706667, 213.6464, 214.89786667, 214.47213333]) #valores mean para rojo

g = np.array([199.86826667, 194.98466667, 178.09013333, 161.94706667, 143.12733333]) #valores mean para verde

b = np.array([204.59746667, 175.63706667, 148.96       , 125.08413333, 107.46466667]) #valores mean para azul


cr = [] #concentracion rojo, verde, azul 
cv = []
ca = []

for i in r: #calculo de concentracion a partir de mean para rojo (y-b)/m = x
    x = (i - 210.2853) / 49936.6667
    cr.append(x) #guarda valor en la lista creada

for i in g: #calculo de concentracion a partir de mean para verde
    x = (i - 219.5593) / -732597.3333
    cv.append(x) #guarda valor en la lista creada

for i in b: #calculo de concentracion a partir de mean para azul
    x = (i - 225.7942) / -1224092.6667
    ca.append(x) #guarda valor en la lista creada

# Convertir listas a arrays
#si bien para cada recta tenemos una concentracion predicha distinta, para tener un unico valor de concentracion predicha por cada punto, se saca el promedio de las 3 rectas
conc_predicha = (np.array(cr)+np.array(cv)+np.array(ca))/3

print("Concentracion nominal:", c_nominal)

print("Concentracion predicha promedio:", conc_predicha)

print("error absoluto cn - cp en cada dato: +-", err_abs := c_nominal - conc_predicha) #error absoluto (Residuos)

print("error medio absoluto +-:", np.mean(np.abs(err_abs))) 

print("desviacion estandar del error absoluto std (cn - cp):", np.std(err_abs, ddof=1)) #revisar bitacora explicacion ddof=1

print("error porcentual medio (relativo):", np.mean(np.abs(err_abs/c_nominal))*100, "%") #error relativo

# ============================================================================
# ANÁLISIS DE VARIANZA (ANOVA)
# ============================================================================

print("\n" + "="*80)
print("ANÁLISIS DE VARIANZA (ANOVA)")
print("="*80)

# Número de observaciones y parámetros
n = len(c_nominal)
p = 1  # número de predictores

# Media de concentración nominal
media_cn = np.mean(c_nominal)

# SUMA DE CUADRADOS TOTAL (SST)
ss_total = np.sum((c_nominal - media_cn)**2)

# SUMA DE CUADRADOS RESIDUAL (SSR o SSE)
ss_residual = np.sum(err_abs**2)

# SUMA DE CUADRADOS DE REGRESIÓN (SSM)
ss_regresion = np.sum((conc_predicha - media_cn)**2)

print("\n--- PASO 1: SUMAS DE CUADRADOS ---")
print(f"SS Total (SST):      {ss_total:.10f}")
print(f"  → Variabilidad total de los datos")
print(f"\nSS Regresión (SSM):  {ss_regresion:.10f}")
print(f"  → Variabilidad EXPLICADA por el modelo")
print(f"\nSS Residual (SSR):   {ss_residual:.10f}")
print(f"  → Variabilidad NO explicada (error)")

# Verificación: SST = SSM + SSR
print(f"\nVerificación: SST = SSM + SSR")
print(f"  {ss_total:.10f} = {ss_regresion:.10f} + {ss_residual:.10f}")
print(f"  Diferencia: {abs(ss_total - (ss_regresion + ss_residual)):.15f}")

# GRADOS DE LIBERTAD
gl_total = n - 1
gl_regresion = p
gl_residual = n - p - 1

print("\n--- PASO 2: GRADOS DE LIBERTAD ---")
print(f"gl Total:      {gl_total}")
print(f"gl Regresión:  {gl_regresion}")
print(f"gl Residual:   {gl_residual}")

# CUADRADOS MEDIOS (Mean Squares)
cm_regresion = ss_regresion / gl_regresion
cm_residual = ss_residual / gl_residual

print("\n--- PASO 3: CUADRADOS MEDIOS ---")
print(f"MS Regresión (MSM): {cm_regresion:.10f}")
print(f"MS Residual (MSE):  {cm_residual:.10f}")

# ESTADÍSTICO F
f_estadistico = cm_regresion / cm_residual

print("\n--- PASO 4: ESTADÍSTICO F ---")
print(f"F = {f_estadistico:.10f}")

# VALOR P
p_valor = 1 - stats.f.cdf(f_estadistico, gl_regresion, gl_residual)

print("\n--- PASO 5: VALOR P Y CONCLUSIÓN ---")
print(f"p-valor = {p_valor:.10f}")

if p_valor < 0.05:
    print(f"\n✓ CONCLUSIÓN: p < 0.05 → El modelo ES SIGNIFICATIVO")
else:
    print(f"\n✗ CONCLUSIÓN: p ≥ 0.05 → El modelo NO es significativo")

# ============================================================================
# TABLA ANOVA
# ============================================================================

print("\n" + "="*120)
print("TABLA ANOVA")
print("="*120)
print(f"{'Fuente':<15} {'|SS suma de cuadrados|':>2} {'|gl grados de libertad|':<8} {'|MS cuadrados medios|':>22} {'|F estadistico|':>18} {'|valor-p|':>16}")
print("-"*120)
print(f"{'Regresión':<15} {ss_regresion:<25.10f} {gl_regresion:<30} {cm_regresion:<22.10f} {f_estadistico:<18.6f} {p_valor:<16.10f}")
print(f"{'Residual':<15} {ss_residual:<25.10f} {gl_residual:<30} {cm_residual:<22.10f}")
print(f"{'Total':<15} {ss_total:<25.10f} {gl_total:<30}")
print("="*120)