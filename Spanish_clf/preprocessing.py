import string
from nltk.stem import SnowballStemmer
from nltk.stem.snowball import SpanishStemmer
import es_core_news_md


ESPECIALES_ESPANOL="áéíóúÁÉÍÓÚñÑüÜ"

#preprocesador basico
def en_minusculas(texto):
    return texto.lower()


#tokenizador basico
def tokenizador_dummy(texto):
    return texto.split()


#Funciones de preprocesamiento (devuelven texto):
def separar_puntuacion(texto, mapping=[(p, ' '+ p +' ') for p in string.punctuation]):
    if not mapping:
        mapping = [(p, ' '+ p +' ') for p in string.punctuation]
    for k, v in mapping:
        texto = texto.replace(k, v)
    return texto




def sin_puntuacion(texto,mapping = [(p, ' ') for p in string.punctuation]):
    if not mapping:
        mapping = [(p, ' ') for p in string.punctuation]
    for k, v in mapping:
        texto = texto.replace(k, v)
    return texto

def en_minusculas_sin_puntuacion(texto):
    return sin_puntuacion(texto.lower())

def procesar_negacion(texto, tokenizador=tokenizador_dummy, \
                      separador_puntuacion = None,
                      palabras_negativas = ['no','sin','nunca'], devolver_texto=True):
    if separador_puntuacion: #separamos puntuaciones que esten pegadas a las palabras
        texto = separador_puntuacion(texto)
    else:
        texto = separar_puntuacion(texto)
        
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




#tokenizadores
def tokenizador_negacion(texto):
    return procesar_negacion(texto, separador_puntuacion=separar_puntuacion, devolver_texto=False)
    
    



def tokenizador_snowball_stem(texto, stemmer = SpanishStemmer()):
    texto = separar_puntuacion(texto)
    return [stemmer.stem(token) for token in texto.split()]

def tokenizador_spacy_simple(texto, nlp = es_core_news_md.load()):
    return [token.text for token in nlp(texto)]

def tokenizador_spacy_lemma(texto, nlp = es_core_news_md.load()):
    return [token.lemma_ for token in nlp(texto)]
