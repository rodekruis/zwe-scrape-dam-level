import json
from azure.storage.blob import BlobServiceClient, BlobClient


def get_blob_service_client(blob_path):
    with open("../credentials/blobstorage_secrets.json") as file:
        blobstorage_secrets = json.load(file)
    blob_service_client = BlobServiceClient.from_connection_string(blobstorage_secrets['connection_string'])
    container = blobstorage_secrets['container']
    return blob_service_client.get_blob_client(container=container, blob=blob_path)