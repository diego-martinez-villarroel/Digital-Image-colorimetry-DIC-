#Código que me mandó el profe para obtener el mean de r,g,b de una imagen
from PIL import Image
import os
 
def most_common_used_color(img):
    # Get width and height of Image
    width, height = img.size
 
    # Initialize Variable
    r_total = 0
    g_total = 0
    b_total = 0
 
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
 

imagenes = [r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ImagenesCROP\imagenrojometilo.jpeg",
            r"C:\Users\Diego\OneDrive - Universidad de Concepción\Documentos\Universidad\Semestre_8\Diseño de prototipos I\ColorPython\ImagenesCROP\rojo4.jpeg"]

for i in imagenes:
    img = Image.open(i).convert('RGB') #abrir y convertir la imagen a RGB
    common_color = most_common_used_color(img) #le aplicas la funcion a la imagen
    nombre = os.path.basename(i) #para mostrar solo el nombre de la imagen y no toda la ruta
    print(f"Los colores de la imagen {nombre} son R,G,B en orden {common_color}")

#Un f-string te permite incrustar variables o expresiones directamente dentro de la cadena usando llaves { }.

#Este codigo funciona para obtener el mean de los r,g,b de una imagen 