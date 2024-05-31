from datetime import datetime, timedelta, timezone

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas

from api.config.settings import AzureContainerSettings

settings = AzureContainerSettings()
# default_credential = DefaultAzureCredential()

container_url = f"https://{settings.account_name}.blob.core.windows.net"

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(container_url, credential=settings.account_key)


async def upload_to_cloud_store(receipt_file: bytes, blob_name: str):
    """
    _summary_

    Args:
        receipt_file (bytes): _description_
        filename (str): _description_
    """    
    #TODO: complete docstring
    blob_client = blob_service_client.get_blob_client(container=settings.container_name, blob=blob_name)
    blob_client.upload_blob(receipt_file)
    return True


def generate_url(blob_name: str) -> str:
    #TODO: complete docstring
    """_summary_

    Args:
        blob_name (str): _description_

    Returns:
        str: _description_
    """
    token = generate_blob_sas(account_name=settings.account_name, 
                                container_name=settings.container_name,
                                blob_name=blob_name,
                                account_key=settings.account_key,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.now(timezone.utc) + timedelta(hours=1))

    return f'{container_url}/{settings.container_name}/{blob_name}?{token}'

