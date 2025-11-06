#03_09_2025 

#El primer corchete (x[0]) accede a la primera fila (que es un array).
#El segundo corchete (x[0][0]) accede al valor dentro de esa fila.

#La f en la línea 20 indica que es un f-string (formatted string literal) en Python.
#Esto permite insertar valores de variables directamente dentro del texto usando {}.

# Para cada color, calcula x usando la ecuación de la recta y = mx + b
#print("\nValores de x calculados para cada dato rojo:")
#for val in r:
#    x_calc = (val - reg0.intercept_) / reg0.coef_[0]
#    print(f"Para y = {val:.3f}, x = {x_calc:.8f}")

#print("\nValores de x calculados para cada dato verde:")
#for val in g:
#    x_calc = (val - reg1.intercept_) / reg1.coef_[0]
#    print(f"Para y = {val:.3f}, x = {x_calc:.8f}")

#print("\nValores de x calculados para cada dato azul:")
#for val in b:
#    x_calc = (val - reg2.intercept_) / reg2.coef_[0]
#    print(f"Para y = {val:.3f}, x = {x_calc:.8f}")

import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression 

x=[1,2,3,4,5,6,7,8,9,10]
y=[2,4,6,8,10,12,14,16,18,20]

x = np.array(x).reshape(-1, 1)
y = np.array(y)

reg = LinearRegression().fit(x, y)
print(f"La recta es : y = {reg.coef_[0]}x + {reg.intercept_}")
plt.scatter(x, y)
plt.plot(x, reg.predict(x), color="red")
plt.show()

#el ajuste funciona. ahora por que me da una recta tan rara con pendiente horrible no tengo idea en el otro
