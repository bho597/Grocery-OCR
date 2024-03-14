import os
import pandas as pd
import json
import glob 
import textdistance as td

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path('azure-credentials.env')
load_dotenv(dotenv_path=dotenv_path)

endpoint = os.getenv('ENDPOINT')
key = os.getenv('KEY')


def analyze_read(
    image_filename,
    verbose=True,
):
    output_dir = image_filename.split(".")[0]

    # Remove '#' from code below in prod
    if any(os.path.isdir(directory) for directory in glob.glob(f'outputs/*/{output_dir}')):
        raise FileExistsError(f"The file has already been analyzed. Output directory '{output_dir}' already exists.")
        
    with open(f'assets/unverified/{image_filename}', "rb") as image_file:
        byte_data = image_file.read()
    
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    try:
        poller_receipt = document_analysis_client.begin_analyze_document(
                "prebuilt-receipt", byte_data)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    else:

        result = poller_receipt.result()
        

        json_dict = {
            "receipt_content": result.content
        }

        if len(result.documents) > 1:
            raise ValueError(f"There are multiple receipts in this file. Please adjust code to take into account.")
        receipt = result.documents[0]


        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            json_dict["merchant_name"] = merchant_name.value
            json_dict["merchant_name_confidence"] = merchant_name.confidence

        store_name = _get_store_name(merchant_name.value) if merchant_name else 'other'
        os.makedirs(f'outputs/{store_name}/{output_dir}')

        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            json_dict["transaction_date"] = str(transaction_date.value)
            json_dict["transaction_date_confidence"] = transaction_date.confidence
        if receipt.fields.get("Items"):
            items = []
            for _, item in enumerate(receipt.fields.get("Items").value):
                item_dict = {}
                item_description = item.value.get("Description")
                if item_description:
                    item_dict["item_description"] = item_description.value
                    item_dict["item_description_confidence"] = item_description.confidence
                item_total_price = item.value.get("TotalPrice")
                if item_total_price:
                    item_dict["item_total_price"] = item_total_price.value
                    item_dict["item_total_price_confidence"] = item_total_price.confidence
                if item_dict:
                    items.append(item_dict)
            json_dict['items'] = items
        tax = receipt.fields.get("TotalTax")
        if tax:
            json_dict["tax"] = tax.value
            json_dict["tax_confidence"] = tax.confidence
        total = receipt.fields.get("Total")
        if total:
            json_dict["total"] = total.value
            json_dict["total_confidence"] = total.confidence


        for page in result.pages:
            receipt_dict = {
                'content': [],
                'confidence': [],
                'bounding_box_point_1_x': [],
                'bounding_box_point_1_y': [],
                'bounding_box_point_2_x': [],
                'bounding_box_point_2_y': [],
                'bounding_box_point_3_x': [],
                'bounding_box_point_3_y': [],
                'bounding_box_point_4_x': [],
                'bounding_box_point_4_y': [],
            }
            for l in page.lines:
                print(l.content)
            for word in page.words:
                receipt_dict['content'].append(word.content)
                receipt_dict['confidence'].append(word.confidence)
                receipt_dict['bounding_box_point_1_x'].append(word.polygon[0][0])
                receipt_dict['bounding_box_point_1_y'].append(word.polygon[0][1])
                receipt_dict['bounding_box_point_2_x'].append(word.polygon[1][0])
                receipt_dict['bounding_box_point_2_y'].append(word.polygon[1][1])
                receipt_dict['bounding_box_point_3_x'].append(word.polygon[2][0])
                receipt_dict['bounding_box_point_3_y'].append(word.polygon[2][1])
                receipt_dict['bounding_box_point_4_x'].append(word.polygon[3][0])
                receipt_dict['bounding_box_point_4_y'].append(word.polygon[3][1])

                if verbose: print(
                    "...Word '{}' has a confidence of {} within bounding box '{}'".format(
                        word.content, 
                        word.confidence,
                        format_bounding_box(word.polygon),
                    )
                )

                df = pd.DataFrame(receipt_dict)
                df.to_csv(f'outputs/{store_name}/{output_dir}/word_confidence.csv', index=False)
        

        with open(f'outputs/{store_name}/{output_dir}/metadata.json', 'w', encoding='utf-8') as f:
            json.dump(json_dict, f, ensure_ascii=False, indent=4)

        if verbose: print("----------------------------------------")
    finally:
        print(f'Image {image_filename} was successfully textracted.')

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])


def _get_store_name(
    merchant_name: str,
    threshold: int = .5,
):
    merchant_name_dict = {
        'Berkeley Bowl': 'berkeley_bowl',
        'Costco': 'costco',
        'Safeway': 'safeway',
        "Trader Joe's": 'trader_joes',
        "Ikea": 'ikea',
    }

    highest_score, store_name = 0, 'other'
    for key, val in merchant_name_dict.items():
        score = td.levenshtein.normalized_similarity(key.lower(), merchant_name.lower())
        if score > highest_score and score > threshold:
            highest_score = score
            store_name = val
    
    return store_name




if __name__ == "__main__":
    asset_files = os.listdir('assets/unverified')
    for filename in asset_files:
        dir_name = filename.split('.')[0]
        
        if len(glob.glob(f'outputs/*/{dir_name}')) == 0:           
            analyze_read(
                image_filename=filename,
                verbose=False
            )
