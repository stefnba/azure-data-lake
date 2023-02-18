"""
See more:
https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli
"""

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, BlobProperties
from azure.core.paging import ItemPaged
from azure.core.exceptions import ClientAuthenticationError, ResourceExistsError
from .base import AzureBaseClient


class AzureBlobClient(AzureBaseClient):
    """
    Client to interact with Azure Storage Account via BlobServiceClient.
    """

    service_client: BlobServiceClient
    container_client: ContainerClient
    blob_client: BlobClient
    
    def init(self):
        """
        Initiates BlobServiceClient.
        """

        try:
            credential = self.auth()
            self.service_client = BlobServiceClient(
                account_url=self.account_url, credential=credential
            )
        except ClientAuthenticationError as exception:
            print("dd", exception)

        except Exception as exception:
            print(exception)


    def get_container_client(self, container: str) -> ContainerClient:
        """
        Get a client to interact with the specified container.
        """
        container_client = self.service_client.get_container_client(container)
        self.container_client = container_client
        return container_client


    def list_blobs(self, container: str) -> ItemPaged[BlobProperties]:
        """
        Lists blobs within the specified container.
        """
        container_client = self.service_client.get_container_client(container)
        blobs: ItemPaged[BlobProperties] = container_client.list_blobs()
        return blobs
