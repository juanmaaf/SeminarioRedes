import tkinter as tk    # Librería para interfaz gráfica
from tkinter.simpledialog import askinteger # Para pedir información al usuario 
from tkinter import scrolledtext
import pandas as pd
import pyAgrum as gum
import metodos
from sklearn.metrics import mean_squared_error

mse = None

def estudio_sin_redes(ventana, excel):
    global ventana_sin_redes
    
    # Estudio SIN REDES

    # Lista de nombres de columnas que deseas seleccionar
    columnas_seleccionadas = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "C7A"]

    # Cargar solo las columnas seleccionadas desde el archivo Excel utilizando pandas
    datos_sin_redes = pd.read_excel(excel, usecols=columnas_seleccionadas, header=0)
    
    # Crear una nueva ventana para mostrar el valor de las tablas
    ventana_sin_redes = tk.Toplevel(ventana)
    ventana_sin_redes.title("Seminario Redes")

    # Crear un Frame para el menú principal
    frame = tk.Frame(ventana_sin_redes)
    frame.pack(pady=5)
    
    # Agregar un título "Menú Principal" con letras en negrita en el Frame
    titulo = tk.Label(frame, text="Estudio Sin Redes", font=("Helvetica", 16, "bold"))
    titulo.pack(pady=10)

    # Método para mostrar los datos
    def mostrar_datos():
        # Convertir los datos a una cadena de texto
        texto_datos = datos_sin_redes.to_string(index=False)

        # Crear un widget Text para mostrar los datos
        cuadro_texto = scrolledtext.ScrolledText(frame, width=60, height=10)
        cuadro_texto.insert(tk.INSERT, texto_datos)
        cuadro_texto.pack(padx=10, pady=10)
    
    # Método para realizar el análisis
    def analisis():
        global mse
        
        # Crear un objeto BN Learner
        learner = gum.BNLearner(datos_sin_redes)

        # Utilizar un criterio específico para la estructura y parámetros
        learner.useScoreBDeu()

        # Aprender la estructura de la red
        bn_structure = learner.learnBN()
        
        # Convertir el DataFrame a una matriz de NumPy
        matriz_datos_sin_redes = datos_sin_redes.to_numpy()

        # Eliminar la última columna de la matriz
        matriz_datos_sin_redes = matriz_datos_sin_redes[:, :-1]
        
        # Posterior inferencia

        # Crear un inferidor de red bayesiana
        inference = gum.LazyPropagation(bn_structure)

        # Aquí van los datos estimados por el modelo 
        datos_estimados = []

        # Iterar por todas las filas de la matriz
        for fila in matriz_datos_sin_redes:
            # Cada 'fila' es una fila completa de la matriz
            # Aquí puedes realizar operaciones en cada fila según sea necesario

            inference.setEvidence({'A1' : int(fila[0]), 'A2' : int(fila[1]), 'A3' : int(fila[2]), 'A4' : int(fila[3]), 'A5' : int(fila[4]), 'A6' : int(fila[5]), 'A7' : int(fila[6]), 'A8' : int(fila[7])})
            result = inference.posterior('C7A')

            # Procesar el resultado y añadirlo a la lista 'datos_estimados'
            resultado_procesado = metodos.procesar_resultado(result[0])
            datos_estimados.append(resultado_procesado)
            
        # Añadir la lista 'datos_estimados' como una nueva columna al final del DataFrame
        datos_sin_redes['DatosEstimados'] = datos_estimados

        # Guardar el DataFrame actualizado en el mismo archivo Excel
        datos_sin_redes.to_excel(excel, index=False)
        
        # Por último, deseamos obtener el ERROR Cuadrático Medio

        datos_error = pd.read_excel(excel, usecols=['C7A', 'DatosEstimados'])

        # Calcular el MSE entre las columnas 'C7A' y 'DatosEstimados'
        mse = mean_squared_error(datos_error['C7A'], datos_error['DatosEstimados'])
                
    # Método para mostrar el error
    def mostrar_error():
        # Convertir el resultado a una cadena de texto
        texto_mse = f"Error Cuadrático Medio (MSE): {mse}"

        # Crear un widget Text para mostrar el resultado
        cuadro_texto_mse = scrolledtext.ScrolledText(frame, width=50, height=3)
        cuadro_texto_mse.insert(tk.INSERT, texto_mse)
        cuadro_texto_mse.pack(padx=10, pady=10)
    
    # Método para cerrar ventana principal
    def salir():
        if ventana_sin_redes is not None:
            ventana_sin_redes.destroy()
    
    # Crear botones para las opciones del menú en el Frame
    button_mostrar_datos = tk.Button(frame, text="Mostrar Datos", command=mostrar_datos)
    button_analisis = tk.Button(frame, text="Análisis Sin Redes", command=analisis)
    button_error = tk.Button(frame, text="Mostrar Error Cuadrático Medio", command=mostrar_error)
    button_salir = tk.Button(frame, text="Salir", command=salir)

    # Colocar los botones en el Frame
    button_mostrar_datos.pack()
    button_analisis.pack()
    button_error.pack()
    button_salir.pack()