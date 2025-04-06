import yfinance as yf
import pandas as pd
from append_or_create_csv import append_or_create_csv
import os
import pytz
from datetime import datetime

def download_data(to_download):

    ##allticks = yf.Tickers('MSFT AAPL GOOG')
    ##msft = allticks.tickers['MSFT']
    ##msftinfo = msft.info

    ini_info = yf.Ticker(to_download).info
    try:
        ini_nama = ini_info['longName']
    except:
        ini_nama = ini_info['shortName']

    alldata = yf.download(to_download, period='3mo', ## klo tanpa period downloadnya sepanjang masa
                        rounding = True)
    alldata = alldata.reset_index() ## buat tanggal jadi data, bukan index
    ##print(alldata)
    ##print(alldata[('Close', 'AAPL')]) ## akses kolom
    ##print(alldata['Date']) ## akses tanggal

    if not os.path.exists('data'):
        os.makedirs('data')

    #now saving data in pandas.
    ini_dict = {}
    ini_dict['Date'] = list(alldata['Date'])
    ini_dict['Open'] = list(alldata[('Open', to_download)])
    ini_dict['High'] = list(alldata[('High', to_download)])
    ini_dict['Low'] = list(alldata[('Low', to_download)])
    ini_dict['Close'] = list(alldata[('Close', to_download)])
    ini_dict['Volume'] = list(alldata[('Volume', to_download)])
    ##print(ini_dict)

    ini_df = pd.DataFrame.from_dict(ini_dict)
    ##print(ini_df)

    ini_df.to_csv('data/'+to_download+'.csv')
    ## NOTE: downloaded data still has index in it

    # this part check the time
    timezone = pytz.timezone('Asia/Singapore')  # GMT+8
    local_time = datetime.now(timezone)
    # for attempt in range(3):
    #     try:
    #         response = requests.get("http://worldtimeapi.org/api/timezone/Etc/GMT-8", timeout=5)
    #         if response.status_code == 200:
    #             data_time = response.json()
    #             local_time = data_time["datetime"]
    #     except requests.exceptions.RequestException as e:
    #         print(f"Attempt {attempt + 1} failed")
    #         time.sleep(3)  # Wait before retrying

    local_str = local_time.strftime("%Y-%m-%d %H:%M:%S.%f%z")

    # print(local_time)
    # print(local_str)
    # print(str2datetime(local_str))

    append_or_create_csv('data/tickername.csv', [to_download, ini_nama, local_str],
                                                ['Ticker', 'Name', 'Last_Update'])

    
