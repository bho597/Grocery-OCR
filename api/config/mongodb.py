from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from api.config.settings import MongoSettings

settings = MongoSettings()
MONGO_URI = f"mongodb+srv://{settings.mongo_user}:{settings.mongo_password}@{settings.mongo_appname}.cmuzcvg.mongodb.net/?retryWrites=true&w=majority&appName={settings.mongo_appname}"

client = MongoClient(MONGO_URI)

# receipt = {
#     "store": "test",
# }

database = client.grocery_ocr
receipts = database.receipts
line_items = database.line_items


# test_id = receipts.insert_one(receipt).inserted_id
# print(test_id)
# print(client.list_database_names())



# def connect_to_mongo(uri:str = MONGO_URI):
#     # Create a new client and connect to the server
#     client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

#     # Send a ping to confirm a successful connection
#     try:
#         client.admin.command('ping')
#         print("Pinged your deployment. You successfully connected to MongoDB!")
#     except Exception as e:
#         print(e)
    
#     return client 