import yfinance as yf
import pandas as pd
import os
from append_or_create_csv import append_or_create_csv
import pytz
from datetime import datetime

def download_data_bulk(to_download):

    ##allticks = yf.Tickers('MSFT AAPL GOOG')
    ##msft = allticks.tickers['MSFT']
    ##msftinfo = msft.info

    alldata = yf.download(to_download, period='3mo', ## klo tanpa period downloadnya sepanjang masa
                        rounding = True)
    alldata = alldata.reset_index() ## buat tanggal jadi data, bukan index
    ##print(alldata)
    ##print(alldata[('Close', 'AAPL')]) ## akses kolom
    ##print(alldata['Date']) ## akses tanggal

    if not os.path.exists('data'):
        os.makedirs('data')

    ## making 'long string' format for Tickers
    ini_str = ''
    for stock in to_download:
        ini_str = ini_str+' '+stock
    ini_str = ini_str[1:]
    ##print(ini_str)

    ## saving long name to a csv
    allinfo = yf.Tickers(ini_str)
    for stock in to_download:
        pass

    #now saving data in pandas.
    for stock in to_download:
        ini_dict = {}
        ini_dict['Date'] = list(alldata['Date'])
        ini_dict['Open'] = list(alldata[('Open', stock)])
        ini_dict['High'] = list(alldata[('High', stock)])
        ini_dict['Low'] = list(alldata[('Low', stock)])
        ini_dict['Close'] = list(alldata[('Close', stock)])
        ini_dict['Volume'] = list(alldata[('Volume', stock)])
        ##print(ini_dict)

        ini_df = pd.DataFrame.from_dict(ini_dict)
        ##print(ini_df)

        ini_df.to_csv('data/'+stock+'.csv')
        ## NOTE: downloaded data still has index in it

        ini_info = allinfo.tickers[stock].info
        try:
            ini_nama = ini_info['longName']
        except:
            ini_nama = ini_info['shortName']

        # this part check the time
        timezone = pytz.timezone('Asia/Singapore')  # GMT+8
        local_time = datetime.now(timezone)
        local_str = local_time.strftime("%Y-%m-%d %H:%M:%S.%f%z")

        append_or_create_csv('data/tickername.csv', [stock, ini_nama, local_str],
                             ['Ticker', 'Name', 'Last_Update'])
