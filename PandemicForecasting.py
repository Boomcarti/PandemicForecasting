from flask import Flask, render_template_string
from matplotlib import pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import re
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)

def fetch_and_process_data():
    response = requests.get('https://www.worldometers.info/coronavirus/country/south-africa/')
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', class_='col-md-12')
    specific_divs_content = [div.prettify() for div in divs if div.find_all('h3', string="Daily New Cases in South Africa")]

    stored_json = json.dumps(specific_divs_content, indent=4)
    xaxis = re.findall(r'\"([a-zA-Z]{3}\s\d{1,2},\s\d{4}).{0,6}\"', stored_json)
    data_pattern = r"data:\s*(\[[^\]]*\])"
    matches = re.findall(data_pattern, stored_json, re.DOTALL)
    extracted_data_arrays = [json.loads(match) for match in matches]
    yaxis3 = [0 if x is None or isinstance(x, str) and x.lower() == 'null' else x for x in extracted_data_arrays[2]]
    min_length = min(len(xaxis), len(yaxis3))
    dates = pd.to_datetime(xaxis[:min_length])
    df = pd.DataFrame({'Date': dates, 'Daily Cases': yaxis3[:min_length]})
    df.set_index('Date', inplace=True)
    df['Daily Cases'] = df['Daily Cases'].ffill()
    df = df.asfreq('D')
    return df


df = fetch_and_process_data()

@app.route('/', methods=['GET'])
def get_forecast():
    model = ARIMA(df['Daily Cases'], order=(2, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.get_forecast(steps=7)
    forecast_df = forecast.summary_frame()
    
    
    # Writen the recommendation to a text file
    with open('forecast_improvement.txt', 'w') as f:
        f.write("Forecasted New Cases for the Next 7 Days:\n")
        f.write("\n\nTo improve the accuracy of the forecast, incorporating additional data such as weather patterns, "
                "mobility data, and government policies (like lockdowns or vaccination rates) could provide more context "
                "to the predictions. Enhancing the model by considering external regressors in a SARIMAX model or using "
                "machine learning approaches like LSTM could also be explored."
                '''Statistical Modeling with SARIMAX:
                Seasonal AutoRegressive Integrated Moving Average with eXogenous factors (SARIMAX) is a powerful statistical model that can handle both seasonal variations and external influences on the data. For forecasting COVID-19 cases, this model can utilize external regressors like local weather conditions (which can affect viral transmission) and mobility indices.
                For instance, implementing a SARIMAX model would involve defining the order of seasonal differencing (S), auto-regression (AR), and moving average (MA) components, along with integrating the impact of external regressors like policy changes or mobility trends.
                Machine Learning Approaches:

                Long Short-Term Memory (LSTM) Networks: These are a type of recurrent neural network (RNN) suitable for sequence prediction problems. LSTMs can effectively capture long-term dependencies and patterns in time-series data, making them ideal for predicting the spread of diseases over time.''')
            

    with open('forecasted_cases.csv', 'w') as file:

        file.write('date,new_cases\n')

        dates = forecast_df.index.format()
        predicted_cases = forecast_df['mean'].values
        
        # Write each row of data
        for date, cases in zip(dates, predicted_cases):
            file.write(f"{date},{cases}\n")
    
    
    # time series plot of the forecasted new cases
    plt.figure(figsize=(10, 5))
    plt.plot(pd.to_datetime(forecast_df.index), forecast_df['mean'], marker='o', linestyle='-')
    plt.title('Forecast of New COVID-19 Cases Over the Next 7 Days')
    plt.xlabel('Date')
    plt.ylabel('Forecasted New Cases')
    plt.grid(True)
    plt.savefig('forecasted_cases_plot.png')
    plt.close()    
        
    
    
    
    
    
    
    forecast_data = forecast_df[['mean']].reset_index()
    forecast_data.columns = ['date', 'predicted_cases']
    
    # Roundin the predicted cases to the nearest whole number
    forecast_data['predicted_cases'] = forecast_data['predicted_cases'].round().astype(int)
    
    # HTML template string for the table with Material Design Lite
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>COVID-19 Forecast</title>
        <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
        <script defer src="https://code.getmdl.io/1.3.0/material.min.js"></script>
        <style>
            table {
                width: 80%;
                margin: 50px auto;
                border-collapse: collapse;
            }
            th, td {
                padding: 12px 15px;
                text-align: left;
            }
            thead {
                background-color: #3f51b5;
                color: #ffffff;
            }
            tbody tr {
                border-bottom: 1px solid #dddddd;
            }
            tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }
            tbody tr:last-of-type {
                border-bottom: 2px solid #3f51b5;
            }
            h2 {
                text-align: center;
                margin-top: 50px;
                color: #3f51b5;
            }
        </style>
    </head>
    <body>
        <h2>COVID-19 Forecast for South Africa</h2>
        <p>Starting from the latest date available from <a>https://www.worldometers.info/coronavirus/country/south-africa/ </a> , for 7 days  </p>
        <table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp">
            <thead>
                <tr>
                    <th class="mdl-data-table__cell--non-numeric">Date</th>
                    <th>Predicted Cases</th>
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                <tr>
                    <td class="mdl-data-table__cell--non-numeric">{{ row['date'] }}</td>
                    <td>{{ row['predicted_cases'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    '''

    return render_template_string(html_template, data=forecast_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
