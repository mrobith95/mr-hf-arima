import plotly.graph_objects as go
import pandas as pd
import numpy as np
from find_missing_dates import find_missing_dates
from symbol2name import *
from statsmodels.iolib.smpickle import load_pickle
from datetime import datetime, timedelta

## make function for rounding, floor, and ceil
def rounding(a, decimals):
    return np.true_divide(np.rint(a * 10**decimals), 10**decimals)

def flooring(a, decimals):
    return np.true_divide(np.floor(a * 10**decimals), 10**decimals)

def ceiling(a, decimals):
    return np.true_divide(np.ceil(a * 10**decimals), 10**decimals)

def make_plot(stock, pi_1, pi_2):
    ## modify the input first
    ## stock input already good for this stuff
    pi_1str = str(pi_1)+"%"
    pi_2str = str(pi_2)+'%'
    pi_1 = (100-pi_1)/200.0 ## /200 karena /2 dlu lalu /100
    if pi_2 is not None:
        pi_2 = (100-pi_2)/200.0

    # print(pi_1str, pi_2str, pi_1, pi_2)

    ##stock = 'MSFT'
    ## import csv first
    datanya = pd.read_csv('data/'+stock+'.csv', parse_dates=['Date'])
    ##print(datanya)

    ## add decimals data
    if stock in ['NG=F', 'RB=F', 'XRP-USD']:
        blkg_koma = 4
    else:
        blkg_koma = 2

    ##dat = yf.Ticker(stock)
    ##bagian ini untuk print info sederhana
    ##for key, value in dat.info.items():
    ##    print(f'{key}: {value}')
    existing_symbol = load_symbol_data('data/tickername.csv')
    nama_stock = get_symbol_name(stock, existing_symbol)

    ## find missing dates
    missing_dates, ada_minggu = find_missing_dates(datanya)

    ## batas data untuk gambar
    maksimum = max(datanya['High'])
    atas_g = 2*maksimum
    bawa_g = 0

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
    lowerl = hasil_fore.conf_int(alpha = pi_1)[:,0] ## lower limit
    upperl = hasil_fore.conf_int(alpha = pi_1)[:,1] ## upper limit

    # (insample)
    hasil_insample = model.get_prediction()
    mean_insample = hasil_insample.predicted_mean ## mean
    lower_in = hasil_insample.conf_int(alpha = pi_1)[:,0] ## lower limit
    upper_in = hasil_insample.conf_int(alpha = pi_1)[:,1] ## upper limit

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

    ## add rounding
    pred = rounding(pred, blkg_koma)
    lowerl = ceiling(lowerl, blkg_koma)
    upperl = flooring(upperl, blkg_koma)

    # plot insample prediction
    fig.add_trace(
    go.Scatter(
        x=tanggalnya[(lower_in>bawa_g) & (upper_in<atas_g)],  # Your x-axis data
        y=mean_insample[(lower_in>bawa_g) & (upper_in<atas_g)],  # Your y-axis data
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
        x=tanggalnya[(lower_in>bawa_g) & (upper_in<atas_g)],
        y=lower_in[(lower_in>bawa_g) & (upper_in<atas_g)],
        mode='lines',
        name=pi_1str+' CI',
        showlegend=False, # remove from legend
        hoverinfo='skip',  # disables hover for this trace
        line=dict(color='gray', width=0.75),
        ))
    
    fig.add_trace(go.Scatter(
        x=tanggalnya[(lower_in>bawa_g) & (upper_in<atas_g)],
        y=upper_in[(lower_in>bawa_g) & (upper_in<atas_g)],
        mode='lines',
        name=pi_1str+' CI',
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
        name=pi_1str+' PI',
        showlegend=False, # remove from legend
        line=dict(color='gray', width=0.75),
        ))
    
    fig.add_trace(go.Scatter(
        x=next_tanggal, y=upperl,
        mode='lines',
        name=pi_1str+' PI',
        fill='tonexty',  # Fill to the trace below (y2)
        fillcolor='rgba(128, 128, 128, 0.15)',  # Grey with transparency
        line=dict(color='gray', width=0.75),
        ))


    ## now for second PI
    if pi_2 is not None:
        ## make lower and upper PI prediction
        lowerl2 = hasil_fore.conf_int(alpha = pi_2)[:,0] ## lower limit
        upperl2 = hasil_fore.conf_int(alpha = pi_2)[:,1] ## upper limit

        ## and Ci
        lower_in2 = hasil_insample.conf_int(alpha = pi_2)[:,0] ## lower limit
        upper_in2 = hasil_insample.conf_int(alpha = pi_2)[:,1] ## upper limit

        lowerl2 = ceiling(lowerl2, blkg_koma)
        upperl2 = flooring(upperl2, blkg_koma)

        # plot conf interval
        fig.add_trace(
            go.Scatter(
            x=tanggalnya[(lower_in2>bawa_g) & (upper_in2<atas_g)],
            y=lower_in2[(lower_in2>bawa_g) & (upper_in2<atas_g)],
            mode='lines',
            name=pi_2str+' CI',
            showlegend=False, # remove from legend
            hoverinfo='skip',  # disables hover for this trace
            line=dict(color='gray', width=0.75),
            ))
        
        fig.add_trace(go.Scatter(
            x=tanggalnya[(lower_in2>bawa_g) & (upper_in2<atas_g)],
            y=upper_in2[(lower_in2>bawa_g) & (upper_in2<atas_g)],
            mode='lines',
            name=pi_2str+' CI',
            fill='tonexty',  # Fill to the trace below (y2)
            fillcolor='rgba(128, 128, 128, 0.05)',  # Grey with transparency
            showlegend=False, # remove from legend
            hoverinfo='skip',  # disables hover for this trace
            line=dict(color='gray', width=0.75),
            ))

        # plot pred interval
        fig.add_trace(
            go.Scatter(
            x=next_tanggal, y=lowerl2,
            mode='lines',
            name=pi_2str+' PI',
            showlegend=False, # remove from legend
            line=dict(color='gray', width=0.75),
            ))
        
        fig.add_trace(go.Scatter(
            x=next_tanggal, y=upperl2,
            mode='lines',
            name=pi_2str+' PI',
            fill='tonexty',  # Fill to the trace below (y2)
            fillcolor='rgba(128, 128, 128, 0.05)',  # Grey with transparency
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

    # make a dict for table
    ini_pred = dict()
    ini_pred['Date'] = next_tanggal
    ini_pred['Prediction'] = pred
    if pi_2 is not None:
        ini_pred[pi_2str+' PI lower'] = lowerl2
    ini_pred[pi_1str+' PI lower'] = lowerl
    ini_pred[pi_1str+' PI upper'] = upperl
    if pi_2 is not None:
        ini_pred[pi_2str+' PI upper'] = upperl2

    ini_pred = pd.DataFrame(ini_pred) # change to pandas dataframe

    ##fig.show()
    return fig, ini_pred