# SeminarioRedes
Proyecto Seminario Red Bayesiana con Influencia de Redes Sociales

Autor: Juan Manuel Aneas Franco
GitHub: Juanmaaf

Requisitos necesarios:
    Librerías:
        -tkinter
            *Intalación Ubuntu: sudo apt-get install python3-tk
            *Intalación Windows: En la mayoría de los casos, Tkinter debería instalarse automáticamente con la instalación de Python en sistemas Windows. Si no lo tienes, generalmente es mejor reinstalar Python e incluir la opción para instalar Tcl/Tk y las bibliotecas Tcl/Tk.
            Al instalar Python en Windows, asegúrate de seleccionar la opción "Add Tcl/Tk support" durante la instalación.
            Si ya tienes Python instalado, puedes intentar reinstalarlo y asegurarte de marcar la opción mencionada.
        -pandas
            pip install pandas
        -pyAgrum
            pip install pyagrum
        -sklearn
            pip install scikit-learn

Funcionalidad:
    Archivo metodos.py:
        Se implementan 4 métodos, acompañados de su correspondiente descripción, que se emplean durante el proyecto.
    Archivo main.py:
        - Archivo principal. Inicialmente filtra los datos del Excel de Datos Útiles y crea un excel con los datos asociados a cada estudio.
            *** IMPORTANTE *** Se deben cambiar las rutas a cada Excel (al principio del archivo)
            Finalmente, a través de la interfaz gráfica, da paso a los 4 distintos análisis (Sin Redes, Facebook, Twitter e Instagram)
        - Archivo facebook.py: 
            La interfaz gráfica permite varias operaciones:
                1. Mostrar los datos actuales del excel de facebook
                2. Realizar el análisis de este caso (Datos de la Red Bayesiana y aplicación Efecto Red). Finalmente calcula el Error Cuadrático Medio
                3. Muestra el ERROR
        - Archivo twitter.py e instagram.py:
            Equivalentes a facebook.py pero aplicando los datos referentes a Twitter e Instagram, respectivamente.
        - Archivo sin_redes.py:
            Equivalente a facebook.py pero en el análisis no se tiene en cuenta efecto red. Solo se calcula el error en función de los datos mostrados por el modelo.
            En este caso no hay cambio de la decisión.
        


