import logging
import requests

from api.config.azure_container import blob_service_client, generate_url
from api.config.azure_document_intelligence import document_analysis_client

logger = logging.getLogger(__name__)


def _upload_to_cloud_store(filepath: str) -> str:
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


def _azure_document_analysis(blob_name):
    
    # blob_url = generate_url(blob_name)
    # blob_content = requests.get(blob_url).content

    # try:
    #     poller_receipt = document_analysis_client.begin_analyze_document("prebuilt-receipt", blob_content)
    # except Exception as e:
    #     logger.error("Error analyzing %r: %s" % (blob_name, e))
    #     raise
    # else:

    #     result = poller_receipt.result()
    

    #     json_dict = {
    #         "receipt_content": result.content
    #     }
        
    #     if len(result.documents) > 1:
    #         raise ValueError(f"There are multiple receipts in this file. Please adjust code to take into account.")
    #     receipt = result.documents[0]

    if True:
        #TODO: delete later
        import pickle
        import pprint
        with open('temp.pickle', 'rb') as file:
            receipt = pickle.load(file)
        # print(receipt.fields.keys())
        # ['Items', 'MerchantAddress', 'MerchantName', 'MerchantPhoneNumber', 'Subtotal', 'TaxDetails', 'Total', 'TotalTax', 'TransactionDate', 'TransactionTime']
        temp_keys = list(receipt.fields.keys())
        for k in temp_keys:
            print(f'Key: {k}')
            pprint.pprint(receipt.fields[k].to_dict())
        # pprint.pprint(receipt.fields[temp_keys[2]], depth=1, width=60)

        return
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
        


print(_azure_document_analysis("20231029_costco.jpg"))


import os
import pandas as pd
import json
import glob 


from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


def upload_receipt(
    filepath: str,
):
    blob_url = _upload_to_cloud_store(filepath=filepath)

    return blob_url
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

########## UPLOAD FILE ################

# from glob import glob
# filepath = glob('assets/verified/*')[0]

# upload_to_cloud_store(glob('assets/verified/*')[0])



############ DISPLAY IMAGE ###############
# import requests
# from PIL import Image
# from io import BytesIO

# def display_image_from_url(url):
#     try:
#         response = requests.get(url)
#         # print(response)
#         img_data = response.content
#         img = Image.open(BytesIO(img_data))
#         img.show()
#     except Exception as e:
#         print("Error:", e)

# # Example usage:
# # Assuming blob_url is the URL of the uploaded blob
# blob_url = generate_url("20231029_costco.jpg")
# # print(blob_url)

# display_image_from_url(blob_url)




##### CHECK BLOB LIST ############

# container_name = 'receipts'
# container_client = blob_service_client.get_container_client(container_name)

# print("\nListing blobs...")

# # List the blobs in the container
# blob_list = container_client.list_blobs()
# for blob in blob_list:
#     print("\t" + blob.name)