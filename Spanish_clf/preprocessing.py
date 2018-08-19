import string


ESPECIALES_ESPANOL="áéíóúÁÉÍÓÚñÑüÜ"


def separar_puntuacion(texto):
    mapping = [(p, ' '+ p +' ') for p in string.punctuation]
    for k, v in mapping:
        texto = texto.replace(k, v)
    return texto


def procesar_negacion(texto, tokenizador=lambda x: x.split(), \
                      separador_puntuacion = None,
                      palabras_negativas = ['no','sin','nunca'], devolver_texto=True):
    if separador_puntuacion: #separamos puntuaciones que esten pegadas a las palabras
        texto = separador_puntuacion(texto)
    else:
        mapping = [(p, ' '+ p +' ') for p in string.punctuation]
        for k, v in mapping:
            texto = texto.replace(k, v)
        
    tokens = tokenizador(texto)
    tokens_negados = []
    
    
    
    oracion_negada = False
    for token in tokens:
        if token.lower() in palabras_negativas: #inicio de oracion negativa
            oracion_negada = True
            tokens_negados.append(token)
            continue
        if token in string.punctuation: #fin de oracion negativa
            oracion_negada = False
            tokens_negados.append(token)
            continue
        if oracion_negada: #cuerpo de oracion negativa
            tokens_negados.append("NO_" + token)
            continue
        #cuerpo de oracion positiva:
        tokens_negados.append(token)
    
    if devolver_texto:
        return ' '.join(tokens_negados)
    else:
        return tokens_negados



    
    
