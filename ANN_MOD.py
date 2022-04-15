#instalasi library
import pandas as pd
import tensorflow as tf
import numpy as np
from keras import backend as K

#function to create the ANN model

#define RMSE loss function
def root_mean_squared_error(y_true,y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))

#define Error loss function
def func_error(y_true,y_pred):
    return (y_pred - y_true)

#define model
def model_create(layercount,neuron,dropout,activation,l_rate,rh,moment,eps):

    #create the model
    model = tf.keras.Sequential()

    for x in range(int(layercount)):

        #create the dropout
        model.add(tf.keras.layers.Dropout(rate=float(dropout[x])))

        #create First hidden layer
        model.add(tf.keras.layers.Dense(int(neuron[x]), activation=str(activation[x])))

    #create output layer
    model.add(tf.keras.layers.Dense(1, activation='linear'))

    # define the optimizer
    Optimizer=tf.keras.optimizers.RMSprop(
        learning_rate=float(l_rate), 
        rho=float(rh), 
        momentum=float(moment), 
        epsilon=float(eps), 
        centered=False,
        name='RMSprop')

    # Optimizer=tf.keras.optimizers.Adadelta(
    #     learning_rate=float(l_rate), 
    #     rho=float(rh), 
    #     epsilon=float(eps), 
    #     name='Adadelta')

    # Optimizer=tf.keras.optimizers.Nadam(
    #     learning_rate=float(l_rate), 
    #     beta_1=0.9,
    #     beta_2=0.999, 
    #     epsilon=float(eps), 
    #     name='Nadam')

    #compiling ANN
    model.compile(optimizer=Optimizer,loss=root_mean_squared_error,metrics=['mae','mape'])

    return model
