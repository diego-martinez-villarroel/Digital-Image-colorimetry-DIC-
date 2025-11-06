import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression #regresión lineal para obtener la función calibración y el coeficiente de correlación.

#05/11/2025

#datos a partir de codigo de 3 crop 1 imagen para ROJO METILO 
#Datos para siempre graficar lo mismo, porque por cada corrida en los otros codigos salen valores diferentes.

r = np.array([209.41386667 ,210.28493333 ,213.19173333 ,212.61946667 ,221.6892]) #valores mean para rojo
g = np.array([200.4792 ,194.05773333 ,168.50893333 ,115.5372 ,40.21493333]) #valores mean para verde
b = np.array([216.34506667, 213.22453333, 208.4784, 192.9688, 172.71213333]) #valores mean para azul

x=[0.25,0.5,1,2,4] 

x = np.array(x).reshape(-1, 1)  #https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html

#regresion lineal para rojo
reg0 = LinearRegression().fit(x,r)
print(" El coeficiente de correlacion para rojo es R^2 = ", r2 := reg0.score(x, r)) #operador walrus
print(f"La recta para rojo es y = {reg0.coef_[0]}x + {reg0.intercept_}")
plt.plot(x, reg0.predict(x), color="red")

#regresion lineal para verde
reg1 = LinearRegression().fit(x, g)
print(" El coeficiente de correlacion para verde es R^2 = ", r2 := reg1.score(x, g))
print(f"La recta para verde es y = {reg1.coef_[0]}x + {reg1.intercept_}")
plt.plot(x, reg1.predict(x), color="green")

#regresion lineal para azul
reg2 = LinearRegression().fit(x, b)
print(" El coeficiente de correlacion para azul es R^2 = ", r2 := reg2.score(x, b))
print(f"La recta para azul es y = {reg2.coef_[0]}x + {reg2.intercept_}")
plt.plot(x, reg2.predict(x), color="blue")


plt.scatter(x,r, color= "red") #plot es la idea cuando se use la absorbancia 
plt.scatter(x,g, color="green") 
plt.scatter(x,b,color="blue") #recuerda hacer esto con las otras fotos
plt.xlabel("Concentración (ppm)",fontsize=12, fontweight='bold')
plt.ylabel("Valor RGB",fontsize=12, fontweight='bold')
plt.title("Regresión lineal y scatter para Rojo Metilo",fontsize=12, fontweight='bold')
plt.legend(["Regresión lineal Rojo","Regresión lineal Verde","Regresión lineal Azul",
            "Datos Rojo","Datos Verde","Datos Azul"], loc='best')
plt.savefig("RojoMetilo_regresion3CROP.jpg")
plt.show()

#calcular x a partir de y


def calcular_x_rojo(y):
    m = reg0.coef_[0]
    b = reg0.intercept_
    x = (y - b) / m
    return x

y_dada = float(input("Ingresa un valor de y (rojo): "))
x_calculada = calcular_x_rojo(y_dada)
print(f"Para y = {y_dada}, x = {x_calculada}")

def calcular_x_verde(y):
    m = reg1.coef_[0]
    b = reg1.intercept_
    x = (y - b) / m
    return x

y_dada = float(input("Ingresa un valor de y (verde): "))
x_calculada = calcular_x_verde(y_dada)
print(f"Para y = {y_dada}, x = {x_calculada}")

def calcular_x_azul(y):
    m = reg2.coef_[0]
    b = reg2.intercept_
    x = (y - b) / m
    return x

y_dada = float(input("Ingresa un valor de y (azul): "))
x_calculada = calcular_x_azul(y_dada)
print(f"Para y = {y_dada}, x = {x_calculada}")

#luego la idea es añadir libreria de python q tu le des una imagen, que extraiga los valores mean de r, g, b
#y con esos valores de mean calcule la concentracion usando las funciones de arriba 
