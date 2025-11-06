import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#ESTADISTICAS PARA ROJO METILO 
#CONCENTRACIÓN NOMINAL (real) 
c_nominal = np.array([0.25, 0.5, 1, 2, 4]) # total r,g,b 

r = np.array([209.41386667 ,210.28493333 ,213.19173333 ,212.61946667 ,221.6892]) #valores mean para rojo
g = np.array([200.4792 ,194.05773333 ,168.50893333 ,115.5372 ,40.21493333]) #valores mean para verde
b = np.array([216.34506667, 213.22453333, 208.4784, 192.9688, 172.71213333]) #valores mean para azul


cr = [] #concentracion rojo, verde, azul 
cv = []
ca = []

#recta x = (y-b)/m 
for i in r: #calculo de concentracion a partir de mean para rojo
    x = (i - 208.6857) / 3.0672
    cr.append(x) #guarda valor en la lista creada

for i in g: #calculo de concentracion a partir de mean para verde
    x = (i - 211.5171) / -43.7145
    cv.append(x) #guarda valor en la lista creada

for i in b: #calculo de concentracion a partir de mean para azul
    x = (i - 219.0486) / -11.8083
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