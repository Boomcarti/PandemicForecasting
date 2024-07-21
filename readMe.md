# COVID-19 Case Forecasting Application

## Overview
This Flask-based application fetches daily new COVID-19 cases data from Worldometer for South Africa, forecasts future cases using the ARIMA model, and presents the results through a simple web interface.

## Features
- **Data Ingestion:** Scrapes COVID-19 case data from Worldometers.
- **Data Processing:** Parses and processes the HTML content to extract daily case numbers.
- **Forecasting:** Uses an ARIMA(2, 1, 1) model to forecast the next 7 days of new COVID-19 cases.
- **Reporting:** Outputs forecast data to a CSV file and a plot image.
- **Web Interface:** Displays the forecast in a simple HTML table using Material Design Lite.

## Prerequisites
- Python 3.8+
- Libraries: Flask, pandas, matplotlib, BeautifulSoup4, requests, statsmodels

## Installation

1. **Clone the repository:**
   git clone [repository-url]
   cd [repository-directory]

2. **Install required Python packages:**
    pip install Flask pandas matplotlib beautifulsoup4 requests statsmodels


## Running the Application

1. **Start the Flask server:**
    python PandemicForecasting.py

1. **Access the application:**
    Open a web browser and navigate to http://127.0.0.1:5000/


## Files
PandemicForecasting.py: The main Python script with Flask app and ARIMA modeling.
forecasted_cases.csv: CSV file containing the forecasted new cases.
forecasted_cases_plot.png: A plot visualizing the forecast of new cases.
forecast_improvement.txt: Recommendations for future model improvements.

## Model Explanation
The ARIMA model parameters (p=2, d=1, q=1) were selected based on research into similar epidemiological data modeling. These parameters provide a balance between model complexity and forecasting accuracy for short-term predictions.


For the ARIMA model parameters (p=2, d=1, q=1) used in epidemiological data modeling, the selection is grounded in analytical practices aimed at achieving optimal forecasting balance. Here’s how these parameters are typically justified:

p=2 (Auto-Regressive term): This setting allows the model to account for the influence of the previous two data points. It's chosen based on the autocorrelation function (ACF) and partial autocorrelation function (PACF) which might show significant lag at the first and possibly at the second lag, suggesting that these past values hold predictive power for the future values​ ([Just into Data](https://www.justintodata.com/arima-models-in-python-time-series-prediction/))​​ ([Data Magic AI Blog](https://datamagiclab.com/demystifying-arima-model-parameters-a-step-by-step-guide/))​.

d=1 (Differencing order): A single differencing (d=1) is generally sufficient for removing any linear trend in the series, thus making the data stationary. This is crucial as non-stationarity can obscure the true relationship between time steps and can lead to misleading models​ ([PhDinds AIM](https://phdinds-aim.github.io/time_series_handbook/01_AutoRegressiveIntegratedMovingAverage/01_AutoRegressiveIntegratedMovingAverage.html))​​ ([QuantStart](https://www.quantstart.com/articles/Autoregressive-Integrated-Moving-Average-ARIMA-p-d-q-Models-for-Time-Series-Analysis/))​.

q=1 (Moving Average term): The choice of q=1 is often based on the smoothing that this parameter can provide to the model, helping to account for other noise in the data series. This is typically indicated by a significant spike at lag one in the ACF, suggesting that the model should incorporate one moving average term to capture the lingering effects of past shocks or innovations​ 

These parameters are chosen to balance model simplicity (to avoid overfitting) and the need to capture enough of the data's dynamics to make accurate predictions. Tools like the AIC and BIC are often used to compare the goodness of fit for models with different parameters, ensuring that the selected model offers a reasonable trade-off between complexity and fit​ 

For further details on ARIMA models and their application in time series analysis, the resources provided on sites like QuantStart and Just Into Data offer comprehensive guides​ 

## Future Improvements
Enhanced Data Sources: Incorporating additional data such as mobility patterns and government policy changes could improve the model’s accuracy.
Model Refinement: Regular reevaluation of the model parameters based on updated data and advanced machine learning techniques could enhance forecast precision.

## Troubleshooting
Common issues: If you encounter any issues with missing data or errors in forecasts, please ensure that the web structure of the data source has not changed.
Support: For additional help, submit an issue on the repository or contact 