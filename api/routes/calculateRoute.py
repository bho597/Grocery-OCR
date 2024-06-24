from fastapi import APIRouter
from fastapi import Depends#, status, File, UploadFile, HTTPException
# from sqlalchemy import func
from sqlalchemy.orm import Session
# from azure.core.exceptions import ResourceExistsError

from api.config.postgresql import get_db
# from api.config.azure_container import upload_to_cloud_store, generate_url
# from api.config.azure_document_intelligence import azure_document_analysis
from api.services import database as database_service
from api.services.calculate import verify_line_items
# from api.postgres_models.receipts import Receipts

calculateRoute = APIRouter()
base = '/calculate/'



@calculateRoute.get(base+'verify')
async def verify_textract(db: Session = Depends(get_db)):
    unverified_receipts = await database_service.get_all_unverified_receipts(db=db)
    for receipt in unverified_receipts:
        print(verify_line_items(receipt))
        break

    return {'content': None}
    
