from azure.identity import DefaultAzureCredential

class AzureBaseClient:

    account_url: str

    def __init__(self, account_url: str) -> None:
        self.account_url = account_url
        self.init()


    def init(self):
        pass


    def auth(self):
        """
        Authenticates application through DefaultAzureCredential.
        """
        credential = DefaultAzureCredential()
        return credential