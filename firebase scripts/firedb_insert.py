import csv
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

cred = credentials.Certificate(r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def upload_csv_to_firestore(csv_file_path, collection_name):

    df = pd.read_csv(csv_file_path)
    data_dict = df.to_dict(orient='records')
    for record in data_dict:
        db.collection(collection_name).add(record)

if __name__ == "__main__":
    csv_file_path = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\esbot.csv'

    collection_name = 'ScibowlScrim'
    upload_csv_to_firestore(csv_file_path, collection_name)
