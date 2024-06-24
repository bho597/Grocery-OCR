from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='prod.env', extra='ignore')


class PostgreSQLSettings(BaseServiceSettings):
    user: str
    password: str
    hostname: str
    database_name: str
    port: int

    model_config = SettingsConfigDict(env_prefix = "postgresql_")


class AzureContainerSettings(BaseServiceSettings):
    account_name: str
    container_name: str
    account_key: str

    model_config = SettingsConfigDict(env_prefix = "azure_container_")



class AzureDocumentIntelligenceSettings(BaseServiceSettings):
    endpoint: str
    key: str
    
    model_config = SettingsConfigDict(env_prefix = "azure_document_intelligence_")



class Settings(BaseModel):
    postgresql_settings: PostgreSQLSettings = PostgreSQLSettings()
    azure_container_settings: AzureContainerSettings = AzureContainerSettings()
    azure_document_intelligence_settings: AzureDocumentIntelligenceSettings = AzureDocumentIntelligenceSettings()


settings = Settings()