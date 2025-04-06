# from download_data import download_data
from download_data_bulk import download_data_bulk
# from make_plot import make_plot
# from data_update import data_update
import yfinance as yf
from train_new_model import *
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.iolib.smpickle import load_pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

to_download =  ['AAPL',
                'JPM',
                'JNJ',
                'CAT',
                'GOOGL',
                'HD',
                'GC=F',
                'CL=F',
                'NG=F',
                'RB=F',
                'BTC-USD',
                'ETH-USD',
                'XRP-USD',
                'BNB-USD']
download_data_bulk(to_download)

# # considered = 'data/'+to_download[0]+'.csv'
# model = train_model(to_download[0])
# print(model.summary())
train_model_bulk(to_download)

## test arima models
# random_numbers = np.random.normal(0, 1, 60)
# seq = []
# nilai = 0
# for val in random_numbers:
#     nilai += val
#     seq.append(nilai)

# # print(seq)
# mod = ARIMA(seq, order=(0, 2, 0), trend='t')
# res = mod.fit()
# print(res.summary())

## look at model
# model = load_pickle('arimas/'+to_download[0]+'.pkl')
# print(model.summary())
## ALTERNATIVE: use model from model_list
## model = model_list[k] ##[TEST]

# ## pick data
# datanya = pd.read_csv('data/'+to_download[6]+'.csv', parse_dates=['Date'])
# datanya.dropna(inplace=True) ## drop na(s)

# close_np  = datanya['Close'].to_numpy()
# tanggalnya = datanya['Date'].iloc[:-1]

# print(tanggalnya)

# # ## predict (outsample)
# model = model.apply(close_np[:-1]) ## we assume that latest candle still forming
# hasil_fore = model.get_forecast(steps = 5)
# pred = hasil_fore.predicted_mean ## mean
# lowerl = hasil_fore.conf_int(alpha = 0.05)[:,0] ## lower limit
# upperl = hasil_fore.conf_int(alpha = 0.05)[:,1] ## upper limit

# # (insample)
# hasil_insample = model.get_prediction()
# mean_insample = hasil_insample.predicted_mean ## mean
# lower_in = hasil_insample.conf_int(alpha = 0.05)[:,0] ## lower limit
# upper_in = hasil_insample.conf_int(alpha = 0.05)[:,1] ## upper limit

# # ## menghitung tanggal berikutnya
# # ini_tanggal = datanya['Date'].to_list() ## ambil data tanggal
# # next_tanggal = [] ## list kosong untuk output
# # late_tanggal = max(ini_tanggal)
# # print(late_tanggal)
# # cek_tanggal = late_tanggal
# # while len(next_tanggal) < 5:
# #     cek_tanggal = cek_tanggal + timedelta(days=1)
# #     if cek_tanggal.weekday() < 5:
# #         next_tanggal.append(cek_tanggal)

# # # print(next_tanggal)
# # # print(type(mean_insample))
# print(mean_insample)
# print(mean_insample[mean_insample!=0])
# print(tanggalnya[mean_insample!=0])