import plotly.graph_objects as go
import pandas as pd
# import numpy as np
from find_missing_dates import find_missing_dates
from symbol2name import *
from statsmodels.iolib.smpickle import load_pickle
from datetime import datetime, timedelta

def make_plot(stock):
    ##stock = 'MSFT'
    ## import csv first
    datanya = pd.read_csv('data/'+stock+'.csv', parse_dates=['Date'])
    ##print(datanya)

    ##dat = yf.Ticker(stock)
    ##bagian ini untuk print info sederhana
    ##for key, value in dat.info.items():
    ##    print(f'{key}: {value}')
    existing_symbol = load_symbol_data('data/tickername.csv')
    nama_stock = get_symbol_name(stock, existing_symbol)

    ## find missing dates
    missing_dates, ada_minggu = find_missing_dates(datanya)

    ## define fig
    fig = go.Figure(data=[go.Candlestick(x=datanya['Date'],
                    open = datanya['Open'],
                    high = datanya['High'],
                    low = datanya['Low'],
                    close = datanya['Close'],
                    name=stock)])
    ## [:-1] should be limit candles on "finished candle only"/"1 day delayed data" chart

    ## NOTE: Load model, drop nans, and Playground here!
    ## load model
    model = load_pickle('arimas/'+stock+'.pkl')

    ## drop nans on data
    data_dense = datanya.dropna() ## drop na(s)

    ## make insample and outsample prediction
    close_np  = data_dense['Close'].to_numpy()
    tanggalnya = data_dense['Date'].iloc[:-1]

    # ## predict (outsample)
    model = model.apply(close_np[:-1]) ## we assume that latest candle still forming
    hasil_fore = model.get_forecast(steps = 5)
    pred = hasil_fore.predicted_mean ## mean
    lowerl = hasil_fore.conf_int(alpha = 0.05)[:,0] ## lower limit
    upperl = hasil_fore.conf_int(alpha = 0.05)[:,1] ## upper limit

    # (insample)
    hasil_insample = model.get_prediction()
    mean_insample = hasil_insample.predicted_mean ## mean
    lower_in = hasil_insample.conf_int(alpha = 0.05)[:,0] ## lower limit
    upper_in = hasil_insample.conf_int(alpha = 0.05)[:,1] ## upper limit

    ## menghitung tanggal untuk prediksi
    ini_tanggal = tanggalnya.to_list() ## ambil data tanggal
    next_tanggal = [] ## list kosong untuk output
    late_tanggal = max(ini_tanggal)
    # print(late_tanggal)
    cek_tanggal = late_tanggal
    while len(next_tanggal) < 5:
        cek_tanggal = cek_tanggal + timedelta(days=1)
        if cek_tanggal.weekday() < 5 or ada_minggu:
            next_tanggal.append(cek_tanggal)

    # plot insample prediction
    fig.add_trace(
    go.Scatter(
        x=tanggalnya[lower_in>0],  # Your x-axis data
        y=mean_insample[lower_in>0],  # Your y-axis data
        mode='lines',      # 'lines', 'markers', or 'lines+markers'
        name=f'Prediction',  # Legend entry
        showlegend=False, # remove from legend
        hoverinfo='skip',  # disables hover for this trace
        line=dict(color='blue', width=1.5)  # Customize line appearance
    ))

    # plot outsample
    fig.add_trace(
    go.Scatter(
        x=next_tanggal,  # Your x-axis data
        y=pred,  # Your y-axis data
        mode='lines',      # 'lines', 'markers', or 'lines+markers'
        name=f'Prediction',  # Legend entry
        line=dict(color='blue', width=1.5)  # Customize line appearance
    ))

    # plot conf interval
    fig.add_trace(
        go.Scatter(
        x=tanggalnya[lower_in>0], y=lower_in[lower_in>0],
        mode='lines',
        name='Insample lower',
        showlegend=False, # remove from legend
        hoverinfo='skip',  # disables hover for this trace
        line=dict(color='gray', width=0.75),
        ))
    
    fig.add_trace(go.Scatter(
        x=tanggalnya[lower_in>0], y=upper_in[lower_in>0],
        mode='lines',
        name='Insample upper',
        fill='tonexty',  # Fill to the trace below (y2)
        fillcolor='rgba(128, 128, 128, 0.15)',  # Grey with transparency
        showlegend=False, # remove from legend
        hoverinfo='skip',  # disables hover for this trace
        line=dict(color='gray', width=0.75),
        ))

    # plot pred interval
    fig.add_trace(
        go.Scatter(
        x=next_tanggal, y=lowerl,
        mode='lines',
        name='prediction lower',
        showlegend=False, # remove from legend
        line=dict(color='gray', width=0.75),
        ))
    
    fig.add_trace(go.Scatter(
        x=next_tanggal, y=upperl,
        mode='lines',
        name='prediction upper',
        fill='tonexty',  # Fill to the trace below (y2)
        fillcolor='rgba(128, 128, 128, 0.15)',  # Grey with transparency
        showlegend=False, # remove from legend
        line=dict(color='gray', width=0.75),
        ))


    fig.update_layout(xaxis_rangeslider_visible=False,
                      title = nama_stock+' ('+stock+')',
                      showlegend = True,
                      xaxis=dict(
                            rangebreaks=[dict(values=missing_dates)]  # Hide weekends
                                ),
                      legend=dict(
                      orientation="h",  # horizontal orientation
                      yanchor="top",
                      y=-0.2,          # position below the plot
                      xanchor="center",
                      x=0.5            # centered horizontally
                          )
                     )
    ##fig.show()
    return fig