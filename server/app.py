import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

app = Flask(__name__)
api = Api(app)

CORS(app)
ALLOWED_EXTENSIONS = {'csv'}

@api.route('/predict_sales', methods=["POST"])
class PredictSales(Resource):
    def post(self):
        file = request.files['file']
        
        # Read the CSV file
        df = pd.read_csv(file, parse_dates=['Date'], index_col='Date')
        
        # Preprocess the data
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df.values.reshape(-1, 1))
        
        # Define the input parameters for the LSTM model
        n_input = 12
        n_features = 1
        
        # Generate time series sequences for the data
        generator = TimeseriesGenerator(scaled_data, scaled_data, length=n_input, batch_size=1)
        
        # Create and train the LSTM model
        model = Sequential()
        model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(generator, epochs=50)
        
        # Perform the forecast for the desired period
        time_period = int(request.form['timePeriod'])
        forecast_generator = TimeseriesGenerator(scaled_data, scaled_data, length=n_input, batch_size=1)
        forecast = model.predict(forecast_generator)
        forecast = forecast.flatten()[-time_period:]
        forecast = scaler.inverse_transform(forecast.reshape(-1, 1)).flatten()
        
        # Plot the forecast
        fig, ax = plt.subplots(figsize=(12, 6))  # Increase the figure size
        
        forecast_dates = pd.date_range(start=df.index[-1], periods=time_period, freq='M')
        
        # Adjust the range of x-axis and convert to months
        start_date = pd.to_datetime('1974-01-01')
        end_date = forecast_dates[-1]
        x_ticks = pd.date_range(start=start_date, end=end_date, freq='M')
        x_tick_labels = [date.strftime('%b %Y') for date in x_ticks]

        # Truncate the actual data to start from 1974
        actual_data = df.loc[df.index >= start_date]
        ax.plot(actual_data.index, actual_data.values, label='Actual')

        # Adjust the forecast data to align with the truncated actual data
        forecast_data = pd.Series(forecast, index=forecast_dates)
        forecast_data = forecast_data.loc[forecast_data.index >= start_date]

        # Extend the forecast data to include the last actual value
        last_actual_date = actual_data.index[-1]
        last_actual_value = actual_data.values[-1]
        forecast_data = pd.concat([pd.Series(last_actual_value, index=[last_actual_date]), forecast_data])

        ax.plot(forecast_data.index, forecast_data.values, label='Forecast')

        ax.set_xlabel('Date')
        ax.set_ylabel('Sales')
        ax.set_title('Sales Forecast')
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_tick_labels, rotation='vertical')
        ax.legend()
        plt.tight_layout()  # Adjust spacing to avoid overlapping labels
        plt.show()

        # Calculate accuracy
        train_predictions = model.predict(generator)
        train_predictions = scaler.inverse_transform(train_predictions).flatten()
        train_actual = scaled_data[n_input:].flatten()
        accuracy = 1 - mean_squared_error(train_actual, train_predictions) / np.var(train_actual)
        print("Model Accuracy:", accuracy)
        
        return jsonify({"success": True, "accuracy": accuracy})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":  
    app.run(debug=True, port=5000)