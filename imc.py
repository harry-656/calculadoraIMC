import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # Necesitarás instalar pillow para trabajar con imágenes
import csv

def calcular_imc():
    try:
        nombre = entry_nombre.get()
        edad = int(entry_edad.get())
        peso = float(entry_peso.get())
        altura = float(entry_altura.get())
        sexo = sexo_var.get()
        imc = peso / (altura ** 2)
        mostrar_resultado(nombre, sexo, imc)
        guardar_datos(nombre, edad, peso, altura, sexo, imc)
    except ValueError:
        messagebox.showerror("Entrada inválida", "Por favor, ingrese valores numéricos válidos.")

def mostrar_resultado(nombre, sexo, imc):
    resultado = f"{nombre}, su IMC es: {imc:.2f}\nSexo: {sexo}\n"
    if imc < 18.5:
        resultado += "Usted está por debajo del peso normal."
    elif 18.5 <= imc < 24.9:
        resultado += "Usted tiene un peso normal."
    elif 25 <= imc < 29.9:
        resultado += "Usted tiene sobrepeso."
    else:
        resultado += "Usted tiene obesidad."
    messagebox.showinfo("Resultado del IMC", resultado)

def guardar_datos(nombre, edad, peso, altura, sexo, imc):
    with open("datos_imc.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nombre, edad, peso, altura, sexo, imc])

def mostrar_datos():
    try:
        with open("datos_imc.csv", mode="r") as file:
            reader = csv.reader(file)
            datos = list(reader)
            if datos:
                mostrar_tabla(datos)
            else:
                messagebox.showinfo("Datos Guardados", "No hay datos guardados.")
    except FileNotFoundError:
        messagebox.showinfo("Datos Guardados", "No se encontró el archivo de datos.")

def mostrar_tabla(datos):
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title("Datos Guardados")

    tree = ttk.Treeview(ventana_tabla, columns=("Nombre", "Edad", "Peso", "Altura", "Sexo", "IMC"), show='headings')
    tree.heading("Nombre", text="Nombre")
    tree.heading("Edad", text="Edad")
    tree.heading("Peso", text="Peso (kg)")
    tree.heading("Altura", text="Altura (m)")
    tree.heading("Sexo", text="Sexo")
    tree.heading("IMC", text="IMC")

    for row in datos:
        tree.insert("", "end", values=row)

    tree.pack(fill="both", expand=True)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de IMC")

# Cargar la imagen de fondo
imagen_fondo = Image.open("fondo.png")
imagen_fondo = imagen_fondo.resize((600, 450))
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

# Crear un widget Canvas para mostrar la imagen de fondo
canvas = tk.Canvas(ventana, width=600, height=450)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=imagen_fondo, anchor="nw")

# Crear un marco para los widgets encima del canvas
frame = tk.Frame(ventana, bg='ghostwhite', bd=0)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Crear y colocar las etiquetas y cuadros de texto para nombre, edad, peso y altura
tk.Label(frame, text="Nombre:", bg='white').grid(row=0, column=0, padx=10, pady=5)
entry_nombre = tk.Entry(frame)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Edad:", bg='white').grid(row=1, column=0, padx=10, pady=5)
entry_edad = tk.Entry(frame)
entry_edad.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Peso (kg):", bg='white').grid(row=2, column=0, padx=10, pady=5)
entry_peso = tk.Entry(frame)
entry_peso.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame, text="Altura (m):", bg='white').grid(row=3, column=0, padx=10, pady=5)
entry_altura = tk.Entry(frame)
entry_altura.grid(row=3, column=1, padx=10, pady=5)

# Crear y colocar los botones de radio para seleccionar el sexo
sexo_var = tk.StringVar()
sexo_var.set("Masculino")  # Valor por defecto

tk.Label(frame, text="Sexo:", bg='white').grid(row=4, column=0, padx=10, pady=5)
radio_masculino = tk.Radiobutton(frame, text="Masculino", variable=sexo_var, value="Masculino", bg='white')
radio_femenino = tk.Radiobutton(frame, text="Femenino", variable=sexo_var, value="Femenino", bg='white')
radio_masculino.grid(row=4, column=1, padx=10, pady=5, sticky="w")
radio_femenino.grid(row=4, column=2, padx=10, pady=5, sticky="e")

# Cargar la imagen del botón
imagen_boton = Image.open("calcular.png")
imagen_boton = imagen_boton.resize((200, 100))  # Redimensionar si es necesario
imagen_boton = ImageTk.PhotoImage(imagen_boton)

# Crear y colocar el botón para calcular el IMC con la imagen
boton_calcular = tk.Button(frame, image=imagen_boton, command=calcular_imc, bd=0)
boton_calcular.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Crear y colocar el botón para mostrar los datos guardados
boton_mostrar = tk.Button(frame, text="Mostrar Datos", command=mostrar_datos)
boton_mostrar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Mantener una referencia de la imagen para que no sea recolectada por el garbage collector
boton_calcular.image = imagen_boton

# Iniciar el bucle principal de la ventana
ventana.mainloop()
