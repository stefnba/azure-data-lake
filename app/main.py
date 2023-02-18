import os
from typing import cast
from dotenv import load_dotenv

from clients import AzureDataLakeClient, AzureBlobClient

load_dotenv()

ACCOUNT_URL = cast(str, os.environ.get('ACCOUNT_URL'))
ACCOUNT_URL = cast(str, os.environ.get('ACCOUNT_URL_BLOB'))

def main():
    print('started')
    client = AzureDataLakeClient(ACCOUNT_URL)

    file_systems = client.list_file_systems()
    print(file_systems)


    client_blob = AzureBlobClient(ACCOUNT_URL)

    blobs = client_blob.list_blobs('dev')
    for blob in blobs:
        print(blob.name)


if __name__ == '__main__':
    print(ACCOUNT_URL)
    main()