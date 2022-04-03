#!python.exe
import sys
sys.path.append("../Lib/site-packages")
sys.path.append("../../")
sys.stdout.buffer.write(b"Content-Type: text/html\n\n")
sys.stdout.buffer.write(b"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../../bootstrap-5.1.3-dist/css/bootstrap.min.css">
    <title>Feature Importance</title>
</head>""")
#first lines of code to prepare python script to web

#import library
import io
import cgitb
import os
import base64
cgitb.enable()
#set the 'HOMEPATH'
os.environ['HOMEPATH'] = '../../PictureTemp'

#import library
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpu
from ANN_MOD import root_mean_squared_error
from keras.models import load_model
import shap

def ABS_SHAP(df_shap,df):
    #ref: https://towardsdatascience.com/explain-your-model-with-the-shap-values-bc36aac4de3d
    ImgFile=io.BytesIO()
    #import matplotlib as plt
    # Make a copy of the input data
    shap_v = pd.DataFrame(df_shap)
    feature_list = df.columns
    shap_v.columns = feature_list
    df_v = df.copy().reset_index().drop('index',axis=1)
    
    # Determine the correlation in order to plot with different colors
    corr_list = list()
    for i in feature_list:
        b = np.corrcoef(shap_v[i],df_v[i])[1][0]
        corr_list.append(b)
    corr_df = pd.concat([pd.Series(feature_list),pd.Series(corr_list)],axis=1).fillna(0)
    # Make a data frame. Column 1 is the feature, and Column 2 is the correlation coefficient
    corr_df.columns  = ['Variable','Corr']
    corr_df['Sign'] = np.where(corr_df['Corr']>0,'red','blue')
    
    # Plot it
    shap_abs = np.abs(shap_v)
    k=pd.DataFrame(shap_abs.mean()).reset_index()
    k.columns = ['Variable','SHAP_abs']
    k2 = k.merge(corr_df,left_on = 'Variable',right_on='Variable',how='inner')
    k2 = k2.sort_values(by='SHAP_abs',ascending = True)
    colorlist = k2['Sign']
    ax = k2.plot.barh(x='Variable',y='SHAP_abs',color = colorlist,figsize=(9,6),legend=False)
    ax.set_xlabel("SHAP Value (Red = Positive Impact)")
    plt.tight_layout()
    plt.savefig(ImgFile,format='png')
    ImgFile.seek(0)
    Img64=base64.b64encode(ImgFile.read()).decode("utf-8").replace("\n", "")
    S="<img src=data:image/png;base64,"+Img64+">\n"
    S=bytes(S, 'utf-8')
    sys.stdout.buffer.write(S)
    ImgFile.close()


#load the model (original)
#load the dataset
X_input_Train=mpu.io.read('../../X_input.pickle')
X_input_names=X_input_Train.columns.values.tolist()

ANN_COVID19=load_model("../../COVID19-ANN(TA).h5",custom_objects={"root_mean_squared_error": root_mean_squared_error})
SC=mpu.io.read('../../SCALER.pickle')

# print(X_input_Train.head())

#transform the original data with 'SCALLER' to normalize/standardize

X_input_Train=SC.transform(X_input_Train)

shap.initjs()

#compute SHAP values
explainer = shap.DeepExplainer(ANN_COVID19, X_input_Train)
shap_values = explainer.shap_values(X_input_Train)

X_input_Train=SC.inverse_transform(X_input_Train)

X_input_Train=pd.DataFrame(X_input_Train,columns=X_input_names)

# print(X_input_Train.head())

#visualize SHAP GLOBAL
#visualize feature importance

sys.stdout.buffer.write(b"""<body style="height: 100vh;">
<script src="../../bootstrap-5.1.3-dist/js/bootstrap.min.js"></script>
<div class="h-100 container">
<div class="row bg-info text-white" style="height: 12%;">
    <p>"ini judul skripsi"</p>
</div>
<div class="row bg-dark align-items-center" style="height: 11%;">
    <div class="col align-middle">
        <a class="btn btn-outline-light border-dark" href="../../index.html">HOME</a>
    </div>
</div>""")
ImgFile=io.BytesIO()

fig=shap.summary_plot(shap_values[0], X_input_Train , feature_names = X_input_Train.columns,show=False)
plt.tight_layout()
plt.savefig(ImgFile,format='png')

ImgFile.seek(0)

sys.stdout.buffer.write(b"""<div class="row">""")

ABS_SHAP(shap_values[0],X_input_Train)

Img64=base64.b64encode(ImgFile.read()).decode("utf-8").replace("\n", "")
S="<img src=data:image/png;base64,"+Img64+">\n"
S=bytes(S, 'utf-8')
sys.stdout.buffer.write(S)

ImgFile.close()

sys.stdout.buffer.write(b"""</div>""")

sys.stdout.buffer.write(b"""<div class="row bg-info text-white" style="height: 12%;">
            <P>"ini footer website"</P>
        </div>""")

sys.stdout.buffer.write(b"""</div>""")

sys.stdout.buffer.write(b"</body>\n")

sys.stdout.buffer.write(b"</html>\n")