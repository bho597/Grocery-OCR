from api.config.azurecontainer import blob_service_client, generate_url

def upload_to_cloud_store(filepath: str):
    filename = filepath.split('/')[-1]

    container_name = 'receipts'  
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    print("\nUploading to Azure Storage as blob:\n\t" + filename)

    # Upload the created file
    with open(file=filepath, mode="rb") as data:
        blob_client.upload_blob(data)

    blob_url = blob_client.url

    print("Uploaded blob URL:", blob_url)

    return blob_url



########## UPLOAD FILE ################

# from glob import glob
# filepath = glob('assets/verified/*')[0]

# upload_to_cloud_store(glob('assets/verified/*')[0])


import requests
from PIL import Image
from io import BytesIO

def display_image_from_url(url):
    try:
        response = requests.get(url)
        # print(response)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.show()
    except Exception as e:
        print("Error:", e)

# Example usage:
# Assuming blob_url is the URL of the uploaded blob
blob_url = generate_url("20231029_costco.jpg")
# print(blob_url)

display_image_from_url(blob_url)




##### CHECK BLOB LIST ############

# container_name = 'receipts'
# container_client = blob_service_client.get_container_client(container_name)

# print("\nListing blobs...")

# # List the blobs in the container
# blob_list = container_client.list_blobs()
# for blob in blob_list:
#     print("\t" + blob.name)