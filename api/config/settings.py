from pydantic_settings import BaseSettings

class MongoSettings(BaseSettings):
    mongo_user: str
    mongo_password: str
    mongo_appname: str
    
    class Config:
        env_file = "mongodb-login.env"