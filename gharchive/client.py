from google.cloud import bigquery
import os
def create_client(key_path):
    return bigquery.Client.from_service_account_json(key_path)
