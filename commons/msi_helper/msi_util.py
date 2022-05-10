from azure.identity.aio import DefaultAzureCredential


def get_msi_cred():
    return DefaultAzureCredential()
