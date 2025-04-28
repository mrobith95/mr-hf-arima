import gradio as gr
from make_plot import make_plot
from data_update import data_update

def grafik_lilin(display_name, pi_1, pi_2):
    ## check validity of inputs
    if display_name is None or display_name == '---':
        raise gr.Error('Unrecognized input. Only choose 1 option on the dropdown.', duration=5)
    
    ## check for pi_1 value
    if pi_1 is None or pi_1 < 1 or pi_1 > 99:
        raise gr.Error('Use valid value for PI input (between 1 to 99).', duration=5)

    # check for pi_2
    if pi_2 == 0: # set to None if pi_2 is entered as 0
        pi_2 = None 
    if pi_2 is None:
        pass
    elif pi_2 < 1 or pi_2 > 99:
        raise gr.Error('Use valid value for optional PI input (between 1 to 99).', duration=5)

    ## switch between pi_1 and pi_2 if pi_2 < pi_1
    if pi_2 is not None and pi_2 < pi_1:
        pi_1, pi_2 = pi_2, pi_1

    ## if pi_1 and pi_2 is the same, set pi_2 to None
    if pi_2 is not None and pi_2 == pi_1:
        pi_2 = None

    # Convert display name to ticker symbol first
    stock = key2val_dropdown(display_name)
    data_update(stock)
    fig, ini_pred = make_plot(stock, pi_1, pi_2)
    return fig, ini_pred

## define function to map keys to values
def key2val_dropdown(chosen):
    ## dict content
    isi_dropdown = ['Apple Inc. (AAPL)',
                    'JPMorgan Chase & Co. (JPM)',
                    'Johnson & Johnson (JNJ)',
                    'Caterpillar Inc. (CAT)',
                    'Alphabet Inc. (GOOGL)',
                    'The Home Depot, Inc. (HD)',
                    'Gold (GC=F)',
                    'Crude Oil (CL=F)',
                    'Natural Gas (NG=F)',
                    'Gasoline (RB=F)',
                    'Bitcoin (BTC-USD)',
                    'Ethereum (ETH-USD)',
                    'Ripple (XRP-USD)',
                    'Binance Coin (BNB-USD)']
    isi_tick = ['AAPL',
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
    ini_dict = {isi_dropdown[i]: isi_tick[i] for i in range(len(isi_dropdown))}
    return ini_dict.get(chosen, '---')

with gr.Blocks() as demo:

    ##globals
    isi_dropdown = ['Apple Inc. (AAPL)',
                    'JPMorgan Chase & Co. (JPM)',
                    'Johnson & Johnson (JNJ)',
                    'Caterpillar Inc. (CAT)',
                    'Alphabet Inc. (GOOGL)',
                    'The Home Depot, Inc. (HD)',
                    'Gold (GC=F)',
                    'Crude Oil (CL=F)',
                    'Natural Gas (NG=F)',
                    'Gasoline (RB=F)',
                    'Bitcoin (BTC-USD)',
                    'Ethereum (ETH-USD)',
                    'Ripple (XRP-USD)',
                    'Binance Coin (BNB-USD)']

    gr.Markdown(
        """
        # mr-hf-arima
        Close price prediction on (some) financial data using ARIMA.

        __DISCLAIMER:__ Prediction given by this app is for informational purpose only, and should not be taken as financial advice.
        """
    )

    with gr.Row():
        symbol_choice = gr.Dropdown(isi_dropdown, label='Available Tickers', info="Choose 1 from the following list.")
        pi_1 = gr.Number(label="Prediction Interval (in %)", info="Enter value between 1 and 99 for Prediction Interval.",
                              value=95)
        pi_2 = gr.Number(label="more Prediction Interval (in %, optional)", info="Enter value between 1 and 99 for more Prediction Interval. 0 is treated as not using more PI.",
                         value = 0)

    submit_button = gr.Button("Submit", variant='primary')
    plot_result = gr.Plot(label='candlestick-chart', format='png')
    pred_dict = gr.Dataframe(label='prediction-table')
    gr.Markdown(
        """
        ## How it works
        1. Choose 1 of available tickers.
        2. Set at least 1 prediction interval.
        2. Click Submit
        3. Wait for the chart to appear (especially the first chart). 
        4. Move cursor to the right side of plot to get detailed info on predictions.
        
        Data is taken from yahoo finance. Note that the displayed data might be delayed.
        Also, we assume that latest candle is still forming.
        """
    )

    # # display chart only after submit button is clicked
    submit_button.click(fn=grafik_lilin,
                        inputs=[symbol_choice,pi_1,pi_2],
                        outputs=[plot_result, pred_dict])

demo.launch()
