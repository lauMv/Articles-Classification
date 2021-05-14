import spacy

articulos = ['El sistema de defensa antimisiles israelí, creado para detectar u neutralizar cohetes y proyectiles en una distancia de cinco a más de 100 kilómetros, está funcionando a pleno estos días.'
,'El proyecto de ley establece que la operadora argentina YPFB Exploración & Producción de Hidrocarburos Bolivia S.A. cede el 40 por ciento de su participación, derechos y obligaciones a la subsidiaria YPFB Chaco S.A.']

nlp = spacy.load('es_core_news_md')
print(nlp.pipe_names)

with nlp.disable_pipes('tok2vec', 'morphologizer', 'parser', 'ner', 'attribute_ruler', 'lemmatizer'):
    docs = list(nlp.pipe(articulos))
    for doc in docs:
        print([(token.text, token.is_stop, token.is_digit)  for token in doc])

        #'El sistema de defensa antimisiles israelí, creado' -> 'sistema defensa antimisiles israelí creado'