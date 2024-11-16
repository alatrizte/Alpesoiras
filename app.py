import tkinter as tk
from tkinter import filedialog
import customtkinter

from PIL import Image

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def seleccionar_carpeta_origen():
    carpeta_origen = filedialog.askdirectory(title="Selecciona o cartafol de orixe")
    entrada_origen.delete(0, tk.END)
    entrada_origen.insert(0, carpeta_origen)

def seleccionar_carpeta_destino():
    carpeta_destino = filedialog.askdirectory(title="Selecciona o cartafol de destino")
    entrada_destino.delete(0, tk.END)
    entrada_destino.insert(0, carpeta_destino)

def procesar_imagenes():
    origen = entrada_origen.get()
    destino = entrada_destino.get()
    
    if not origen or not destino:
        finishLabel.configure(text = "Por favor, selecciona amboslos cartafoles", text_color="red")
        return
    
    try:

        font = {'family': 'Arial',
        'color':  'darkred',
        'weight': 'normal',
        'size': 25,
        }
        p_percentage.pack()
        progress_bar.pack()

        total = len (os.listdir(origen))
        cont = 0

        for i in os.listdir(origen):
            cont += 1

            img = cv2.imread(f"{origen}/{i}")
            img  = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            backup= img.copy()

            lower = [60, 60, 60]
            upper = [250, 250, 250]

            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            # find the colors within the specified boundaries and apply
            mask = cv2.inRange(img, lower, upper)
            output = cv2.bitwise_and(img, img, mask=mask)

            ret,thresh = cv2.threshold(mask, 40, 255, 0)

            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


            if len(contours) != 0:
                # draw in blue the contours that were founded
                cv2.drawContours(output, contours, -1, 255, 3)

                # find the biggest countour (c) by the area
                c = max(contours, key = cv2.contourArea)
                x,y,w,h = cv2.boundingRect(c)

                # draw the biggest contour (c) in green
                cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),5)

            foreground = img[y:y+h,x:x+w]
            plt.figure(figsize=(20,4))
            plt.subplot(1,3,1),plt.imshow(img),plt.title("Input",fontdict=font)
            plt.subplot(1,3,2),plt.imshow(output),plt.title("All Contours",fontdict=font)
            plt.subplot(1,3,3),plt.imshow(foreground),plt.title("output",fontdict=font)
            print(foreground.shape)

            # Guardar la imagen 'output' cropeada
            plt.imsave(f"{destino}/{i}", foreground)
            percentage_compl = cont / total *100
            percentage = str(int(percentage_compl))
            p_percentage.configure(text=percentage + "%")
            p_percentage.update()
            
            progress_bar.set(float(percentage_compl) / 100)

            check_state = check_var.get()
            if check_state == "on":
                plt.show()

        finishLabel.configure(text = "Imáxes cortadas!", text_color="green")

    except Exception as e:
        finishLabel.configure(text = f"Ocorreu un erro: {str(e)}", text_color="red")

# System Settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Crear la ventana principal
app = customtkinter.CTk()
app.title("Alpesoiras")
app.geometry("600x800")

reductor = 0.85

my_image = customtkinter.CTkImage(light_image=Image.open("alpesoiras-white.png"),
                                  dark_image=Image.open("alpesoiras-white.png"),
                                  size=(268*reductor, 179*reductor))

image = customtkinter.CTkLabel(app, image=my_image, text="")
image.pack(pady=30)

title = customtkinter.CTkLabel(app, text="Selecciona as imáxes para cortar")
title.pack()

# Carpeta de origen
customtkinter.CTkLabel(app, text="Cartafol de orixe:").pack(pady=(20, 0))
entrada_origen = customtkinter.CTkEntry(app, width=350, height=40)
entrada_origen.pack()
customtkinter.CTkButton(app, text="Seleccionar", command=seleccionar_carpeta_origen).pack(pady=(7, 0))

# Carpeta de destino
customtkinter.CTkLabel(app, text="Cartafol de destino:").pack(pady=(10, 0))
entrada_destino = customtkinter.CTkEntry(app, width=350, height=40)
entrada_destino.pack()
customtkinter.CTkButton(app, text="Seleccionar", command=seleccionar_carpeta_destino).pack(pady=(7, 0))

# Mostrar proceso imagenes
check_var = customtkinter.StringVar(value="off")
checkbox = customtkinter.CTkCheckBox(app, text="Activar a vista do proceso de imaxes.", variable=check_var, onvalue="on", offvalue="off")
checkbox.pack(pady=20)

# Botón para procesar
font_bold = customtkinter.CTkFont(weight="bold", size=14)
customtkinter.CTkButton(app, width=250, height=40, text="CORTAR IMÁXES",font=font_bold, command=procesar_imagenes).pack(pady=40)

p_percentage = customtkinter.CTkLabel(app, text="0%")


progress_bar = customtkinter.CTkProgressBar(app, width=350)
progress_bar.set(0)


finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()


app.mainloop()

