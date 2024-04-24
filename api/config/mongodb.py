# import os

# from dotenv import load_dotenv
# from pathlib import Path

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from api.config.settings import MongoSettings

# dotenv_path = Path('mongodb-login.env')
# load_dotenv(dotenv_path=dotenv_path)

# MONGO_USER = os.getenv('mongo_user')
# MONGO_PASSWORD = os.getenv('mongo_password')
# MONGO_APPNAME = os.getenv('mongo_appname')
settings = MongoSettings()
MONGO_URI = f"mongodb+srv://{settings.mongo_user}:{settings.mongo_password}@{settings.mongo_appname}.cmuzcvg.mongodb.net/?retryWrites=true&w=majority&appName={settings.mongo_appname}"

MongoClient = MongoClient(MONGO_URI)
print(MongoClient.list_database_names())



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