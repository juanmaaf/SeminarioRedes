import tkinter as tk    # Librería para interfaz gráfica
from tkinter.simpledialog import askinteger # Para pedir información al usuario 
import pandas as pd

import metodos
import facebook
import instagram
import twitter
import sin_redes

# Almacenamos la ruta de los excel necesarios
datos_utiles = "/home/juanmaaf/Escritorio/Seminario/SeminarioRedes/datosUtiles.xlsx"
excel_corregido_sin_redes = "/home/juanmaaf/Escritorio/Seminario/SeminarioRedes/datosCorregidos_sin_redes.xlsx" 
excel_corregido_redes = "/home/juanmaaf/Escritorio/Seminario/SeminarioRedes/datosCorregidos_redes.xlsx" 
excel_facebook = "/home/juanmaaf/Escritorio/Seminario/SeminarioRedes/datosFacebook.xlsx" 
excel_twitter = "/home/juanmaaf/Escritorio/Seminario/SeminarioRedes/datosTwitter.xlsx" 
excel_instagram = "/home/juanmaaf/Escritorio/Seminario/SeminarioRedes/datosInstagram.xlsx"

# Método que crea los Excel para cada estudio partiendo de DatosUtiles
def excel_estudio():

    # Lee los datos del archivo Excel
    datos = pd.read_excel(datos_utiles, header=0)

    # Eliminar filas donde la variable C7 no es igual a 1
    datos = datos[datos['C7'] == 1]

    # Aplica la función de transformación a la columna C7A suponiendo que es la columna del voto
    datos['C7A'] = datos['C7A'].apply(metodos.transformar_voto)

    # Aplicamos la normalización a las columnas A1-A8
    datos['A1'] = datos['A1'].apply(metodos.normalizar)
    datos['A2'] = datos['A2'].apply(metodos.normalizar)
    datos['A3'] = datos['A3'].apply(metodos.normalizar)
    datos['A4'] = datos['A4'].apply(metodos.normalizar)
    datos['A5'] = datos['A5'].apply(metodos.normalizar)
    datos['A6'] = datos['A6'].apply(metodos.normalizar)
    datos['A7'] = datos['A7'].apply(metodos.normalizar)
    datos['A8'] = datos['A8'].apply(metodos.normalizar)

    # Eliminar filas con valor None en la columna C7A
    datos = datos[datos['C7A'].notna()]
    # Eliminar filas con valor None en la columna A1
    datos = datos[datos['A1'].notna()]
    # Eliminar filas con valor None en la columna A2
    datos = datos[datos['A2'].notna()]
    # Eliminar filas con valor None en la columna A3
    datos = datos[datos['A3'].notna()]
    # Eliminar filas con valor None en la columna A4
    datos = datos[datos['A4'].notna()]
    # Eliminar filas con valor None en la columna A5
    datos = datos[datos['A5'].notna()]
    # Eliminar filas con valor None en la columna A6
    datos = datos[datos['A6'].notna()]
    # Eliminar filas con valor None en la columna A7
    datos = datos[datos['A7'].notna()]
    # Eliminar filas con valor None en la columna A8
    datos = datos[datos['A8'].notna()]

    # No necesitamos C7
    datos = datos.drop('C7', axis=1)

    # Nos quedamos solamente con las filas en las que los electores NO usan las redes para seguir campaña
    # Quitamos las columnas referentes a las redes en el Excel sin redes
    datos_sin_redes = datos[datos['B11_5'] != 1]
    datos_sin_redes = datos_sin_redes.drop('B10_1', axis=1)
    datos_sin_redes = datos_sin_redes.drop('B10_2', axis=1)
    datos_sin_redes = datos_sin_redes.drop('B10_4', axis=1)
    datos_sin_redes = datos_sin_redes.drop('B11_5', axis=1)

    # Guarda los datos transformados en un nuevo archivo Excel
    datos_sin_redes.to_excel(excel_corregido_sin_redes, index=False)
    
    # Nos quedamos solamente con las filas en las que los electores usan las redes para seguir campaña
    # Quitamos las columnas referentes a las redes en el Excel sin redes
    datos = datos[datos['B11_5'] == 1]

    # Guarda los datos transformados en un nuevo archivo Excel
    datos.to_excel(excel_corregido_redes, index=False)

    datos_facebook = datos[datos['B10_1'] == 1]
    datos_facebook = datos_facebook.drop('B10_1', axis=1) 
    datos_facebook = datos_facebook.drop('B10_2', axis=1) 
    datos_facebook = datos_facebook.drop('B10_4', axis=1) 
    datos_facebook = datos_facebook.drop('B11_5', axis=1)

    datos_facebook.to_excel(excel_facebook, index=False)

    datos_twitter = datos[datos['B10_2'] == 1]
    datos_twitter = datos_twitter.drop('B10_1', axis=1) 
    datos_twitter = datos_twitter.drop('B10_2', axis=1) 
    datos_twitter = datos_twitter.drop('B10_4', axis=1) 
    datos_twitter = datos_twitter.drop('B11_5', axis=1)

    datos_twitter.to_excel(excel_twitter, index=False)

    datos_instagram = datos[datos['B10_4'] == 1]
    datos_instagram = datos_instagram.drop('B10_1', axis=1) 
    datos_instagram = datos_instagram.drop('B10_2', axis=1) 
    datos_instagram = datos_instagram.drop('B10_4', axis=1) 
    datos_instagram = datos_instagram.drop('B11_5', axis=1)

    datos_instagram.to_excel(excel_instagram, index=False)

# Función principal
def main():
    global root
    
    excel_estudio()
    
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Seminario Redes")

    # Crear un Frame para el menú principal
    frame = tk.Frame(root)
    frame.pack(pady=5)
    
    # Agregar un título "Menú Principal" con letras en negrita en el Frame
    titulo = tk.Label(frame, text="Menú Principal", font=("Helvetica", 16, "bold"))
    titulo.pack(pady=10)

    # Método para cerrar ventana principal
    def salir():
        if root is not None:
            root.destroy()
        
    # Crear botones para las opciones del menú en el Frame
    button_sin_redes = tk.Button(frame, text="Estudio Sin Redes", command=lambda:sin_redes.estudio_sin_redes(root, excel_corregido_sin_redes))
    #button_facebook = tk.Button(frame, text="Estudio Influencia Facebook", command=lambda:facebook.estudio_facebook(root))
    #button_twitter = tk.Button(frame, text="Estudio Influencia Twitter", command=lambda:twitter.estudio_twitter(root))
    #button_instagram = tk.Button(frame, text="Estudio Influencia Instagram", command=lambda:instagram.estudio_instagram(root))
    button_salir = tk.Button(frame, text="Salir", command=salir)

    # Colocar los botones en el Frame
    button_sin_redes.pack()
    #button_facebook.pack()
    #button_twitter.pack()
    #button_instagram.pack()
    button_salir.pack()
    
    # Iniciar la interfaz
    root.mainloop()

if __name__ == "__main__":
    main()

