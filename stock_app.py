import dash
import pickle
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go

app = dash.Dash(__name__)

with open('model.h5', 'rb') as file:
    model = pickle.load(file)

app.layout = html.Div([
    html.H1("BTC/USDT Price Prediction"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    dcc.Dropdown(
        id='coin-selection',
        options=[
            {'label': 'BTC/USDT', 'value': 'btc'},
            # Add more coin options if needed
        ],
        value='btc',
        style={'width': '200px', 'margin': '10px'}
    ),
    html.Div(id='output-graph')
])


@app.callback(
    Output('output-graph', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    Input('coin-selection', 'value')
)
def update_graph(contents, filename, selected_coin):
    if contents is not None:
        # Read the uploaded file as a Pandas DataFrame
        df = pd.read_csv(contents)

        # Perform the necessary data processing and prediction using the DataFrame and selected coin
        # Replace this with your actual code to load the model, preprocess the data, and make predictions
        predictions = model.predict(df)

        # Create a scatter plot with the predicted data
        fig = go.Figure()
        # Add the predicted data to the scatter plot
        fig.add_trace(go.Scatter(
            x=df[],  # Replace with the x-axis values of the predicted data
            y=...,  # Replace with the y-axis values of the predicted data
            mode="lines",
            name="Predicted"
        ))
        # Set the layout of the plot
        fig.update_layout(
            title=f"{selected_coin.upper()}/USDT Price Prediction",
            xaxis_title="Time",
            yaxis_title="Price"
        )

        # Return the Plotly figure to update the graph on the webpage
        return dcc.Graph(figure=fig)

    # If no file is uploaded, display a message
    return 'Upload a file to see the predictions.'

if __name__ == '__main__':
    app.run_server(debug=True)