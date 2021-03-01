# -*- coding: utf-8 -*-
"""AlgpritmoFuzzyWuzzy y levesting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-PQLNKDQfE0M_AZvQG8GHjODLu0-j-HL

conexion con drive
"""

from google.colab import files
from google.colab import drive
drive.mount('/content/gdrive')

"""**LIBRERIA**"""

from time import time
start_nb = time()
start = time()

import pandas as pd
import re
from nltk import word_tokenize
import string

print('Importación de Librerias. %.2f segundos' % (time() - start))

"""**MOSTRAR** **DATASET**"""

dataset = pd.read_csv('//content/gdrive/My Drive/dataset.csv',
                      sep=';', encoding='utf-8-sig')
dataset.head(5)

"""**PREPROCESADO**"""

def preprocess(doc):
  
    strong = re.compile('<strong>.*?</strong>')
    doc = re.sub(strong, '', doc)

    etp = re.compile('<p>.*?.</p>') # Eliminación de contenido de la etiqueta <p>.
    doc = re.sub(etp, '', doc)

    pre = re.compile('<pre>|</pre>') # Eliminación de tag <pre>.
    doc = re.sub(pre, '', doc)

    tag = re.compile('[\s]*<code>|</code>[\s]*') # Eliminación de tag <code> y espacios.
    doc = re.sub(tag, '', doc)

    etp1 = re.compile('[\S]*<code>|</code>[\S]*') # Eliminación de contenido de la etiqueta <p>.
    doc = re.sub(etp1, '', doc)

    sigM = re.compile('&lt;') # Reemplazar la entidad &lt; por caracter <.
    doc = re.sub(sigM, '<', doc)

    sigm = re.compile('&gt;') # Reemplazar la entidad &gt; por caracter >.
    doc = re.sub(sigm, '>', doc)

    com = re.compile('&quot;') # Reemplazar la entidad &gt; por caracter >.
    doc = re.sub(com, '"', doc)

    amp = re.compile('&amp;') # Reemplazar la entidad &gt; por caracteror >.
    doc = re.sub(amp, '&', doc)

    p = re.compile('<.*?>') # Reemplazar la entidad &gt; por caracteror >.
    doc = re.sub(p, '', doc)

    doc = doc.lower()  # Minuscula todo el texto.
    #doc = word_tokenize(doc)  # Dividir en palabras.
    # doc = [w for w in doc if w.isalpha()]  # Eliminar numbers and punctuation.
    return doc

"""**CREACION DE COLUMNA P_BODY QUE GUARDA EL PREPROCESADO **"""

dataset['p_body'] = dataset.apply(
        lambda dataset: preprocess(dataset['Attribute:Body']), axis=1)

dataset.iloc[:,[2,5]]

print(dataset['Attribute:Body'][5])

print(dataset['p_body'][5])

dataset['p_body'][1001]

"""**GUARDAMOS EL DATASET EN UNA VARIABLE **"""

df = dataset
df

"""Coincidencia de cadenas difusas en Python

**FUZZY WUZZY**

DESCARGAMOS LAS LIBRERAS PARA UTILIZAR EL ALGORITMO
"""

!pip install fuzz
!pip install fuzzywuzzy

"""EJEMPLO PREVIO A LA EJECUCION

"""

from fuzzywuzzy import process
st = "apple inc"
strOptions = ["Apple Inc.","apple park","apple incorporated","iphone","apple inc"]
Ratios = process.extract(st,strOptions)
print(Ratios)
# You can also select the string with the highest matching percentage
highest = process.extractOne(st,strOptions)
print(highest)

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

a= dataset['p_body'][40]
b = [dataset['p_body'][40]]

res = process.extract(a,b,limit=100, scorer=fuzz.token_sort_ratio)
res

a

"""LIBRERIAS """

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

df.head()

data= df['p_body'].to_numpy()

#test = dataset.p_body.to_list()

#data [:5]

"""codigo unico"""

# data = df['p_body'].unique()
# data[:15]

"""validacion """

#query= "<?php localhost:8080 username=admin password=admin"

string = dataset['p_body'][995]
string
process.extract(string, dataset['p_body'], limit=4, scorer=fuzz.token_sort_ratio)

process.extract(string, dataset['p_body'], limit=4, scorer=fuzz.token_sort_ratio)

duplicado = process.extract(string, choices=dataset['p_body'], limit=4, scorer=fuzz.token_sort_ratio)

[i for i in duplicado if i[1] >50]

def get_ratio(row):
    name = row['p_body']
    return fuzz.token_sort_ratio(name, string)

df[df.apply(get_ratio, axis=1) > 50]

df[df.apply(lambda row: fuzz.token_sort_ratio(row['p_body'], string), axis=1) > 10]

"""Pickle Rick"""

fz = pd.read_csv('//content/gdrive/My Drive/fuzzy.csv',
                      sep=';', encoding='utf-8-sig')

fz.head()

fz = fz.fillna(0)

fz['Id'] = fz['Id'].astype(int)

fz[0:13]

fz.dtypes

fz.shape

# Save Model Using Pickle
import pandas
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle

array = fz.values
X = array[:,0:4]
Y = array[:,2]

X

Y

seed = 7
X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.20, random_state=seed)
# Fit the model on training set
model = LogisticRegression()
model.fit(X_train, Y_train)
# save the model to disk
filename = 'pickle.sav'
pickle.dump(model, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
print(result)

"""CURVA RO"""

fz['alzahrani']

fz

import numpy as np
from sklearn.metrics import roc_curve, auc
# calculate roc curves
fpr, tpr, thresholds = roc_curve(fz['is_similar'], fz['alzahrani'])
roc_auc = auc(fpr, tpr)

print("Area under the ROC curve : %f" % roc_auc)
from matplotlib import pyplot
# plot the roc curve for the model
pyplot.plot([0, 1], [0, 1], linestyle='--', label='No Skill')
pyplot.plot(fpr, tpr, marker='.', label='Logistic')
# axis labels
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
pyplot.legend()
# show the plot
pyplot.show()

gmeans = np.sqrt(tpr * (1 - fpr))
# locate the index of the largest g-mean
ix = np.argmax(gmeans)
print('Best Threshold = %f, G-Mean = %.3f' % (thresholds[ix], gmeans[ix]))
best_thresh = thresholds[ix]
fz['pred'] = np.where(fz["alzahrani"] > thresholds[ix], 1, 0)
#
# Python script for confusion matrix creation.
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
actual = fz['is_similar']
predicted = fz['pred']
results = confusion_matrix(actual, predicted)
print('Confusion Matrix :')
print(results)
print('Accuracy Score :', accuracy_score(actual, predicted))
print('Report : ')
print(classification_report(actual, predicted))
print('Best Threshold = %f' % (best_thresh))