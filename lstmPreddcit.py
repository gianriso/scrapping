from pandas.core.tools.datetimes import to_datetime

import numpy as np
np.random.seed(4)
import matplotlib.pyplot as plt
#%matplotlib inline
import pandas as pd
from datetime import datetime

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import io


def graficar_predicciones(real, prediccion):
    plt.plot(real[0:len(prediccion)],color='red', label='Valor real de la acción')
    plt.plot(prediccion, color='blue', label='Predicción de la acción')
    plt.ylim(1.1 * np.min(prediccion)/2, 1.1 * np.max(prediccion))
    plt.xlabel('Tiempo')
    plt.ylabel('Valor de la acción')
    plt.legend()
    plt.show()


def export(prediccion, real):
    print(real)    
    print('funcion real  --->  ')
    real= real[0:len(prediccion)]
    real['Fecha'] = real.plot(legend=False)   
    col1 = "Reales" #datos reales u originales
    col2 = "Datos"
    data = pd.DataFrame({col1:real.iloc[:,0],col2:prediccion})
    data.to_excel('euro_predict.xlsx', sheet_name='hoja1', index=False)



#
# Lectura de los datos
#

#dataset= pd.read_csv(io.BytesIO(uploaded['EURUSD2.csv']))
dataset = pd.read_csv('EURUSD2.csv', index_col='Fecha', parse_dates=['Fecha'])
dataset.head()

#
# Sets de entrenamiento y validación 
# La LSTM se entrenará con datos de 2019 hacia atrás. La validación se hará con datos de 2020 en adelante.
# En ambos casos sólo se usará el valor más alto de la acción para cada día
#
set_entrenamiento = dataset[:'2019-12-31'].iloc[:,1:4]
set_validacion = dataset['2020-01-01':].iloc[:,1:4]

print(set_entrenamiento)

# Normalización del set de entrenamiento
sc = MinMaxScaler(feature_range=(0,1))
set_entrenamiento_escalado = sc.fit_transform(set_entrenamiento)




set_entrenamiento['Máximo'] = set_entrenamiento.plot(legend=True)
set_validacion['Máximo'] = set_validacion.plot(legend=True)
plt.legend(['Entrenamiento (2017-2019)', 'Validación (2020)'])
plt.show()


# La red LSTM tendrá como entrada "time_step" datos consecutivos, y como salida 1 dato (la predicción a
# partir de esos "time_step" datos). Se conformará de esta forma el set de entrenamiento
time_step = 60
X_train = []
Y_train = []
m = len(set_entrenamiento_escalado)

for i in range(time_step,m):
    # X: bloques de "time_step" datos: 0-time_step, 1-time_step+1, 2-time_step+2, etc
    X_train.append(set_entrenamiento_escalado[i-time_step:i,0])

    # Y: el siguiente dato
    Y_train.append(set_entrenamiento_escalado[i,0])
X_train, Y_train = np.array(X_train), np.array(Y_train)

# Reshape X_train para que se ajuste al modelo en Keras
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

#
# Red LSTM
#
dim_entrada = (X_train.shape[1],1)
dim_salida = 1
na = 50

modelo = Sequential()
modelo.add(LSTM(units=na, input_shape=dim_entrada))
modelo.add(Dense(units=dim_salida))
modelo.compile(optimizer='rmsprop', loss='mse')
modelo.fit(X_train,Y_train,epochs=20,batch_size=32)


#
# Validación (predicción del valor de las acciones)
#
set_validacion = dataset['2020':].iloc[:,1:4]
#set_validacion.values
x_test = set_validacion
x_test = sc.transform(x_test)

X_test = []
for i in range(time_step,len(x_test)):
    X_test.append(x_test[i-time_step:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))


print(X_test)
prediccion = modelo.predict(X_test)
#print(prediccion)

#----- soluc error
Predict_dataset = np.zeros(shape=(len(prediccion), 3) )
Predict_dataset[:,0] = prediccion[:,0]


prediccion = sc.inverse_transform(Predict_dataset)[:,0]
print('print prediccion')
print(prediccion)


# Graficar resultados


set_val =  set_validacion.to_numpy()
graficar_predicciones(set_val,prediccion)

#--- ultimo export xd

export(prediccion, set_validacion)