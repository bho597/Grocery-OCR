import logging

from datetime import datetime, timedelta, timezone

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas

from api.config.settings import AzureContainerSettings

logger = logging.getLogger(__name__)

settings = AzureContainerSettings()
default_credential = DefaultAzureCredential()

container_url = f"https://{settings.account_name}.blob.core.windows.net"

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(container_url, credential=default_credential)


def _upload_to_cloud_store(filepath: str) -> str:
    #TODO: complete docstring
    """_summary_

    Args:
        filepath (str): Filepath for image file to upload

    Returns:
        str: Azure storage container blob URL.
    """    
    blob_name = filepath.split('/')[-1]

    container_name = 'receipts'  
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # print("\nUploading to Azure Storage as blob:\n\t" + filename)

    # Upload the created file
    with open(file=filepath, mode="rb") as data:
        try:
            blob_client.upload_blob(data)
        except Exception as e:
            logger.error("Error uploading %r: %s" % (blob_name, e))
            raise
        else:
            return blob_name


def _generate_url(blob_name: str) -> str:
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

