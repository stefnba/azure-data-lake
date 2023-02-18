"""
Interact with Azure Data Lake Gen 2 through the DataLakeServiceClient.

Learn more on:
https://learn.microsoft.com/en-us/python/api/azure-storage-file-datalake/azure.storage.filedatalake.datalakeserviceclient?view=azure-python
"""


import os
from azure.core.paging import ItemPaged

from azure.core.exceptions import ClientAuthenticationError, ResourceExistsError
from azure.storage.filedatalake import (
    DataLakeServiceClient,
    FileSystemClient,
    DataLakeDirectoryClient,
    DataLakeFileClient,
    PathProperties,
)
from .base import AzureBaseClient


class AzureDataLakeClient(AzureBaseClient):
    """
    DataLakeServiceClient has several sub-clients:
    - FileSystemClient (similar to containers)
    - DataLakeDirectoryClient (similar to folders)
    - DataLakeFileClient
    """

    service_client: DataLakeServiceClient
    file_system_client: FileSystemClient
    file_client: DataLakeFileClient   

    def init(self):
        """
        Initiates DataLakeServiceClient.
        """

        try:
            credential = self.auth()
            self.service_client = DataLakeServiceClient(
                account_url=self.account_url, credential=credential
            )
        except ClientAuthenticationError as exception:
            print("dd", exception)

        except Exception as exception:
            print(exception)

    def create_file_system(self, name: str) -> FileSystemClient:
        """
        Create file systems/containers and return file system client
        """
        try:
            file_system_client = self.service_client.create_file_system(file_system=name)
            self.file_system_client = file_system_client
            return file_system_client

        except ResourceExistsError as exception:
            print(exception)
            raise exception

    def get_file_system(self, name: str) -> FileSystemClient:
        """
        Get a client to interact with the specified file system/container.
        """
        file_system_client = self.service_client.get_file_system_client(file_system=name)
        self.file_system_client = file_system_client
        return file_system_client

    def list_file_systems(self) -> list:
        """
        List file systems/containers
        """
        try:
            file_systems = self.service_client.list_file_systems()
            return list(file_systems)
        except Exception as exception:
            print(exception)
            raise exception

    def create_directory(
        self, name: str, file_system_client: FileSystemClient | None = None
    ) -> DataLakeDirectoryClient:
        """
        Create a new directory for provided FileSystemClient. If no
        """
        try:
            if file_system_client is None:
                file_system_client = self.file_system_client
            if file_system_client is None:
                raise Exception("Directory cannot be created, no FileSystemClient provided.")
            directory_client = file_system_client.create_directory(name)

            return directory_client

        except Exception as exception:
            print(exception)
            raise exception

    def list_directory_contents(self, file_system: str, directory: str | None = None) -> ItemPaged[PathProperties]:
        """
        List directory contents by calling the FileSystemClient.get_paths method.
        """
        try:
            file_system_client = self.service_client.get_file_system_client(file_system=file_system)
            paths: ItemPaged[PathProperties] = file_system_client.get_paths(path=directory)

            for path in paths:
                print(path.name)

            return paths

        except Exception as exception:
            print(exception)
            raise exception

    def get_file_client(self, path: str) -> DataLakeFileClient:
        """ """
        file_client = self.service_client.get_file_client(self.file_client, path)
        self.file_client = file_client
        return file_client

    def download_file(self, file_system: str, remote_file: str, local_file_path: str):
        """
        Download a file from the Data Lake.
        """
        try:
            file_client = self.service_client.get_file_client(file_system=file_system, file_path=remote_file)
            downloadde_file = file_client.download_file()
            downloaded_bytes = downloadde_file.readall()

            with open(local_file_path, "wb") as local:
                local.write(downloaded_bytes)

        except Exception as exception:
            print(exception)
            raise exception

    def upload_file(self, remote_file: str, file_system: str, local_file_path: str):
        """
        Upload a file to the Data Lake.
        """
        try:
            file_client = self.service_client.get_file_client(file_system=file_system, file_path=remote_file)
            file_client.create_file()

            with open(local_file_path, "rb") as local_file:
                file_contents = local_file.read()

            file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
            file_client.flush_data(len(file_contents))

        except Exception as exception:
            print(exception)
            raise exception
