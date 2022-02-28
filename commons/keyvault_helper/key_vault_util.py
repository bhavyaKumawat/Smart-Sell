import base64
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

vault_url = os.environ["vault_url"]
credential = DefaultAzureCredential()

secret_client = SecretClient(vault_url=vault_url, credential=credential)


def get_secret(secret_name: str) -> str:
    secret = secret_client.get_secret(secret_name)
    return secret.value


def get_secret_b64(secret_name: str) -> str:
    secret = secret_client.get_secret(secret_name)
    b_string = base64.b64decode(secret.value)
    conn_str = b_string.decode('ascii')
    return conn_str
