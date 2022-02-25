import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

vault_url = os.environ["vault_url"]
secret_name = os.environ["secret_name"]

credential = DefaultAzureCredential()

secret_client = SecretClient(vault_url=vault_url, credential=credential)
secret = secret_client.get_secret(secret_name)