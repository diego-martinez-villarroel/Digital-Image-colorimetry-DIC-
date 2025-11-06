import numpy as np
import matplotlib.pyplot as plt

#CONCETRACION NOMINAL (real) 
c_nominal = np.array([0.25, 0.5, 1, 2, 4]) # total r,g,b 

r = np.array([208.9228,209.9088,212.3892,212.0512,221.6216]) #valores mean para rojo
g = np.array([199.9192,193.5736,167.7464,115.1532,40.048]) #valores mean para verde
b = np.array([216.2816,213.0768,207.9304,192.5616,172.6828]) #valores mean para azul

cr = [] #concentracion rojo, verde, azul 
cv = []
ca = []

for i in r: #calculo de concentracion a partir de mean para rojo
    x = (i - 208.04905) / 3.1804322580645152
    cr.append(x) #guarda valor en la lista creada
    #print("concentracion predicha recta roja:", x)

for i in g: #calculo de concentracion a partir de mean para verde
    x = (i - 210.86661666666663) / -43.59905591397849
    cv.append(x) #guarda valor en la lista creada
    #print("concentracion predicha recta verde:", x)

for i in b: #calculo de concentracion a partir de mean para azul
    x = (i - 218.76211666666666) / -11.777726881720431
    ca.append(x) #guarda valor en la lista creada
    #print("concentracion predicha recta azul:", x)

# Convertir listas a arrays #basicamente me deja los datos como los txt que tenia para poder hacer el ajuste lineal y hacer el promedio para comparar con cn
#conc_predicha = np.array([np.array(cr[0]+cv[0]+ca[0])/3, np.array(cr[1]+cv[1]+ca[1])/3, np.array(cr[2]+cv[2]+ca[2])/3, np.array(cr[3]+cv[3]+ca[3])/3, np.array(cr[4]+cv[4]+ca[4])/3]) otra forma de calcular el 
#promedio
#conc_predicha = np.array(cr[0]+cv[0]+ca[0])/3, np.array(cr[1]+cv[1]+ca[1])/3, np.array(cr[2]+cv[2]+ca[2])/3, np.array(cr[3]+cv[3]+ca[3])/3, np.array(cr[4]+cv[4]+ca[4])/3
#es mejor tenerlo todo en ([...]) para que quede como array de 5 elementos

#si bien para cada recta tenemos una concentracion predicha distinta, para tener un unico valor de concentracion predicha por cada punto, se saca el promedio de las 3 rectas

conc_predicha = (np.array(cr)+np.array(cv)+np.array(ca))/3 #calculo del promedio de las 3 concentraciones predichas


print("Concentracion nominal:", c_nominal)

print("Concentracion predicha promedio:", conc_predicha)

print("error absoluto cn - cp en cada dato: +-", err_abs := c_nominal - conc_predicha) #error absoluto (Residuos)

print("error medio absoluto +-:", np.mean(np.abs(err_abs))) 

print("desviacion estandar del error absoluto std (cn - cp):", np.std(err_abs, ddof=1)) #revisar bitacora explicacion ddof=1

print("error porcentual medio (relativo):", np.mean(np.abs(err_abs/c_nominal))*100, "%") #error relativo

