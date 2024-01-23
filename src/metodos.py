import random

# Método para pasar los datos de la columna voto a 0,1
# Este método se emplea para pasar los datos que proporciona la encuesta del CIS, referentes a los distintos partidos,
# a 1 si se ha votado al PSOE(2), o 0 si no se ha votado al PSOE. 
def transformar_voto(partido):
    if partido == 2:  # PSOE
        return 1
    else:
        return 0 if partido not in {98, 99} else None

# Método para normalizar los valores de las situaciones -> 1-3 pasará a 0-2 y 1-5 pasará a 0-4
# Este método se utiliza porque la encuesta del CIS muestra los valores de 1 hasta el valor máximo,
# y el BNLearnes de PyAgrum necesita los valores desde o hasta el valor máximo.
def normalizar(valor):
    return valor-1 if valor not in {8, 9} else None

# Este método se emplea para definir el dato estimado. El BNLearner de la librería PyAgrum nos devuelve como resultado al inferir una probabilidad para 0 y para 1.
# Trabajando con la primera (probabilidad para votar 0), ese valor entra en este método. En primer lugar, se planteó tomar el valor 0 si su probabilidad asociada 
# superaba el 50%. Ocurre un problema para el estudio de las redes. Todas las probabilidades para 0 en el caso de redes eran superiores al 50%, por lo que nunca 
# se estimaba un 1. Decicí que la decisión se tomase con certeza cuando el porcentaje superase el 65%. Voto a 0 cuando P(0) > 65%. Voto a 1 cuando P(0) < 35%.
# Finalmente, para ese intervalo central de probabilidad, he optado por una elección 50/50. Así, en el estudio de las redes, han aparecido estimados algunos 1s.
def procesar_resultado(resultado):
    if resultado > 0.65:
        # No se vota al partido del Gobierno
        return 0
    elif resultado < 0.35:
        # Se vota al partido del Gobierno
        return 1
    else:
        random.seed()
        numero_aleatorio = random.randint(1, 100)
        if numero_aleatorio < 50: 
            return 0
        else:
            return 1
        
# Este método es el que empleamos para aplicar el efecto red en el estudio del caso con redes, sea con FACEBOOK, INSTAGRAM 
# o Twitter
# Muy Sencillo. Si el dato real difiere del estimado por el modelo, ¿cómo nos influenciamos?. Aplicamos una probabilidad,
# que se ha decidido que sea 45% (cuando se llame a este método se empleará ese valor) y generamos un número aleatorio  entre 0 y 1.
# Si el número aleatorio es menor a la probabilidad en tanto por 1, se cambia la decisión. En caso contrario, se mantiene el dato estimado.
def efecto_red(dato_real, dato_estimado, probabilidad_cambio):
    diferencia = abs(dato_real - dato_estimado)
    probabilidad = min(probabilidad_cambio * diferencia, 1.0)
    
    random.seed()
    if random.random() < probabilidad: # Cambio de decisión
        if(dato_estimado == 0):
            return 1
        else:
            return 0
    else:
        return dato_estimado
