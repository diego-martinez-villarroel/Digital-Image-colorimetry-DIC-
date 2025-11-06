import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from PIL import Image
import os
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

#05/11/2025

# Prueba de recorte interactivo con 3 cuadrados + función para color promedio + regresión lineal para FeCN

class InteractiveCrop:
    def __init__(self, img, nombre):
        self.img = img
        self.nombre = nombre
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.ax.imshow(img)
        self.ax.set_title(f"Arrastra los 3 rectángulos a diferentes zonas: {nombre}\nClick 'Confirmar' cuando estén listos", fontsize=12)
        
        # Tamaño del rectángulo de selección
        width, height = img.size
        self.rect_width = int(width * 0.10)
        self.rect_height = int(height * 0.15)
        
        # Crear 3 rectángulos en diferentes posiciones iniciales
        self.rectangles = []
        self.crop_coords_list = []
        
        # Posiciones iniciales para los 3 cuadrados (distribuidos verticalmente)
        positions = [
            (width // 2 - self.rect_width // 2, height // 3 - self.rect_height // 2),      # Superior
            (width // 2 - self.rect_width // 2, height // 2 - self.rect_height // 2),      # Centro
            (width // 2 - self.rect_width // 2, 2 * height // 3 - self.rect_height // 2)   # Inferior
        ]
        
        # Colores diferentes para cada rectángulo
        colors = ['black', 'black', 'black']
        
        for i, (x0, y0) in enumerate(positions):
            rect = Rectangle((x0, y0), self.rect_width, self.rect_height,
                           linewidth=4, edgecolor=colors[i], facecolor='none', linestyle='--')
            self.ax.add_patch(rect)
            self.rectangles.append(rect)
        
        # Variables para el arrastre
        self.press = None
        self.active_rect = None
        self.confirmed = False
        
        # Conectar eventos
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        # Botón de confirmación
        ax_button = plt.axes([0.7, 0.02, 0.2, 0.05])
        self.btn_confirm = Button(ax_button, 'Confirmar')
        self.btn_confirm.on_clicked(self.confirm)
        
        plt.show()
    
    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        
        # Verificar cuál rectángulo fue clickeado
        for rect in self.rectangles:
            contains, _ = rect.contains(event)
            if contains:
                x0, y0 = rect.get_xy()
                self.press = (x0, y0, event.xdata, event.ydata)
                self.active_rect = rect
                break
    
    def on_motion(self, event):
        if self.press is None or event.inaxes != self.ax or self.active_rect is None:
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
        
        self.active_rect.set_xy((new_x, new_y))
        self.fig.canvas.draw()
    
    def on_release(self, event):
        self.press = None
        self.active_rect = None
    
    def confirm(self, event):
        # Guardar las coordenadas de los 3 rectángulos
        for rect in self.rectangles:
            x, y = rect.get_xy()
            coords = (int(x), int(y), int(x + self.rect_width), int(y + self.rect_height))
            self.crop_coords_list.append(coords)
        
        self.confirmed = True
        plt.close(self.fig)
    
    def get_crop_coords_list(self):
        return self.crop_coords_list  # Retorna lista con 3 tuplas de coordenadas

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
imagenes = [r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\FeSCN\FeSCN01A.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\FeSCN\FeSCN02A.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\FeSCN\FeSCN03A.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\FeSCN\FeSCN04A.jpg",
           r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\FeSCN\FeSCN05A.jpg"]

rval, gval, bval = [], [], []  # listas para guardar los valores de r,g,b a futuro

for i in imagenes:
    img = Image.open(i).convert('RGB')
    nombre = os.path.basename(i)
    
    # Interfaz para recortar la imagen (ahora con 3 cuadrados)
    print(f"\nProcesando: {nombre}")
    
    cropper = InteractiveCrop(img, nombre)
    coords_list = cropper.get_crop_coords_list()  # Lista con 3 coordenadas
    
    if coords_list and len(coords_list) == 3:
        # Listas temporales para los 3 crops de esta imagen
        r_temps = []
        g_temps = []
        b_temps = []
        
        # Procesar cada uno de los 3 cuadrados
        for idx, coords in enumerate(coords_list):
            # Recortar la imagen según las coordenadas seleccionadas
            img_cropped = img.crop(coords)
            
            # Redimensionar la imagen recortada
            img_resized = img_cropped.resize((50, 50))
            
            # Calcular el color promedio
            common_color = most_common_used_color(img_resized)
            r_temps.append(common_color[0])
            g_temps.append(common_color[1])
            b_temps.append(common_color[2])
            
            print(f"  Cuadrado {idx+1} - R,G,B: {common_color}")
        
        # Calcular el promedio de los 3 cuadrados
        r_promedio = np.mean(r_temps)
        g_promedio = np.mean(g_temps)
        b_promedio = np.mean(b_temps)
        
        # Guardar el promedio en las listas finales
        rval.append(r_promedio)
        gval.append(g_promedio)
        bval.append(b_promedio)
        
        print(f"  → Promedio final RGB para {nombre}: ({r_promedio:.4f}, {g_promedio:.4f}, {b_promedio:.4f})")
        
        # Mostrar las 3 imágenes recortadas
        fig_crops, axes = plt.subplots(1, 3, figsize=(12, 4))
        for idx, coords in enumerate(coords_list):
            img_cropped = img.crop(coords)
            img_resized = img_cropped.resize((50, 50))
            axes[idx].imshow(img_resized)
            axes[idx].set_title(f"Cuadrado {idx+1}")
            axes[idx].axis('off')
        fig_crops.suptitle(f"Imagen procesada: {nombre}", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

# Convertir listas a arrays
r = np.array(rval)
g = np.array(gval)
b = np.array(bval)

print("\n" + "="*60)
print("VALORES RGB FINALES (promedio de 3 mediciones por imagen)")
print("="*60)
print(f"Rojo:   {r}")
print(f"Verde:  {g}")
print(f"Azul:   {b}")

# Concentraciones reales
x=[2*10**-5,4*10**-5,6*10**-5,8*10**-5,10*10**-5] # mol/L concetraciones que me mando el profe
x = np.array(x).reshape(-1, 1)

# Regresión lineal para rojo
reg0 = LinearRegression().fit(x, r)
print(f"\nEl coeficiente de correlacion para rojo es R^2 = {reg0.score(x, r):.6f}")
print(f"La recta para rojo es y = {reg0.coef_[0]:.4f}x + {reg0.intercept_:.4f}")
plt.plot(x, reg0.predict(x), color="red", linewidth=2)

# Regresión lineal para verde
reg1 = LinearRegression().fit(x, g)
print(f"El coeficiente de correlacion para verde es R^2 = {reg1.score(x, g):.6f}")
print(f"La recta para verde es y = {reg1.coef_[0]:.4f}x + {reg1.intercept_:.4f}")
plt.plot(x, reg1.predict(x), color="green", linewidth=2)

# Regresión lineal para azul
reg2 = LinearRegression().fit(x, b)
print(f"El coeficiente de correlacion para azul es R^2 = {reg2.score(x, b):.6f}")
print(f"La recta para azul es y = {reg2.coef_[0]:.4f}x + {reg2.intercept_:.4f}")
plt.plot(x, reg2.predict(x), color="blue", linewidth=2)

# Gráfico de concentración y mean rgb
plt.scatter(x, r, color="red")
plt.scatter(x, g, color="green")
plt.scatter(x, b, color="blue")
plt.xlabel("Concentración (mol/L)", fontsize=12, fontweight='bold')
plt.ylabel("Valor RGB", fontsize=12, fontweight='bold')
plt.title("Curvas de calibración RGB vs Concentración FeSCN", fontsize=13, fontweight='bold')
plt.legend(["Regresión lineal Rojo","Regresión lineal Verde","Regresión lineal Azul",
            "Datos Rojo","Datos Verde","Datos Azul"], loc='best')
#plt.savefig("FeSCN_regresion3CROP.jpg")
plt.show()