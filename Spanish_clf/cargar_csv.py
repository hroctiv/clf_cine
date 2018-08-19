import pandas as pd
from preprocessing import procesar_negacion


def load_data(filename = None,procesar_no = False, as_tuples = True, include_body = True):
    """ Devuelve los reviews de peliculas junto con su clasificacion (0: desaprobacion, 1: aprobacion)
        Parametros:
          filename = nombre del archivo csv a cargar
          procesar_no: en caso sea True, devuelve texto con 'oraciones negativas'
                       (al encontrar un 'no', antepone 'NO_' a cada token que encuentra).
          as_tuples: en caso sea True, devuelve una lista de tuplas de la forma[(review, clasificacion), ...].
                     de lo contrario, devuelve dos listas: reviews, clasificaciones.
          include_body: en caso sea True, incluye la parte 'body' del review, al ser extenso, este
                        podria ser obviado para acelerar el entrenamiento."""
    if not filename:
        filename = "corpus/corpusCine/resenas.csv"

    dfResenas = pd.read_csv(filename,delimiter='|',quotechar='^')
    dfResenas.summary = dfResenas.summary.fillna('')
    dfResenas.body = dfResenas.body.fillna('')
    
    # Nos deshacemos de la 'ambigüedad' en las reseñas
    dfResenas = dfResenas.loc[~(dfResenas['rank'] == 3)]
    
    # Creamos las categorias de sentimiento:
    dfResenas['opinion'] = dfResenas['rank'].apply(lambda x: 1 if x > 3 else 0)
    

    if include_body:
        texto_resenas = dfResenas.summary + " " + dfResenas.body
    else:
        texto_resenas = dfResenas.summary
    
    if procesar_no:
        texto_resenas = texto_resenas.apply(procesar_negacion)
    if as_tuples:
        return [t for t in zip(texto_resenas, dfResenas.opinion)]
    else:                                             
        return texto_resenas.tolist(), dfResenas.opinion.tolist()