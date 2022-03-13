import json
import simplejson
import pandas as pd
from flask import Flask, request, Response

from fbprophet import Prophet
from fbprophet.serialize import model_from_json

from google.cloud import storage

### Define environmental variables
PROJECT_ID = 'YOUR_PROJECT_NAME'
BUCKET_NAME = 'YOUR_BUCKET'
MODEL_PATH = 'YOUR_FOLDER/model/YOUR_MODEL.json'

### Get your model from the bucket
storage_client = storage.Client(project=PROJECT_ID)
BUCKET = storage_client.get_bucket(BUCKET_NAME)
blob = BUCKET.get_blob(MODEL_PATH)
model_data = json.loads(blob.download_as_string())
m = model_from_json(model_data)  

### Create Flask app
app = Flask(__name__)

# Health check
@app.route("/health")
def health():
    return "OK"

# Prediction
@app.route('/predict',methods=['GET','POST'])
def prediction():
    future = m.make_future_dataframe(periods=6, freq='M')
    forecast = m.predict(future)
    predictions = simplejson.dumps({"predictions": [{row['ds'].strftime("%Y-%m"): row['yhat']} for _, row in forecast.iterrows()]})
    
    return predictions

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)