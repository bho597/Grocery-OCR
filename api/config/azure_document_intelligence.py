from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

from api.config.settings import AzureDocumentIntelligenceSettings

settings = AzureDocumentIntelligenceSettings()

document_analysis_client = DocumentAnalysisClient(
    endpoint=settings.endpoint, 
    credential=AzureKeyCredential(settings.key)
)