import requests

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

from api.config.settings import AzureDocumentIntelligenceSettings

settings = AzureDocumentIntelligenceSettings()

document_analysis_client = DocumentAnalysisClient(
    endpoint=settings.endpoint, 
    credential=AzureKeyCredential(settings.key)
)


async def azure_document_analysis(
    blob_url: str,
    selected_fileds: dict = {
        "MerchantName": 'merchant_name',
        "Total": 'total',
        "Subtotal": 'subtotal',
        "TotalTax": 'total_tax',
        "TransactionDate": 'transaction_date',
        "TransactionTime": 'transaction_time',
    },
):
    #TODO: Complete docstring
    """_summary_

    Args:
        blob_name (str): _description_
        selected_fileds (list, optional): _description_. Defaults to [ "MerchantName", "Total", "Subtotal", "TotalTax", "TransactionDate", "TransactionTime"].

    Raises:
        ValueError: _description_
    """    
    blob_content = requests.get(blob_url).content
    poller_receipt = document_analysis_client.begin_analyze_document("prebuilt-receipt", blob_content)
    result = poller_receipt.result()
    print(result)
    if len(result.documents) > 1:
        raise ValueError(f"There are multiple receipts in this file. Please adjust image to take into account.")
    receipt = result.documents[0]
    receipt_dict = {}
    for k, v in selected_fileds.items():
        if k in receipt.fields:
            receipt_dict[v] = receipt.fields.get(k).value

    return receipt_dict