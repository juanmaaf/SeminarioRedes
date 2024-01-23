import tkinter as tk    # Librería para interfaz gráfica
from tkinter.simpledialog import askinteger # Para pedir información al usuario 
from tkinter import scrolledtext
import pandas as pd
import pyAgrum as gum
import metodos
from sklearn.metrics import mean_squared_error

mse_pre = None
mse_post = None

def estudio_twitter(ventana, excel):
    global ventana_twitter
    
    # Estudio REDES - TWITTER

    # Lista de nombres de columnas que deseas seleccionar
    columnas_seleccionadas = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "C7A"]

    # Cargar solo las columnas seleccionadas desde el archivo Excel utilizando pandas
    datos_twitter = pd.read_excel(excel, usecols=columnas_seleccionadas, header=0)
    
    # Crear una nueva ventana para mostrar el valor de las tablas
    ventana_twitter = tk.Toplevel(ventana)
    ventana_twitter.title("Seminario Redes")

    # Crear un Frame para el menú principal
    frame = tk.Frame(ventana_twitter)
    frame.pack(pady=5)
    
    # Agregar un título "Menú Principal" con letras en negrita en el Frame
    titulo = tk.Label(frame, text="Estudio Twitter", font=("Helvetica", 16, "bold"))
    titulo.pack(pady=10)

    # Método para mostrar los datos
    def mostrar_datos():
        # Convertir los datos a una cadena de texto
        texto_datos = datos_twitter.to_string(index=False)

        # Crear un widget Text para mostrar los datos
        cuadro_texto = scrolledtext.ScrolledText(frame, width=70, height=10)
        cuadro_texto.insert(tk.INSERT, texto_datos)
        cuadro_texto.pack(padx=10, pady=10)
    
    # Método para realizar el análisis
    def analisis():
        global mse_pre
        global mse_post
        
        # Crear un objeto BN Learner
        learner = gum.BNLearner(datos_twitter)

        # Utilizar un criterio específico para la estructura y parámetros
        learner.useScoreBDeu()

        # Aprender la estructura de la red
        bn_structure = learner.learnBN()

        # Convertir el DataFrame a una matriz de NumPy
        matriz_datos_twitter = datos_twitter.to_numpy()

        # Eliminar la última columna de la matriz
        matriz_datos_twitter = matriz_datos_twitter[:, :-1]
        
        # Posterior inferencia

        # Crear un inferidor de red bayesiana
        inference = gum.LazyPropagation(bn_structure)

        # Aquí van los datos estimados por el modelo 
        datos_estimados = []

        # Iterar por todas las filas de la matriz
        for fila in matriz_datos_twitter:
            # Cada 'fila' es una fila completa de la matriz
            # Aquí puedes realizar operaciones en cada fila según sea necesario

            inference.setEvidence({'A1' : int(fila[0]), 'A2' : int(fila[1]), 'A3' : int(fila[2]), 'A4' : int(fila[3]), 'A5' : int(fila[4]), 'A6' : int(fila[5]), 'A7' : int(fila[6]), 'A8' : int(fila[7])})
            result = inference.posterior('C7A')

            # Procesar el resultado y añadirlo a la lista 'datos_estimados'
            resultado_procesado = metodos.procesar_resultado(result[0])
            datos_estimados.append(resultado_procesado)


        # Añadir la lista 'datos_estimados' como una nueva columna al final del DataFrame
        datos_twitter['DatosEstimados'] = datos_estimados

        # Guardar el DataFrame actualizado en el mismo archivo Excel
        datos_twitter.to_excel(excel, index=False)
        
        # Por último, deseamos obtener el ERROR Cuadrático Medio

        datos_error = pd.read_excel(excel, usecols=['C7A', 'DatosEstimados'])

        # Calcular el MSE entre las columnas 'C7A' y 'DatosEstimados'
        mse_pre = mean_squared_error(datos_error['C7A'], datos_error['DatosEstimados'])
        
        datos_reales = datos_twitter['C7A']

        # Aquí van los datos tras evaluar la red
        datos_red = []

        # Iterar para calcular la influencia del efecto red
        for dato_real, dato_estimado in zip(datos_reales, datos_estimados):
            resultado_procesado = metodos.efecto_red(dato_real, dato_estimado, 0.45)
            datos_red.append(resultado_procesado)


        datos_twitter['DatosTrasRed'] = datos_red    
        datos_twitter.to_excel(excel, index=False)

        # Por último, deseamos obtener el ERROR Cuadrático Medio

        datos_error = pd.read_excel(excel, usecols=['C7A', 'DatosTrasRed'])

        # Calcular el MSE entre las columnas 'C7A' y 'DatosEstimados'
        mse_post = mean_squared_error(datos_error['C7A'], datos_error['DatosTrasRed'])
                
    # Método para mostrar el error
    def mostrar_error():
        # Convertir el resultado a una cadena de texto
        texto_mse = f"Error Cuadrático Medio antes de Efecto Red (MSE): {mse_pre} \nError Cuadrático Medio tras Efecto Red (MSE): {mse_post}"

        # Crear un widget Text para mostrar el resultado
        cuadro_texto_mse = scrolledtext.ScrolledText(frame, width=60, height=4)
        cuadro_texto_mse.insert(tk.INSERT, texto_mse)
        cuadro_texto_mse.pack(padx=10, pady=10)
    
    # Método para cerrar ventana principal
    def salir():
        if ventana_twitter is not None:
            ventana_twitter.destroy()
    
    # Crear botones para las opciones del menú en el Frame
    button_mostrar_datos = tk.Button(frame, text="Mostrar Datos", command=mostrar_datos)
    button_analisis = tk.Button(frame, text="Análisis Twitter", command=analisis)
    button_error = tk.Button(frame, text="Mostrar Error Cuadrático Medio", command=mostrar_error)
    button_salir = tk.Button(frame, text="Salir", command=salir)

    # Colocar los botones en el Frame
    button_mostrar_datos.pack()
    button_analisis.pack()
    button_error.pack()
    button_salir.pack()