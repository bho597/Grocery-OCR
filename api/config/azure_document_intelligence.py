import requests
import logging

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

from api.config.settings import AzureDocumentIntelligenceSettings
from api.config.azure_container import _generate_url

logger = logging.getLogger(__name__)

settings = AzureDocumentIntelligenceSettings()

document_analysis_client = DocumentAnalysisClient(
    endpoint=settings.endpoint, 
    credential=AzureKeyCredential(settings.key)
)


def _azure_document_analysis(
    blob_name: str,
    selected_fileds = [
        "MerchantName",
        "Total",
        "Subtotal",
        "TotalTax",
        "TransactionDate",
        "TransactionTime",
    ],
):
    #TODO: Complete docstring
    """_summary_

    Args:
        blob_name (str): _description_
        selected_fileds (list, optional): _description_. Defaults to [ "MerchantName", "Total", "Subtotal", "TotalTax", "TransactionDate", "TransactionTime"].

    Raises:
        ValueError: _description_
    """    
    blob_url = _generate_url(blob_name)
    blob_content = requests.get(blob_url).content

    try:
        poller_receipt = document_analysis_client.begin_analyze_document("prebuilt-receipt", blob_content)
    except Exception as e:
        logger.error("Error analyzing %r: %s" % (blob_name, e))
        raise
    else:

        result = poller_receipt.result()
        
        if len(result.documents) > 1:
            raise ValueError(f"There are multiple receipts in this file. Please adjust code to take into account.")
        receipt = result.documents[0]
        receipt_dict = {}
        for k in selected_fileds:
            receipt_dict[k] = receipt.fields.get(k).value

        return receipt_dict