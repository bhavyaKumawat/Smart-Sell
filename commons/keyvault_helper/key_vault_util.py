import base64
import os
from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient

vault_url = os.environ["vault_url"]


async def get_secret(secret_name: str) -> str:
    credential = DefaultAzureCredential()
    async with credential:
        secret_client = SecretClient(vault_url=vault_url, credential=credential)
        secret = await secret_client.get_secret(secret_name)
        return secret.value


async def get_secret_b64(secret_name: str) -> str:
    credential = DefaultAzureCredential()
    async with credential:
        secret_client = SecretClient(vault_url=vault_url, credential=credential)
        secret = await secret_client.get_secret(secret_name)
        b_string = base64.b64decode(secret.value)
        conn_str = b_string.decode('ascii')
        return conn_str
