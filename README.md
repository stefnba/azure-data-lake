# Azure Data Lake SDK

Python SDK for Azure Storage.

## Getting started

Setup virtual environment and install packages.

```bash
make setup
make install-dev
```

## Authentification

Authentification is done through [DefaultAzureCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python).

```bash
pip install azure-identity
```

```py
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
```

### Local Development

For local development, Azure CLI is used as long as VS Code Auth is disabled.

Set tenant id in VS Code.

```bash
az login
```

### Production

https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview#authentication-during-local-development


## IAM Roles

It's not enough for the app and account to be added as `OWNERS` for the sotrage account, they also need to have the role `STORAGE BLOB DATA CONTRIBUTOR`. Go to `storage account > IAM > Add role and add the special permission`.