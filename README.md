# Twitch Channel Growth Predictor

## Description

This project uses machine learning to predict viewer growth for Twitch channels. It leverages the Twitch API to fetch historical data and applies an ARIMA (AutoRegressive Integrated Moving Average) model to forecast future viewer counts.
Features

* Secure handling of Twitch API credentials using environment variables
* Data fetching from the Twitch API for specified channels
* Data preprocessing and resampling for time series analysis
* ARIMA model implementation for viewer count prediction
* Visualization of historical data and forecasts

## Technologies Used

* Python
* Pandas for data manipulation
* NumPy for numerical operations
* Statsmodels for ARIMA modeling
* Matplotlib for data visualization
* Requests for API interactions
* python-dotenv for environment variable management
