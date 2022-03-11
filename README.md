# Get-Predictions-Using-Custom-Trained-Model

### Intro
This is a project to create an endpoint that you can request and get predictions from using your custom-trained model. The endpoint was created in Google Cloud. In this project, time series sales data was extracted from Kaggle　[ドキュメント情報共有サービス NotePM](https://notepm.jp) and uploaded to Google Cloud Storage. The model that would be trained here is a model to forecast sales values in the future. The creating endpoint steps details are shown below.

---

### GCP Services used in this project
- Cloud Storage
- BigQuery
- Vertex AI
- Container Registry

---

### 1. Download a csv file from Kaggle
You can download the file from [here](https://www.kaggle.com/c/store-sales-time-series-forecasting/overview). For the simplication, I just downloaded a train.csv.

### 2. Upload the file in Cloud Storage
Login to GCP and go to Cloud Storage and create a bucket. Upload the csv file from your local storage.

### 3. Load the csv file into BigQuery
Create a dataset and a table in Bigquery. Use bq command to load the data.

```
bq load \
--autodetect \
--source_format=CSV \
YOUR_DATASET.YOUR_TABLE \
gs://YOUR_BUCKET/train.csv
```
