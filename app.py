from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import json

app = Flask(__name__)

# Load your time series data here
# For this example, we'll generate random data
def generate_sample_data(n_samples=1000):
    timestamps = pd.date_range(start='2023-01-01', periods=n_samples, freq='H')
    values = np.random.randn(n_samples).cumsum() + 100
    df = pd.DataFrame({'timestamp': timestamps, 'value': values})
    return df

# Initialize the model
def initialize_model():
    model = IsolationForest(contamination=0.05, random_state=42)
    return model

# Global variables
data = generate_sample_data()
model = initialize_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_anomalies', methods=['POST'])
def detect_anomalies():
    # Get the data from the request
    input_data = request.json['data']
    
    # Convert input data to DataFrame
    df = pd.DataFrame(input_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    
    # Fit the model and predict anomalies
    model.fit(df[['value']])
    anomalies = model.predict(df[['value']])
    
    # Create a result DataFrame
    result = df.copy()
    result['anomaly'] = anomalies
    
    # Convert result to JSON
    result_json = result.reset_index().to_json(orient='records', date_format='iso')
    
    return jsonify(json.loads(result_json))

if __name__ == '__main__':
    app.run(debug=True)
