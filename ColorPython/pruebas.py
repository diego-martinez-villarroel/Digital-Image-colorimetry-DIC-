import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression #regresión lineal para obtener la función calibración y el coeficiente de correlación.
from PIL import Image
import os

#prueba con rojo metilo 25/09/2025 - 27/09/2025

#cuadrado predefinido y asi posicionar en la parte que quiero para recortar la imagen, para que solo se vea lo que necesito.


def most_common_used_color(img): #funcion para obtener el mean de r,g,b de una imagen
    # Get width and height of Image
    width, height = img.size
 
    # Initialize Variable
    r_total = g_total = b_total = 0
    count = 0
 
    # Iterate through each pixel
    for x in range(0, width):
        for y in range(0, height):
            # r,g,b value of pixel
            r, g, b = img.getpixel((x, y))
 
            r_total += r
            g_total += g
            b_total += b
            count += 1
 
    return (r_total/count, g_total/count, b_total/count)

imagenes= [r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO01B.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO02B.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO03B.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO04B.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO05B.jpg"]
#introducir las rutas de las imagenes que se quieren analizar

rval, gval, bval = [], [], [] #listas para guardar los valores de r,g,b a futuro

for i in imagenes:
    img = Image.open(i).convert('RGB') #abrir y convertir la imagen a RGB (split channels?)
    img_resized = img.resize((50, 50)) #redimensionar la imagen 
    common_color = most_common_used_color(img_resized) #le aplicas la funcion a la imagen redimensionada
    rval.append(common_color[0])
    gval.append(common_color[1])
    bval.append(common_color[2])
    nombre = os.path.basename(i) #para mostrar solo el nombre de la imagen y no toda la ruta
    #Ahora mostrare la imagen redimensionada para comprobar visualmente como queda
    plt.imshow(img_resized)
    plt.title(f"Imagen redimensionada: {nombre}")
    plt.show()
    print(f"Los colores de la imagen {nombre} son R,G,B en orden {common_color}")

#Un f-string permite incrustar variables o expresiones directamente dentro de la cadena usando llaves { }.

# Convertir listas a arrays
r = np.array(rval)
g = np.array(gval)
b = np.array(bval) #basicamente me deja los datos como los txt que tenia para poder hacer el ajuste lineal

print(r,g,b)

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
plt.scatter(x,b,color="blue") #scatter como tal
#plt.savefig("RojoMetilo.jpg")
plt.show()

#calcular x a partir de y 01/10 todavia no es necesario.

# def calcular_x_rojo(y):
#     m = reg0.coef_[0]
#     b = reg0.intercept_
#     x = (y - b) / m
#     return x
#
# y_dada = float(input("Ingresa un valor de y (rojo): "))
# x_calculada = calcular_x_rojo(y_dada)
# print(f"Para y = {y_dada}, x = {x_calculada}")
#
# def calcular_x_verde(y):
#     m = reg1.coef_[0]
#     b = reg1.intercept_
#     x = (y - b) / m
#     return x
#
# y_dada = float(input("Ingresa un valor de y (verde): "))
# x_calculada = calcular_x_verde(y_dada)
# print(f"Para y = {y_dada}, x = {x_calculada}")
#
# def calcular_x_azul(y):
#     m = reg2.coef_[0]
#     b = reg2.intercept_
#     x = (y - b) / m
#     return x
#
# y_dada = float(input("Ingresa un valor de y (azul): "))
# x_calculada = calcular_x_azul(y_dada)
# print(f"Para y = {y_dada}, x = {x_calculada}")