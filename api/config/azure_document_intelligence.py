import requests

from typing import Tuple

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

from api.config.settings import AzureDocumentIntelligenceSettings

settings = AzureDocumentIntelligenceSettings()

document_analysis_client = DocumentAnalysisClient(
    endpoint=settings.endpoint, 
    credential=AzureKeyCredential(settings.key)
)


def azure_document_analysis(
    blob_url: str,
):
    #TODO: Complete docstring
    """_summary_

    Args:
        blob_url (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """    
    blob_content = requests.get(blob_url).content

    poller_receipt = document_analysis_client.begin_analyze_document("prebuilt-receipt", blob_content)
    result = poller_receipt.result()


    if len(result.documents) > 1:
        raise ValueError(f"There are multiple receipts in this file. Please adjust image to take into account.")
    receipt = result.documents[0]
    page = result.pages[0]
    analysis_dict = {}
    
    analysis_dict['receipt'] = _get_receipt_dict(receipt)
    analysis_dict['line_items'] = _get_line_items_list(receipt)
    analysis_dict['words'] = _get_word_list(page)

    return analysis_dict


def _get_receipt_dict(
    receipt,
    selected_fileds: dict = {
        "MerchantName": 'merchant_name',
        "Total": 'total',
        "Subtotal": 'subtotal',
        "TotalTax": 'total_tax',
        "TransactionDate": 'transaction_date',
        "TransactionTime": 'transaction_time',
    },
):
    receipt_dict = {}
    for k, v in selected_fileds.items():
        if k in receipt.fields:
            receipt_dict[v] = receipt.fields.get(k).value

    return receipt_dict

def _get_line_items_list(receipt):
    items = []
    if receipt.fields.get("Items"):
        for _, item in enumerate(receipt.fields.get("Items").value):
            item_dict = {}
            item_description = item.value.get("Description")
            item_total_price = item.value.get("TotalPrice")

            if item_description is None and item_total_price is None:
                continue

            item_dict["item_description"] = item_description.value if item_description else None
            item_dict["item_total_price"] = item_total_price.value if item_total_price else None
        
            items.append(item_dict)

    return items

def _extract_bounding_box(polygon)-> Tuple[int, int, int, int]:
    """Extract the bounding box coordinates from a polygon."""
    x_coords = [point.x for point in polygon]
    y_coords = [point.y for point in polygon]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    return min_x, min_y, max_x, max_y

def _is_within(word_bbox, line_bbox):
    """Check if word bounding box is within line bounding box."""
    w_min_x, w_min_y, w_max_x, w_max_y = word_bbox
    l_min_x, l_min_y, l_max_x, l_max_y = line_bbox
    return l_min_x <= w_min_x and w_max_x <= l_max_x and l_min_y <= w_min_y and w_max_y <= l_max_y


def _get_word_list(
    page
):
    word_bboxes = [(i, word.content, _extract_bounding_box(word.polygon), word.confidence) for i, word in enumerate(page.words)]
    line_bboxes = [(i, line.content, _extract_bounding_box(line.polygon)) for i, line in enumerate(page.lines)]

    word_list = []
    for word_index, word, word_bbox, confidence in word_bboxes:
        for line_index, line, line_bbox in line_bboxes:
            if _is_within(word_bbox, line_bbox):
                word_dict = {}

                if word not in line:
                    #TODO: log info
                    print(f'Word content "{word}" is not withint line content "{line}"')
                    word_dict['line_index'] = None
                else:
                    word_dict['line_index'] = line_index
                    
                word_dict['word'] = word
                word_dict['word_index'] = word_index
                word_dict['confidence'] = confidence
                word_dict['min_x'] = word_bbox[0]
                word_dict['min_y'] = word_bbox[1]
                word_dict['max_x'] = word_bbox[2]
                word_dict['max_y'] = word_bbox[3]
                word_list.append(word_dict)

    return word_list