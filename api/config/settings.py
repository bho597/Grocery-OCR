from pydantic_settings import BaseSettings

class MongoSettings(BaseSettings):
    mongo_user: str
    mongo_password: str
    mongo_appname: str
    
    class Config:
        env_file = "mongodb-login.env"



class AzureContainerSettings(BaseSettings):
    container_url: str
    
    class Config:
        env_file = "azure-container-credentials.env"


        