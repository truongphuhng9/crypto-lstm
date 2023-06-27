# First we will import the necessary Library 
import pandas as pd
import numpy as np

# For Evalution we will use these library
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

# For PLotting we will use these library
import dash
from dash import dcc
from dash import html
from itertools import cycle
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Run a Dash app

app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.H1("Crypto Price Prediction", style={"textAlign": "center"}),
    html.H2("Please select a cryptocurrency", style={"textAlign": "center"}),
    html.Div([
        dcc.Dropdown(id='my-dropdown',
                        options=[{'label': 'BTC/USD', 'value': 'BTC-USD'},
                        {'label': 'ETH/USD', 'value': 'ETH-USD'},
                        {'label': 'ADA/USD', 'value': 'ADA-USD'}],
                        multi=False,value='BTC-USD',
                        style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "60%"}             
        )
    ]),
    dcc.Graph(id="btc-graph")
])

def load_data(crypto):
    data_file = "./data/{filename}.csv".format(filename=crypto)
    df = pd.read_csv(data_file)
    return df

def predict_data(crypto, closedf, time_step):
    scaler=MinMaxScaler(feature_range=(0,1))
    closedf=scaler.fit_transform(np.array(closedf).reshape(-1,1))
    X, y = create_dataset(closedf, time_step)
    X = X.reshape(X.shape[0],X.shape[1] , 1)

    # Model name: crypto like "BTC/USD" convert to "btc_usd"
    model_file = "./models/{filename}.h5".format(filename=crypto.lower().replace("-", "_") + "_model")
    model = load_model(model_file)

    predict = model.predict(X)
    predict_inv = scaler.inverse_transform(predict)
    return predict_inv



def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]   
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

@app.callback(Output("btc-graph", "figure"), [Input("my-dropdown", "value")])
def update_graph(selected_dropdown):
    trace1 = []
    trace2 = []

    # Load the data
    time_step = 15
    crypto = selected_dropdown
    df = load_data(crypto)
    df = df.dropna()

    closedf = df[['Date','Close']]
    del closedf['Date']

    prediction = predict_data(crypto, closedf, time_step)

    look_back=time_step

    # shift test predictions for plotting
    testPredictPlot = np.empty_like(closedf)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[(look_back):len(closedf)-1, :] = prediction

    trace1.append(go.Scatter(x=df.Date, y=df.Close, mode='lines', opacity=0.7, name="Actual Price",
                                textposition='bottom center'))

    trace2.append(go.Scatter(x=df.Date, y=testPredictPlot.reshape(1,-1)[0].tolist(), mode='lines', opacity=0.6, name="Predicted Price",
                                textposition='bottom center')) 

    traces = [trace1, trace2]

    data = [val for sublist in traces for val in sublist]

    figure = {'data': data,
                'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                                    height=600,
                                    title=f"Actual and Predicted Prices for {crypto} Over Time",
                                    xaxis={"title":"Date",
                                            'rangeselector': {'buttons': list([{'count': 1, 'label': '1M',
                                                                                'step': 'month',
                                                                                'stepmode': 'backward'},
                                                                                {'count': 6, 'label': '6M',
                                                                                'step': 'month',
                                                                                'stepmode': 'backward'},
                                                                                {'step': 'all'}])},
                                                                                'rangeslider': {'visible': True}, 'type': 'date'},
                                    yaxis={"title":"Price (USD)"})}
    return figure

    # Predict the price


if __name__=='__main__':
    app.run_server(debug=True, use_reloader=True)