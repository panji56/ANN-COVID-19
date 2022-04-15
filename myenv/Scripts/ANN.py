#!python.exe
import cgi, os, sys, io, cgitb, base64
sys.stdout.buffer.write(b"Content-Type: text/html\n\n")
sys.stdout.buffer.write(b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>\n""")
sys.path.append("../Lib/site-packages")
sys.path.append("../../")
os.environ['HOMEPATH'] = '../../PictureTemp'
cgitb.enable()
#first lines of code to prepare python script to be load on web
#library import
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import mpu
from ANN_MOD import model_create

#get data from POST request
form = cgi.FieldStorage()

activation = form.getvalue('activation')
neuron = form.getvalue('neuron')
dropout = form.getvalue('dropout')
layercount = form.getvalue('layercount')
epoch = form.getvalue('epoch')
l_rate = form.getvalue('l_rate')
rh = form.getvalue('rh')
moment = form.getvalue('moment')
eps = form.getvalue('eps')

#check if more than one item, if it is convert to list
if not (isinstance(neuron, list)):
    neuron=[neuron]
if not (isinstance(dropout, list)):
    dropout=[dropout]
if not (isinstance(activation, list)):
    activation=[activation]

#loading dataset
X_input_Train=mpu.io.read('../../X_input_Train.pickle')
Y_input_Train=mpu.io.read('../../Y_input_Train.pickle')
X_input_Train=pd.DataFrame(X_input_Train)
Y_input_Train=pd.DataFrame(Y_input_Train)

#Initialising ANN and CALLBACK
ck = tf.keras.callbacks.ModelCheckpoint("../../COVID19-ANN(SA).h5", save_best_only=False)

#define model by calling function model_create() from ANN_MOD module,
#then fit it with training data

ANN_COVID19=model_create(layercount,neuron,dropout,activation,l_rate,rh,moment,eps)

#fit the ANN
History=ANN_COVID19.fit(X_input_Train,Y_input_Train,epochs = int(epoch),callbacks=[ck],validation_split=0.20,verbose=0,shuffle=True)


#visualise the loss

sys.stdout.buffer.write(b"<body>\n")

ANN_History=pd.DataFrame(History.history)
ANN_History['epochs']=History.epoch


epochs=ANN_History.shape[0]

plt.plot(np.arange(0,epochs),ANN_History['loss'],label="training RMSE")
plt.plot(np.arange(0,epochs),ANN_History['val_loss'],label="validation RMSE")
plt.legend()

plt.tight_layout()

ImgFile=io.BytesIO()

plt.savefig(ImgFile,format='png')

ImgFile.seek(0)

Img64=base64.b64encode(ImgFile.read()).decode("utf-8").replace("\n", "")
S="<img src=data:image/png;base64,"+Img64+">\n"
S=bytes(S, 'utf-8')
sys.stdout.buffer.write(S)

ImgFile.close()

#print the score
S="<br> RMSE Train : "+str(ANN_History.loc[epochs-1,'loss'])+" RMSE Valid : "+str(ANN_History.loc[epochs-1,'val_loss'])+"<br>"
S=bytes(S,'utf-8')
sys.stdout.buffer.write(S)

sys.stdout.buffer.write(b"</body>\n")

sys.stdout.buffer.write(b"</html>")