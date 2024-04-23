
import os

from dotenv import load_dotenv
from pathlib import Path

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


dotenv_path = Path('mongodb-login.env')
load_dotenv(dotenv_path=dotenv_path)

mongo_user = os.getenv('mongo_user')
mongo_password = os.getenv('mongo_password')
mongo_appname = os.getenv('mongo_appname')

uri = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_appname}.cmuzcvg.mongodb.net/?retryWrites=true&w=majority&appName={mongo_appname}"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)