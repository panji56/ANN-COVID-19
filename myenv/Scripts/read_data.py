#!python.exe
print("Content-Type: text/html")    # HTML is following
print()
#first 3 lines to load python via web server (using 'shebang')
# #import necessary library
import cgi, os, sys, io, cgitb
cgitb.enable()
sys.path.append("../Lib/site-packages")
#set HOMEPATH and append Folder Access
sys.path.append("../../")
os.environ['HOMEPATH'] = '../../PictureTemp'
#for web python debungging purpose
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import mpu
#load the data from the request
form=cgi.FieldStorage()

#select the row based on country
COUNTRY=['Indonesia']

#load data from IHME then append
IHME_2020= form["IHME2020"].file.read()
IHME_2020 = pd.read_csv(io.BytesIO(IHME_2020),parse_dates=['date'],na_values='') 
IHME_2021= form["IHME2021"].file.read()
IHME_2021 = pd.read_csv(io.BytesIO(IHME_2021),parse_dates=['date'],na_values='')
IHME_2022 = form["IHME2022"].file.read()
IHME_2022 = pd.read_csv(io.BytesIO(IHME_2022),parse_dates=['date'],na_values='')

#select row for IHME and append
IHME_data=IHME_2020.append(IHME_2021,ignore_index=True)
IHME_data=IHME_data.append(IHME_2022,ignore_index=True)
IHME_data=IHME_data[IHME_data['location_name'].isin(COUNTRY)]

IHME_data.to_csv('../../ALL_IHME.csv',index=False,encoding='UTF-8')

# load data from OWID
OWID_data=form["OWID"].file.read()
OWID_data = pd.read_csv(io.BytesIO(OWID_data),parse_dates=['date'],na_values='')

#select the row based on country
COUNTRY=['Indonesia']

#select row for OWID
OWID_data=OWID_data[OWID_data['location'].isin(COUNTRY)]

OWID_data.to_csv('../../ALL_OWID.csv',index=False,encoding='UTF-8')

#load the IHSG stock prices
STOCK_data=form["STOCK"].file.read()
STOCK_data = pd.read_csv(io.BytesIO(STOCK_data),parse_dates=['Date'],na_values='')

#create validation here
# print(IHME_2020.head())
# print(IHME_2021.head())
# print(OWID_data.head())
# print(STOCK_data.head())

#un-capitalize the column name

#perform first join of STOCK and IHME data based on 'date'
ALL_DATA=STOCK_data.join(IHME_data.set_index('date'),on='Date')

ALL_DATA.to_csv('../../FIRST_JOIN.csv',index=False,encoding='UTF-8')

#perform second join
OWID_data=OWID_data[OWID_data.columns.difference(['population'])]
ALL_DATA=ALL_DATA.join(OWID_data.set_index('date'),on='Date')

ALL_DATA.to_csv('../../SECOND_JOIN.csv',index=False,encoding='UTF-8')

#select the column
selection=[
'Date',
'Close',
#----confirmed casses
'new_cases',
#----confirmed deaths
'new_deaths',
'pneumonia_mean',#radang paru-paru, COVID-19 menyerang paru - paru. ratio kematian pneumonia dalam satu minggu terhadap kematian pneumonia/tahun pada lokasi tersebut
#----reproduction rate
'reproduction_rate',#Rt tingkat penularan COVID-19 setelah adanya intervensi (1 orang dapat nular berapa orang)
#----Tests
'new_tests',#test harian baru
'positive_rate',#jumlah test COVID-19 yang positif
'tests_per_case',#jumlah test yang dijalankan setiap ada kasus baru positif (harian)
#----Policy
'stringency_index',#pembatasan kegiatan
'mask_use_mean',#penggunaan masker ketika meninggalkan rumah
#----Mobility	
'mobility_mean',#tingkat mobilitas
#----vaccinations
'total_boosters',#dosis vaksin, bukan orang, jumlah dosis vaksin (botol) booster
'total_vaccinations',#jumlah total dosis vaksin (termasuk booster)
'new_vaccinations',#jumlah harian dosis vaksin yang dipakai (7 hari)
'cumulative_all_vaccinated',#orang 1 dari 2 dosis	
'cumulative_all_fully_vaccinated',#orang 1 dari 1 dan 2 dari 2 dosis
'cumulative_all_effectively_vaccinated',#orang 2 dari 2 dosis
#----infections rate
'infection_fatality',# IFR
'infection_detection',# IDR
'infection_hospitalization'# IHR
]
data_input=ALL_DATA[selection]

#remove the 'NaN' with zero
data_input=data_input.replace(np.nan,0)
data_input=data_input.replace('inf',0)
data_input=data_input.replace('Inf',0)
data_input=data_input.replace([np.inf, -np.inf],0)

#save the final data in csv
data_input.to_csv('../../ALL_FINAL.csv',index=False,encoding='UTF-8')

#divide between X (Attributes), Y (target) and Date input
X_input = data_input.loc[:,~data_input.columns.isin(['Close','Date'])]

Y_input = data_input['Close']

date_input = data_input['Date']

#splitting data (train and test) 80:20

X_input_Train,X_input_Test,Y_input_Train,Y_input_Test=train_test_split(X_input,Y_input,test_size=0.2)

#perform standarization/normalization
from sklearn.preprocessing import StandardScaler
sc = StandardScaler(with_mean=True,with_std=True)
X_input_Train=sc.fit_transform(X_input_Train)
X_input_Test=sc.transform(X_input_Test)

#write to file
mpu.io.write('../../X_input.pickle',X_input)
mpu.io.write('../../X_input_Train.pickle',X_input_Train)
mpu.io.write('../../Y_input_Train.pickle',Y_input_Train)
mpu.io.write('../../date_input.pickle',date_input)

mpu.io.write('../../Y_input.pickle',Y_input)
mpu.io.write('../../X_input_Test.pickle',X_input_Test)
mpu.io.write('../../Y_input_Test.pickle',Y_input_Test)
mpu.io.write('../../SCALER.pickle',sc)

print("Finish upload data to server!<br>")