<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parameter untuk Training</title>
    <link href="bootstrap-5.1.3-dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body style="height: 100vh;">
    <script src="bootstrap-5.1.3-dist/js/bootstrap.min.js"></script>
    <div class="h-100 container">
        <div class="row bg-info text-white" style="height: 12%;">
            <p>"ini judul skripsi"</p>
        </div>
        <div class="row bg-dark align-items-center" style="height: 11%;">
            <div class="col align-middle">
                <a class="btn btn-outline-light border-dark" href="index.html">HOME</a>
                <a class="btn btn-outline-light border-dark" href="train.html">BACK</a>
            </div>
        </div>
        <form action="myenv\Scripts\ANN.py" method="post" target="_blank" class="h-100">
            <div class="h-100 row">
                <div class="col">
                    <div class="form-group row">
                    <?php
                        $layer=$_GET['layercount'];
                        for($x=0;$x<$layer;$x+=1){
                            echo '<div class="col-sm-2 col-form-label">';
                            echo 'Layer : ';
                            echo ($x+1);
                            echo '</div>';
                            ?>
                                <label for="neuron" class="col-sm-2 col-form-label">neuron:</label>
                                <div class="col-sm-3">
                                    <input type="text" name="neuron" id="neuron" class="form-control">
                                </div>
                                <label for="dropout" class="col-sm-2 col-form-label">dropout_rate:</label>
                                <div class="col-sm-3">
                                <input type="text" name="dropout" id="dropout" class="form-control">
                                </div>
                                <br>
                            <?php
                        }
                        // tambahkan fitur nilai default
                    ?>
                    </div>                    
                </div>
                <div class="col">
                    <div class="form-group row">
                        <label for="l_rate" class="col-sm-3 col-form-label">Learning Rate:</label>
                        <div class="col-sm-9">
                            <input type="text" name="l_rate" id="l_rate" value="0.20" class="form-control">
                        </div>
                        <label for="rh" class="col-sm-3 col-form-label">Rho:</label>
                        <div class="col-sm-9">
                            <input type="text" name="rh" id="rh" value="0.90" class="form-control">
                        </div>
                        <label for="moment" class="col-sm-3 col-form-label">Rho:</label>
                        <div class="col-sm-9">
                            <input type="text" name="moment" id="moment" value="0.00" class="form-control">
                        </div>
                        <label for="eps" class="col-sm-3 col-form-label">Rho:</label>
                        <div class="col-sm-9">
                            <input type="text" name="eps" id="eps" value="1e-05" class="form-control">
                        </div>
                        <label for="epoch" class="col-sm-3 col-form-label">Epoch:</label>
                        <div class="col-sm-9">
                            <input type="text" name="epoch" id="epoch" value="200" class="form-control">
                        </div>
                    </div>
                    <input type="hidden" name="layercount" value="<?php echo $layer?>">
                    <button type="submit" class="button">TRAIN ANN !</button>
                </div>
            </div>    
        </form>
        <div class="row bg-info text-white" style="height: 12%;">
            <P>"ini footer website"</P>
        </div>
    </div>
</body>
</html>