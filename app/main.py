import os
from typing import cast
from dotenv import load_dotenv

from clients.datalake import AzureDataLakeClient

load_dotenv()

ACCOUNT_URL = cast(str, os.environ.get('ACCOUNT_URL'))

def main():
    print('started')
    client = AzureDataLakeClient(ACCOUNT_URL)

    file_systems = client.list_file_systems()
    print(file_systems)


if __name__ == '__main__':
    print(ACCOUNT_URL)
    main()