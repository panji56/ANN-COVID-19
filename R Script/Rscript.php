<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../bootstrap-5.1.3-dist/css/bootstrap.min.css">
    <script src="../bootstrap-5.1.3-dist/js/bootstrap.bundle.min.js"></script>
    <title>ANN STOCK(JKSE)</title>
</head>
<body style="height: 100vh;">
    <div class="h-100 container">
        <div class="row bg-info text-white" style="height: 12%;">
            <p>"ini judul skripsi"</p>
        </div>
        <div class="row bg-dark align-items-center" style="height: 11%;">
            <div class="col align-middle">
                <a class="btn btn-outline-light border-dark" href="../index.html">HOME</a>
                <a class="btn btn-outline-light border-dark" href="../Upload.html">Upload File</a>
                <div class="btn-group">
                    <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Pelatihan Model
                      </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="../train.html">Melatih ANN</a></li>
                        <li><a class="dropdown-item" href="Rscript.php">Another action</a></li>
                    </ul>
                </div>
                <a class="btn btn-outline-light border-dark" href="../myenv/Scripts/feature_importance.py">Interpretasi Model ANN</a>
            </div>
        </div>
        <div class="h-100 row">
            <?php
                passthru("Rscript myScript.R")
            ?>
        </div>
        <div class="row bg-info text-white" style="height: 12%;">
            <P>"ini footer website"</P>
        </div>
    </div>
</body>
<!-- passthru("\"E:\Program and Files\R\R-4.0.2\bin\Rscript\" \"E:\xampp\htdocs\ANN COVID-19\R Script\myScript.R\"") -->
</html>