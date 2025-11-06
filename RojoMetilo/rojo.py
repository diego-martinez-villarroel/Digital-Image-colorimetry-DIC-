import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression #regresión lineal para obtener la función calibración y el coeficiente de correlación.

DatosR=np.loadtxt("Macro1(red).txt",skiprows=1)
DatosG=np.loadtxt("Macro1(green).txt",skiprows=1)
DatosB=np.loadtxt("Macro1(blue).txt",skiprows=1)

r = DatosR[:,2]
g = DatosG[:,2]
b = DatosB[:,2]

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
#plt.savefig("RojoMetilo_regresion.jpg")
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
