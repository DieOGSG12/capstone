import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer #Para pasar las palabras a su forma raíz
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers.schedules import ExponentialDecay 
import random
nltk.download('punkt_tab')

data_file = open('intents_capstone.json', 'r', encoding='utf-8').read()
intents = json.loads(data_file)

lemmatizer = WordNetLemmatizer()

words=[]
classes = []
documents = []
ignore_words = ['?', '!']

## recorre cada intencion y sus patrones en el archivo JSON 
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokeniza las palabras en cada patron y las agrega a la lista de palabras
        W = nltk.word_tokenize(pattern)
        words.extend(W)
        # Agrega el par (patron, etiqueta) a la lista de documentacion
        documents.append((W, intent['tag']))
        # Si la etiqueta no esta en la lista de clases, la agrega
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lematiza las palabras y las convierte en minusculas, excluyendo las palabras ignoradas
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Guarda las listas de palabras y clases en archivos pickle
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

# Crea el conjunto de entrenamiento
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for word in words:
        # Crea una bolsa de palabras binaria para cada patron
        bag.append(1) if word in pattern_words else bag.append(0)
    output_row = list(output_empty)
    # Crea un vector de salida con un 1 en la posicion correspondiente a la etiqueta de la intencion
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# Mezcla aleatoreamente el conjunto de entrenamiento
random.shuffle(training)

# Divide el conjunto de entrenamiento en caracteristicas (train_x) y etiquetas (train_y)
train_x = [row[0] for row in training]
train_y = [row[1] for row in training]

train_x = np.array(train_x)
train_y = np.array(train_y)

# Crea el modelo de red neuronal
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Configura el optimizador con una tasa de aprendizaje exponencial decreciente
lr_schedule = ExponentialDecay(
    initial_learning_rate=0.01,
    decay_steps=10000,
    decay_rate=0.9)

sgd = SGD(learning_rate=lr_schedule, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Entrena el modelo con el conjunto  de entrenamiento
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

# Guarda el modelo entrenando en un archivo h5
model.save('chatbot_model.h5', hist)

print("model created")  ### esto es para entrenar el chat