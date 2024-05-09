from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas

from datetime import datetime, timedelta, timezone

from api.config.settings import AzureContainerSettings

settings = AzureContainerSettings()
default_credential = DefaultAzureCredential()

container_url = f"https://{settings.account_name}.blob.core.windows.net"

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(container_url, credential=default_credential)


# Create BaseBlobService object
def generate_url(blob_name: str):

    token = generate_blob_sas(account_name=settings.account_name, 
                                container_name=settings.container_name,
                                blob_name=blob_name,
                                account_key=settings.account_key,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.now(timezone.utc) + timedelta(hours=1))

    return f'{container_url}/{settings.container_name}/{blob_name}?{token}'