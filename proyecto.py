import tkinter as tk
from tkinter import messagebox
import re
from email.message import EmailMessage
import smtplib
import ssl

def validar_fecha(fecha):
    # Validar formato de fecha (dd/mm/aaaa)
    patron_fecha = re.compile(r'^\d{2}/\d{2}/\d{4}$')
    return bool(re.match(patron_fecha, fecha))

def validar_correo(correo):
    # Validar formato de correo electrónico
    patron_correo = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return bool(re.match(patron_correo, correo))

def validar_telefono(telefono):
    # Validar formato de número telefónico (opcional: + y dígitos)
    patron_telefono = re.compile(r'^\+?\d+$')
    return bool(re.match(patron_telefono, telefono))

def guardar_datos():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    fecha_nacimiento = entry_fecha.get()
    pais = entry_pais.get()
    correo = entry_correo.get()
    telefono = entry_telefono.get()

    if not validar_fecha(fecha_nacimiento):
        messagebox.showerror("Error", "Formato de fecha incorrecto (dd/mm/aaaa)")
        return
    if pais not in lista_paises:
        messagebox.showerror("Error", "País no válido")
        return
    if not validar_correo(correo):
        messagebox.showerror("Error", "Formato de correo electrónico incorrecto")
        return
    if not validar_telefono(telefono):
        messagebox.showerror("Error", "Formato de número telefónico incorrecto")
        return

    # Guardar los datos en un archivo txt
    with open("datos_usuarios.txt", "a") as archivo:
        archivo.write(f"Nombre: {nombre}\nApellido: {apellido}\nFecha de Nacimiento: {fecha_nacimiento}\nPaís: {pais}\nCorreo: {correo}\nTeléfono: {telefono}\n\n")
    
    envio_email(correo, nombre)

    messagebox.showinfo("Registro exitoso", "¡Usuario registrado exitosamente!")

    # Limpiar el formulario después del registro
    limpiar_formulario()
    
    actualizar_tabla()
def envio_email(email_recibir, nombre):
    email_sender = 'Agrega-Tu-Correo@gmail.com'  # Correo que enviara el mail
    email_password = 'agrega-tu-contrasena-de-aplicacion'  # Contraseña del correo
    email_receiver = email_recibir  # Correo que recibirá el mail

    subject = '¡Bienvenido a nuestra aplicación!'
    body = f"¡Hola {nombre}!\n\nGracias por registrarte en nuestra aplicación. ¡Bienvenido!"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)  # Iniciar sesión en el correo
        smtp.sendmail(email_sender, email_receiver, em.as_string())  # Enviar correo
def limpiar_formulario():
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)
    entry_pais.set(lista_paises[0])
    entry_correo.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)

# Lista de países para elegir
lista_paises = ["Argentina", "Brasil", "Chile", "Colombia", "México", "Perú", "España", "Venezuela"]

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Formulario de Registro")

# Crear y colocar etiquetas y campos de entrada en fila
tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(ventana)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(ventana, text="Apellido:").grid(row=0, column=2, padx=5, pady=5)
entry_apellido = tk.Entry(ventana)
entry_apellido.grid(row=0, column=3, padx=5, pady=5)

tk.Label(ventana, text="Fecha de Nacimiento (dd/mm/aaaa):").grid(row=0, column=4, padx=5, pady=5)
entry_fecha = tk.Entry(ventana)
entry_fecha.grid(row=0, column=5, padx=5, pady=5)

tk.Label(ventana, text="País:").grid(row=0, column=6, padx=5, pady=5)
entry_pais = tk.StringVar()
entry_pais.set(lista_paises[0])
dropdown_pais = tk.OptionMenu(ventana, entry_pais, *lista_paises)
dropdown_pais.grid(row=0, column=7, padx=5, pady=5)

tk.Label(ventana, text="Correo:").grid(row=0, column=8, padx=5, pady=5)
entry_correo = tk.Entry(ventana)
entry_correo.grid(row=0, column=9, padx=5, pady=5)

tk.Label(ventana, text="Teléfono:").grid(row=0, column=10, padx=5, pady=5)
entry_telefono = tk.Entry(ventana)
entry_telefono.grid(row=0, column=11, padx=5, pady=5)

# Botón para enviar el formulario
boton_enviar = tk.Button(ventana, text="Registrar Usuario", command=guardar_datos)
boton_enviar.grid(row=1, column=0, columnspan=12, pady=10)



# Crear un marco con un lienzo y una barra de desplazamiento para mostrar los datos de usuario
frame_scroll = tk.Frame(ventana, borderwidth=2, relief="groove")
frame_scroll.grid(row=2, column=0, columnspan=12, pady=10, padx=5, sticky="nsew")

canvas = tk.Canvas(frame_scroll, height=200)
scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Etiquetas para el encabezado de la tabla
labels_header = ["Nombre", "Apellido", "Fecha de Nacimiento", "País", "Correo", "Número Telefónico"]

# Mostrar el encabezado de la tabla
for col, label in enumerate(labels_header):
    tk.Label(scrollable_frame, text=label, font=("bold", 10), padx=55, pady=5, borderwidth=1, relief="solid").grid(row=0, column=col, sticky="nsew")

def actualizar_tabla():
    # Leer datos desde el archivo y actualizar la tabla
    try:
        with open("datos_usuarios.txt", "r") as archivo:
            lines = archivo.readlines()
            
            # Mostrar todas las entradas en la tabla
            for i in range(len(lines)//7):
                data = [line.strip().split(":")[1] for line in lines[i*7:i*7+6]]
                for col, value in enumerate(data):
                    tk.Label(scrollable_frame, text=value, padx=10, pady=5, borderwidth=1, relief="solid").grid(row=i+1, column=col, sticky="nsew")
                                    # Botón "Modificar" en cada fila
                tk.Button(scrollable_frame, text="Modificar", command=lambda i=i: modificar_usuario(i)).grid(row=i+1, column=len(data), padx=10, pady=5)

    except FileNotFoundError:
        # Manejar el caso en el que no se encuentra el archivo
        pass

# Llamar a la función para actualizar la tabla inicialmente
actualizar_tabla()
def modificar_usuario(indice):

    ventana_modificar = tk.Toplevel(ventana)
    ventana_modificar.title("Modificar Usuario")

    # Obtener la información del usuario desde el archivo
    with open("datos_usuarios.txt", "r") as archivo:
        lines = archivo.readlines()
        data = [line.strip().split(":")[1] for line in lines[indice*7:indice*7+6]]

    # Crear etiquetas y campos de entrada en la nueva ventana para editar la información
    etiquetas = ["Nombre", "Apellido", "Fecha de Nacimiento", "País", "Correo", "Teléfono"]
    campos = []

    for i, etiqueta in enumerate(etiquetas):
        tk.Label(ventana_modificar, text=f"{etiqueta}:").grid(row=i, column=0, padx=5, pady=5)
        if etiqueta == "País":
            # Agregar un menú desplegable para el país
            entry_mod = tk.StringVar(value=data[i])
            dropdown_pais_mod = tk.OptionMenu(ventana_modificar, entry_mod, "Argentina", "Brasil", "Chile", "Colombia", "México", "Perú", "España", "Venezuela")
            dropdown_pais_mod.grid(row=i, column=1, padx=5, pady=5)
            campos.append(entry_mod)
        elif etiqueta == "Fecha de Nacimiento":
            entry_mod = tk.Entry(ventana_modificar)
            entry_mod.insert(0, data[i])
            entry_mod.grid(row=i, column=1, padx=5, pady=5)
            campos.append(entry_mod)
        elif etiqueta == "Correo":
            entry_mod = tk.Entry(ventana_modificar)
            entry_mod.insert(0, data[i])
            entry_mod.grid(row=i, column=1, padx=5, pady=5)
            campos.append(entry_mod)
        elif etiqueta == "Teléfono":
            entry_mod = tk.Entry(ventana_modificar)
            entry_mod.insert(0, data[i])
            entry_mod.grid(row=i, column=1, padx=5, pady=5)
            campos.append(entry_mod)
        else:
            entry_mod = tk.Entry(ventana_modificar)
            entry_mod.insert(0, data[i])
            entry_mod.grid(row=i, column=1, padx=5, pady=5)
            campos.append(entry_mod)

    def guardar_modificaciones():
        # Obtener los nuevos valores de los campos de entrada
        nuevos_datos = [campo.get() for campo in campos]

        # Validar la fecha
        if not validar_fecha(nuevos_datos[2]):
            messagebox.showerror("Error", "Formato de fecha incorrecto (dd/mm/aaaa)")
            return

        # Validar el correo
        if not validar_correo(nuevos_datos[4]):
            messagebox.showerror("Error", "Formato de correo electrónico incorrecto")
            return

        # Validar el número telefónico
        if not validar_telefono(nuevos_datos[5]):
            messagebox.showerror("Error", "Formato de número telefónico incorrecto")
            return


        # Actualizar la información en el archivo
        with open("datos_usuarios.txt", "r") as archivo:
            lineas = archivo.readlines()

        lineas[indice*7:indice*7+6] = [f"{etiqueta}: {valor}\n" for etiqueta, valor in zip(etiquetas, nuevos_datos)]

        with open("datos_usuarios.txt", "w") as archivo:
            archivo.writelines(lineas)

        # Cerrar la ventana de modificación
        ventana_modificar.destroy()

        messagebox.showinfo("Éxito", "Usuario modificado exitosamente")

        # Actualizar la tabla con los nuevos datos
        actualizar_tabla()

    # Botón para guardar las modificaciones
    tk.Button(ventana_modificar, text="Actualizar Datos", command=guardar_modificaciones).grid(row=len(etiquetas), column=0, columnspan=2, pady=10)

# Mostrar todas las entradas en la tabla
with open("datos_usuarios.txt", "r") as archivo:
    lines = archivo.readlines()

for i in range(len(lines)//7):
    data = [line.strip().split(":")[1] for line in lines[i*7:i*7+6]]
    
    # Mostrar la información en la fila correspondiente
    for col, value in enumerate(data):
        tk.Label(scrollable_frame, text=value, padx=10, pady=5, borderwidth=1, relief="solid").grid(row=i+1, column=col, sticky="nsew")

    # Botón "Modificar" en cada fila
    tk.Button(scrollable_frame, text="Modificar", command=lambda i=i: modificar_usuario(i)).grid(row=i+1, column=len(data), padx=10, pady=5)



ventana.mainloop()





