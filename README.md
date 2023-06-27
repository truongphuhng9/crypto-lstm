# PREDICT CRYPTO PRICES USING LSTM

## Introduction
This is an small project for beginner into machine learning. The project using: 
  - Historical data of crypto trading, was collected from [Yahoo finance](https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD)
  - Long short-term memory for predict the time-series data of 3 crypto currencies BTC, ETH and ADA
  - Data visualizationon web browser by [Plotly](https://plotly.com/) and [Dash](https://plotly.com/dash/).

## Folder struct
1. `data`: contains all the trainning data
2. `models`: contains all the models after trainning
3. `tranings`: contains notebooks using for trainning and visualization data
4. `crypto_prediction_app.py`: a application run the Dash web server and prepare the predict data of 3 upper models.
## How to run?
### Trainning
Go into notebook and run it!
### Dashboard
run `python crypto_prediction_app.py` or `python3 crypto_prediction_app.py`
