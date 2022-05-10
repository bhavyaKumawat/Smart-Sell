import base64
import logging
import os

from azure.keyvault.secrets.aio import SecretClient

from commons.msi_helper.msi_util import get_msi_cred

logger = logging.getLogger()
vault_url = os.environ["vault_url"]


async def get_secret(secret_name: str) -> str:
    try:
        async with get_msi_cred() as credential:
            secret_client = SecretClient(vault_url=vault_url, credential=credential)
            secret = await secret_client.get_secret(secret_name)
            return secret.value
    except Exception as ex:
        logger.exception(f'Exception while getting Secret-{secret_name} : {ex!r}')
        raise


async def get_secret_b64(secret_name: str) -> str:
    try:
        async with get_msi_cred() as credential:
            secret_client = SecretClient(vault_url=vault_url, credential=credential)
            secret = await secret_client.get_secret(secret_name)
            b_string = base64.b64decode(secret.value)
            conn_str = b_string.decode('ascii')
            return conn_str
    except Exception as ex:
        logger.exception(f'Exception while getting Secret-{secret_name} : {ex!r}')
        raise
