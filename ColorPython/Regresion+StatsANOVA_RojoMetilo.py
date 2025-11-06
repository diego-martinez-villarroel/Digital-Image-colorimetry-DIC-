import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from PIL import Image
import os
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

#recorte intereactivo + funcion para color promedio + regresion lineal (casi completo) para rojo metilo + INTENTO DE AÑADIR ESTADISTICA + ANOVA

class InteractiveCrop:
    def __init__(self, img, nombre):
        self.img = img #guarda imagen
        self.nombre = nombre #guarda nombre
        self.fig, self.ax = plt.subplots(figsize=(12, 10)) #tamaño de la ventana
        self.ax.imshow(img) #muestra la imagen
        self.ax.set_title(f"Arrastra el rectángulo a la zona de la solución: {nombre}\nClick 'Confirmar' cuando esté listo", fontsize=12) #titulo de la ventana
        
        # Tamaño del rectángulo de selección (ajustado para cubetas)
        width, height = img.size
        self.rect_width = int(width * 0.10)  # % del ancho de la imagen MODIFICAR ESTO SI ES NECESARIO
        self.rect_height = int(height * 0.4)  # % del alto de la imagen
        
        # Posición inicial del rectángulo (no es tan importante porque se puede mover después)
        self.x0 = width // 2 - self.rect_width // 2
        self.y0 = height // 2 - self.rect_height // 2 - int(height * 0.05)
        
        # Crear el rectángulo (rectangular vertical para la cubeta)
        self.rect = Rectangle((self.x0, self.y0), self.rect_width, self.rect_height,
                              linewidth=4, edgecolor='lime', facecolor='none', linestyle='--')
        self.ax.add_patch(self.rect)
        
        # Variables para el arrastre
        self.press = None
        self.crop_coords = None
        self.confirmed = False

        self.fig.canvas.mpl_connect('button_press_event', self.on_press) # Conectar eventos
        self.fig.canvas.mpl_connect('button_release_event', self.on_release) #mpl es porque es metodo de matplotlib
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # Botón de confirmación
        ax_button = plt.axes([0.7, 0.02, 0.2, 0.05])
        self.btn_confirm = Button(ax_button, 'Confirmar')
        self.btn_confirm.on_clicked(self.confirm)
        
        plt.show()
    
    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        
        contains, _ = self.rect.contains(event)
        if contains:
            x0, y0 = self.rect.get_xy()
            self.press = (x0, y0, event.xdata, event.ydata)
    
    def on_motion(self, event):
        if self.press is None or event.inaxes != self.ax:
            return
        
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        
        new_x = x0 + dx
        new_y = y0 + dy
        
        # Limitar el movimiento dentro de los bordes de la imagen
        width, height = self.img.size
        new_x = max(0, min(new_x, width - self.rect_width))
        new_y = max(0, min(new_y, height - self.rect_height))
        
        self.rect.set_xy((new_x, new_y))
        self.fig.canvas.draw()
    
    def on_release(self, event):
        self.press = None
    
    def confirm(self, event): #cuando se presiona el boton de confirmar
        x, y = self.rect.get_xy()
        self.crop_coords = (int(x), int(y), int(x + self.rect_width), int(y + self.rect_height))
        self.confirmed = True
        plt.close(self.fig)
    
    def get_crop_coords(self):
        return self.crop_coords #(variable) crop_coords: tuple[int, int, int, int]
    
    
# Función para obtener el color promedio de una imagen

def most_common_used_color(img):
    width, height = img.size
    r_total = g_total = b_total = 0
    count = 0
 
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
            r_total += r
            g_total += g
            b_total += b
            count += 1
 
    return (r_total/count, g_total/count, b_total/count)

# Lista de imágenes
imagenes = [r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO01B.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO02B.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO03B.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO04B.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ROJO05B.jpg"]

rval, gval, bval = [], [], [] #listas para guardar los valores de r,g,b a futuro

for i in imagenes:
    img = Image.open(i).convert('RGB')
    nombre = os.path.basename(i)
    
    #interfaz para recortar la imagen
    print(f"\nProcesando: {nombre}")
    
    cropper = InteractiveCrop(img, nombre)
    coords = cropper.get_crop_coords()
    
    if coords:
        # Recortar la imagen según las coordenadas seleccionadas
        img_cropped = img.crop(coords)
        
        # Redimensionar la imagen recortada
        img_resized = img_cropped.resize((50, 50))
        
        # Calcular el color promedio
        common_color = most_common_used_color(img_resized)
        rval.append(common_color[0]) #return (r_total/count, g_total/count, b_total/count) posicion 0,1,2
        gval.append(common_color[1])
        bval.append(common_color[2])
        
        # Mostrar la imagen recortada y redimensionada
        plt.imshow(img_resized)
        plt.title(f"Imagen procesada: {nombre}")
        plt.show()
        
        print(f"Los colores de la imagen {nombre} son R,G,B: {common_color}")

# Convertir listas a arrays #basicamente me deja los datos como los txt que tenia para poder hacer el ajuste lineal
r = np.array(rval)
g = np.array(gval)
b = np.array(bval) #son los valores en arrays son 5 de cada en este caso 


# Concentraciones
x = [0.25, 0.5, 1, 2, 4]
x = np.array(x).reshape(-1, 1) #https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html

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

# Grafico de concentracion y mean rgb
plt.scatter(x, r, color="red") #se puede poner alpha = x para transparencia de los puntos
plt.scatter(x, g, color="green")
plt.scatter(x, b, color="blue")
plt.xlabel("Concentración")
plt.ylabel("Valor RGB")
plt.title("Curvas de calibración RGB vs Concentración")
plt.show()