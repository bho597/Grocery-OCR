from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from api.config.settings import AzureContainerSettings

settings = AzureContainerSettings()
default_credential = DefaultAzureCredential()

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(settings.container_url, credential=default_credential)