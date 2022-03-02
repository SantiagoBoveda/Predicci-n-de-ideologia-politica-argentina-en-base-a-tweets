from flask import Flask, jsonify, render_template, url_for, request, redirect, send_file, Response, make_response
import pickle
import unidecode
import re

# import pandas as pd
# import numpy as np

# UPLOAD_FOLDER = 'static/uploads'
# pd.options.mode.chained_assignment = None  # default='warn'

app = Flask(__name__)
# app = application
# app.secret_key = b'{\xef~\x17\xe9\xc3\xd0\x1d\x806F\xb2\xc9\xed\xf9!\x91\xc5\xf0\x0f!\xde\x97V'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


with open('pickle/model_no_sw_232993.pickle', 'rb') as f:
    model = pickle.load(f)

with open('pickle/vectorizer_no_sw_232993.pickle', 'rb') as v:
    vectorizer = pickle.load(v)



with open('pickle/model_canciones.pickle', 'rb') as f:
    model_canciones = pickle.load(f)

with open('pickle/vectorizer_canciones.pickle', 'rb') as v:
    vectorizer_canciones = pickle.load(v)



def limpiar_textos(tweet):
    t_lower_no_accents=unidecode.unidecode(tweet.lower()); # sacamos acentos y llevamos a minuscula
    t_lower_no_accents_no_punkt=re.sub(r'([^\s\w]|_)+','',t_lower_no_accents); # quitamos signos de puntuacion usando una regex que reemplaza todo lo q no sean espacios o palabras por un string vacio
    t_no_new_line = t_lower_no_accents_no_punkt.replace('\n', ' ')
    t_remove_http = re.sub(r'http\S+', '', t_no_new_line).strip()
    x = re.sub("(.)\\1{2,}", "\\1", t_remove_http)
    return x

stopwords_list = [
    'de',
    'la',
    'que',
    'el',
    'en',
    'y',
    'a',
    'los',
    'del',
    'se',
    'las',
    'por',
    'un',
    'para',
    'con',
    'no',
    'una',
    'su',
    'al',
    'lo',
    'como',
    'mas',
    'pero',
    'sus',
    'le',
    'ya',
    'o',
    'este',
    'si',
    'porque',
    'esta',
    'entre',
    'cuando',
    'muy',
    'sin',
    'sobre',
    'tambien',
    'me',
    'hasta',
    'hay',
    'donde',
    'quien',
    'desde',
    'todo',
    'nos',
    'durante',
    'todos',
    'uno',
    'les',
    'ni',
    'contra',
    'otros',
    'ese',
    'eso',
    'ante',
    'ellos',
    'e',
    'esto',
    'mi',
    'antes',
    'algunos',
    'que',
    'unos',
    'yo',
    'otro',
    'otras',
    'otra',
    'el',
    'tanto',
    'esa',
    'estos',
    'mucho',
    'quienes',
    'nada',
    'muchos',
    'cual',
    'poco',
    'ella',
    'estar',
    'estas',
    'algunas',
    'algo',
    'nosotros',
    'mi',
    'mis',
    'tu',
    'te',
    'ti',
    'tu',
    'tus',
    'ellas',
    'nosotras',
    'vosotros',
    'vosotras',
    'os',
    'mio',
    'mia',
    'mios',
    'mias',
    'tuyo',
    'tuya',
    'tuyos',
    'tuyas',
    'suyo',
    'suya',
    'suyos',
    'suyas',
    'nuestro',
    'nuestra',
    'nuestros',
    'nuestras',
    'vuestro',
    'vuestra',
    'vuestros',
    'vuestras',
    'esos',
    'esas',
    'estoy',
    'estas',
    'esta',
    'estamos',
    'estais',
    'estan',
    'este',
    'estes',
    'estemos',
    'esteis',
    'esten',
    'estare',
    'estaras',
    'estara',
    'estaremos',
    'estareis',
    'estaran',
    'estaria',
    'estarias',
    'estariamos',
    'estariais',
    'estarian',
    'estaba',
    'estabas',
    'estabamos',
    'estabais',
    'estaban',
    'estuve',
    'estuviste',
    'estuvo',
    'estuvimos',
    'estuvisteis',
    'estuvieron',
    'estuviera',
    'estuvieras',
    'estuvieramos',
    'estuvierais',
    'estuvieran',
    'estuviese',
    'estuvieses',
    'estuviesemos',
    'estuvieseis',
    'estuviesen',
    'estando',
    'estado',
    'estada',
    'estados',
    'estadas',
    'estad',
    'he',
    'has',
    'ha',
    'hemos',
    'habeis',
    'han',
    'haya',
    'hayas',
    'hayamos',
    'hayais',
    'hayan',
    'habre',
    'habras',
    'habra',
    'habremos',
    'habreis',
    'habran',
    'habria',
    'habrias',
    'habriamos',
    'habriais',
    'habrian',
    'habia',
    'habias',
    'habiamos',
    'habiais',
    'habian',
    'hube',
    'hubiste',
    'hubo',
    'hubimos',
    'hubisteis',
    'hubieron',
    'hubiera',
    'hubieras',
    'hubieramos',
    'hubierais',
    'hubieran',
    'hubiese',
    'hubieses',
    'hubiesemos',
    'hubieseis',
    'hubiesen',
    'habiendo',
    'habido',
    'habida',
    'habidos',
    'habidas',
    'soy',
    'eres',
    'es',
    'somos',
    'sois',
    'son',
    'sea',
    'seas',
    'seamos',
    'seais',
    'sean',
    'sere',
    'seras',
    'sera',
    'seremos',
    'sereis',
    'seran',
    'seria',
    'serias',
    'seriamos',
    'seriais',
    'serian',
    'era',
    'eras',
    'eramos',
    'erais',
    'eran',
    'fui',
    'fuiste',
    'fue',
    'fuimos',
    'fuisteis',
    'fueron',
    'fuera',
    'fueras',
    'fueramos',
    'fuerais',
    'fueran',
    'fuese',
    'fueses',
    'fuesemos',
    'fueseis',
    'fuesen',
    'sintiendo',
    'sentido',
    'sentida',
    'sentidos',
    'sentidas',
    'siente',
    'sentid',
    'tengo',
    'tienes',
    'tiene',
    'tenemos',
    'teneis',
    'tienen',
    'tenga',
    'tengas',
    'tengamos',
    'tengais',
    'tengan',
    'tendre',
    'tendras',
    'tendra',
    'tendremos',
    'tendreis',
    'tendran',
    'tendria',
    'tendrias',
    'tendriamos',
    'tendriais',
    'tendrian',
    'tenia',
    'tenias',
    'teniamos',
    'teniais',
    'tenian',
    'tuve',
    'tuviste',
    'tuvo',
    'tuvimos',
    'tuvisteis',
    'tuvieron',
    'tuviera',
    'tuvieras',
    'tuvieramos',
    'tuvierais',
    'tuvieran',
    'tuviese',
    'tuvieses',
    'tuviesemos',
    'tuvieseis',
    'tuviesen',
    'teniendo',
    'tenido',
    'tenida',
    'tenidos',
    'tenidas',
    'tened'
]

stopwords_es = set(stopwords_list)

# stopwords_en_stem = [stemmer.stem(x) for x in stopwords_es]
# stopwords_en_uni = [stemmer.stem(unidecode.unidecode(x.lower())) for x in stopwords_es]


# @app.route('/pruebas', methods=['POST', 'GET'])
# def pruebas():
    
#     global stopwords_es
#     global stemmer

#     texto = 'Exportado al final de la primera notebook. Se agregaron y filtraron los partidos y bloques, se quitaron tweets viejos.'
#     clean_text = ' '.join([word.lower() for word in texto.split() if word.lower() not in stopwords_es])
#     stemm_text = ' '.join([stemmer.stem(y) for y in clean_text.split(" ")])

#     return jsonify(stemm_text)



@app.route('/', methods=['POST', 'GET'])
def inicio():



    return render_template('inicio.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():

    def limpiar_tweets(tweet):
        t_lower_no_accents=unidecode.unidecode(tweet.lower()); # sacamos acentos y llevamos a minuscula
        t_lower_no_accents_no_punkt=re.sub(r'([^\s\w]|_)+','',t_lower_no_accents); # quitamos signos de puntuacion usando una regex que reemplaza todo lo q no sean espacios o palabras por un string vacio
        t_no_new_line = t_lower_no_accents_no_punkt.replace('\n', ' ')
        t_remove_http = re.sub(r'http\S+', '', t_no_new_line).strip()
        x = re.sub("(.)\\1{2,}", "\\1", t_remove_http)
        return x

    global vectorizer
    global model
    global stopwords_es
    # global stemmer

    if request.method == 'POST':

        tweet = request.form['tweet']

    cleaned_tweet = limpiar_tweets(tweet)

    clean_text = ' '.join([word.lower() for word in cleaned_tweet.split() if word.lower() not in stopwords_es])
    # stemm_text = ' '.join([stemmer.stem(y) for y in clean_text.split(" ")])

    pred = model.predict(vectorizer.transform([clean_text]))[0]
    
    if pred == 0:
        bloque = 'Juntos por el Cambio'
        imagen = '../static/images/2560px-Juntos-Por-El-Cambio-Logo.png'

    else:
        bloque = 'Frente de Todos'
        imagen = '../static/images/2560px-Frente_de_Todos_logo.png'

    return render_template('partido-politico-probable.html', bloque=bloque, imagen=imagen, tweet=tweet)




@app.route('/promedio-10-tweets', methods=['POST', 'GET'])
def mean_10_tweets():



    return render_template('promedio-10-tweets.html')



@app.route('/predecir-promedio-10-tweets', methods=['POST', 'GET'])
def mean_10_tweets_predict():

    def limpiar_tweets(tweet):
        t_lower_no_accents=unidecode.unidecode(tweet.lower()); # sacamos acentos y llevamos a minuscula
        t_lower_no_accents_no_punkt=re.sub(r'([^\s\w]|_)+','',t_lower_no_accents); # quitamos signos de puntuacion usando una regex que reemplaza todo lo q no sean espacios o palabras por un string vacio
        t_no_new_line = t_lower_no_accents_no_punkt.replace('\n', ' ')
        t_remove_http = re.sub(r'http\S+', '', t_no_new_line).strip()
        x = re.sub("(.)\\1{2,}", "\\1", t_remove_http)
        return x

    global vectorizer
    global model
    global stopwords_es
    # global stemmer

    if request.method == 'POST':

        todos_los_tweets = []
        for i in range(1, 11):
            tweet = request.form['tweet' + str(i)]
            if len(tweet) > 0:
                todos_los_tweets.append(tweet)

        valoracion_de_tweets = []
        for j in range(len(todos_los_tweets)):
            print(todos_los_tweets[j])
            cleaned_tweet = limpiar_tweets(todos_los_tweets[j])
            clean_text = ' '.join([word.lower() for word in cleaned_tweet.split() if word.lower() not in stopwords_es])
            # stemm_text = ' '.join([stemmer.stem(y) for y in clean_text.split(" ")])
            pred = model.predict(vectorizer.transform([clean_text]))[0]
            valoracion_de_tweets.append(pred)

        promedio = sum(valoracion_de_tweets) / len(valoracion_de_tweets)
        porcentaje = promedio * 100

        porcentaje_jc = 50 + (50 - porcentaje)
        porcentaje_ft = 50 + (porcentaje - 50)
        
        len_tweets = len(todos_los_tweets)

        if promedio < 0.5:
            bloque = 'Juntos por el Cambio'
            imagen = '../static/images/2560px-Juntos-Por-El-Cambio-Logo.png'
            grado = porcentaje_jc
        else:
            bloque = 'Frente de Todos'
            imagen = '../static/images/2560px-Frente_de_Todos_logo.png'
            grado = porcentaje_ft

    return render_template('promedio-10-tweets-resultado.html', bloque=bloque, imagen=imagen, promedio=promedio, tweets=todos_los_tweets, len_tweets=len_tweets, grado=grado)








@app.route('/versos', methods=['POST', 'GET'])
def versos():



    return render_template('versos.html')



@app.route('/predict-verso', methods=['POST', 'GET'])
def predict_verso():

    def limpiar_texto(texto):
        t_lower_no_accents=unidecode.unidecode(texto.lower()); # sacamos acentos y llevamos a minuscula
        t_lower_no_accents_no_punkt=re.sub(r'([^\s\w]|_)+','',t_lower_no_accents); # quitamos signos de puntuacion usando una regex que reemplaza todo lo q no sean espacios o palabras por un string vacio
        t_no_new_line = t_lower_no_accents_no_punkt.replace('\n', ' ')
        t_remove_http = re.sub(r'http\S+', '', t_no_new_line).strip()
        x = re.sub("(.)\\1{2,}", "\\1", t_remove_http)
        return x

    global vectorizer_canciones
    global model_canciones

    if request.method == 'POST':

        verso = request.form['verso']


    verso_clean = limpiar_texto(verso)
    pred = model_canciones.predict(vectorizer_canciones.transform([verso_clean]))[0]
    

    if pred == 0:
        artista = 'Calamaro'
        imagen = '../static/images/calamaro.jpeg'

    elif pred == 1:
        artista = 'Spinetta'
        imagen = '../static/images/spinetta.jpeg'

    else:
        bloque = 'Shakira'
        imagen = '../static/images/shakira.jpeg'

    return render_template('artista.html', artista=artista, imagen=imagen, verso=verso)






######## Para que corra en mi compu ########
if __name__ == '__main__':
    app.run(debug=True, port=7000)



### PARA ENCENDER: 
# source venv/bin/activate
# python3 app.py

## PARA DESCONECTAR:
# deactivate


### TAMBIEN, SE PUEDE:
# export FLASK_APP="application.py"
# flask run
