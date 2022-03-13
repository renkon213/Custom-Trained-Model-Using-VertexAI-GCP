import pandas as pd
import matplotlib.pyplot as plt
import json

from fbprophet import Prophet
from fbprophet.serialize import model_to_json, model_from_json

from google.cloud import bigquery, storage

### Define environmental variables
PROJECT_ID = 'YOUR_PROJECT_NAME'
TABLE_PATH = 'YOUR_DATASET.TABLE_NAME'
BUCKET_NAME = 'YOUR_BUCKET'
MODEL_PATH = 'YOUR_FOLDER/model/' # You need the model folder for Vertex AI to tell where your model is.

### BigQuery client
client = bigquery.Client(project=PROJECT_ID)

### Extract data
sql = f"""
SELECT * FROM `{TABLE_PATH}`
"""

df = client.query(sql).to_dataframe()

### Data processing
df = df.rename(columns={'monthly_sep': 'ds', 'sales': 'y'})
df.drop(55, inplace=True)
df['y'] = df['y'].apply(lambda x: round(x, 2))

### Modeling
m = Prophet()
m.fit(df)

### Save the model
# Cloud Storage client
storage_client = storage.Client(project=PROJECT_ID)

# write your bucket name
BUCKET = storage_client.get_bucket(BUCKET_NAME)

# create a blob
blob = BUCKET.blob(MODEL_PATH + 'prophet_model.json')
# upload the blob 
blob.upload_from_string(
    data=json.dumps(model_to_json(m)),
    content_type='application/json'
)

print('model saved.')