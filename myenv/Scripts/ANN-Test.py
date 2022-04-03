#!python.exe
#instalasi library
import sys, io, os
sys.stdout.buffer.write(b"Content-Type: text/html\n\n")
sys.stdout.buffer.write(b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../../bootstrap-5.1.3-dist/css/bootstrap.min.css">
    <title>Test Result</title>
</head>\n""")
sys.path.append("../Lib/site-packages")
sys.path.append("../../")
os.environ['HOMEPATH'] = '../../PictureTemp'
import matplotlib
import pandas as pd
from keras.models import load_model
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import mpu
import base64
# import tensorflow as tf
from ANN_MOD import root_mean_squared_error

#loading dataset forecast, model
X_input_Test=mpu.io.read('../../X_input_Test.pickle')
Y_input_Test=mpu.io.read('../../Y_input_Test.pickle')
X_input_Test=pd.DataFrame(X_input_Test)
# Y_input_Test=pd.DataFrame(Y_input_Test)
ANN_COVID19=load_model("../../COVID19-ANN(TA).h5",custom_objects={"root_mean_squared_error": root_mean_squared_error})


#evaluate the model
scores=ANN_COVID19.evaluate(
    x=X_input_Test, y=Y_input_Test, verbose=0
)

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

#make prediction
Y_Predict=ANN_COVID19(X_input_Test)

#plot between labels and prediction
testlen=len(Y_input_Test)

ImgFile=io.BytesIO()

# ax.plot(Y_Predict,label="Predict")
plt.plot(range(1,testlen+1),Y_input_Test,label="Actuals")
plt.plot(range(1,testlen+1),Y_Predict,label="Prediction")
# ax.xaxis.set_ticks_position('none')
# ax.yaxis.set_ticks_position('none')
# ax.spines["top"].set_alpha(0)
# ax.tick_params(labelsize=6)

plt.legend()
plt.tight_layout()
plt.savefig(ImgFile,format='png')
ImgFile.seek(0)

Img64=base64.b64encode(ImgFile.read()).decode("utf-8").replace("\n", "")
S="<img src=data:image/png;base64,"+Img64+">\n"
S=bytes(S, 'utf-8')

sys.stdout.buffer.write(b"""
<div class="row">
<div class="col">
""")

sys.stdout.buffer.write(S)

sys.stdout.buffer.write(b"""</div>
""")

#print the score
sys.stdout.buffer.write(b"""
<div class="col">
""")
S=str(scores)
S=bytes(S,'utf-8')
sys.stdout.buffer.write(S)

sys.stdout.buffer.write(b"""</div>
""")

ImgFile.close()

sys.stdout.buffer.write(b"""</div>
""")

sys.stdout.buffer.write(b"""<div class="row bg-info text-white" style="height: 12%;">
            <P>"ini footer website"</P>
        </div>""")

sys.stdout.buffer.write(b"""</div>
</body>""")

sys.stdout.buffer.write(b"</html>")