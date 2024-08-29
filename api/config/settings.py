from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from pathlib import Path
from dotenv import load_dotenv

env_file = Path('prod.env')
if env_file.exists():
    load_dotenv(dotenv_path=env_file)

class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, extra='ignore')


class PostgreSQLSettings(BaseServiceSettings):
    url: str

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


class GoogleSheetsSettings(BaseServiceSettings):
    scopes: Union[List[str], str]
    spreadsheet_id: str
    sheet_name: str
    
    model_config = SettingsConfigDict(env_prefix = "google_sheets_")

    @field_validator("scopes", mode="before")
    def validate_transaction_total(cls, v):
        if isinstance(v, str):
            return v.split(',')
        return v

class Settings(BaseModel):
    postgresql_settings: PostgreSQLSettings = PostgreSQLSettings()
    azure_container_settings: AzureContainerSettings = AzureContainerSettings()
    azure_document_intelligence_settings: AzureDocumentIntelligenceSettings = AzureDocumentIntelligenceSettings()
    google_sheets_settings: GoogleSheetsSettings = GoogleSheetsSettings()


settings = Settings()

# print(settings.model_dump())