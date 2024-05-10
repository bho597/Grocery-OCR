from pydantic_settings import BaseSettings

class MongoSettings(BaseSettings):
    mongo_user: str
    mongo_password: str
    mongo_appname: str
    
    class Config:
        env_file = "mongodb-login.env"



class AzureContainerSettings(BaseSettings):
    account_name: str
    container_name: str
    account_key: str
    
    class Config:
        env_file = "azure-container-credentials.env"



class AzureDocumentIntelligenceSettings(BaseSettings):
    endpoint: str
    key: str
    
    class Config:
        env_file = "azure-document-intelligence.env"