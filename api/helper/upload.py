from api.config.azurecontainer import blob_service_client

def upload_to_cloud_store(filepath: str):
    filename = filepath.split('/')[-1]

    container_name = 'receipts'  
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    print("\nUploading to Azure Storage as blob:\n\t" + filename)

    # Upload the created file
    with open(file=filepath, mode="rb") as data:
        blob_client.upload_blob(data)




########## UPLOAD FILE ################

# from glob import glob
# filepath = glob('assets/verified/*')[0]

# upload_to_cloud_store(glob('assets/verified/*')[0])







##### CHECK BLOB LIST ############

# container_name = 'receipts'
# container_client = blob_service_client.get_container_client(container_name)

# print("\nListing blobs...")

# # List the blobs in the container
# blob_list = container_client.list_blobs()
# for blob in blob_list:
#     print("\t" + blob.name)