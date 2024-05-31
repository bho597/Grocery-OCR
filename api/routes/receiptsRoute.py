from fastapi import APIRouter
from fastapi import status, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from azure.core.exceptions import ResourceExistsError


from api.schemas.receipts import Receipt
from api.postgres_models.receipts import Receipts
from api.config.postgresql import get_db
from api.config.azure_container import upload_to_cloud_store, generate_url
from api.config.azure_document_intelligence import azure_document_analysis

receiptsRoute = APIRouter()
base = '/receipts/'
UploadImage = f'{base}image-upload/'



@receiptsRoute.post(base)
async def create_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Unsupported Media Type. Only images are allowed.")
    content = await file.read()
    try:
        print('')
        # await upload_to_cloud_store(receipt_file=content, blob_name=file.filename)
    except ResourceExistsError as e:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        image_url = generate_url(blob_name=file.filename)
        receipt_dict = await azure_document_analysis(blob_url=image_url)
        
        receipt = Receipt(**receipt_dict, blob_name=file.filename)
        new_receipt = Receipts(**receipt.dict())
        
        await db.add(new_receipt)
        db.commit()
        db.refresh(new_receipt)
        return new_receipt
    


@receiptsRoute.get(base)
def get_all_receipts(db: Session = Depends(get_db)):
    all_products = db.query(Receipts).all()
    return all_products


# @receiptsRoute.get(base+'{id}')
# async def getById(id):
#     return await resultVerification(id)


# @receiptsRoute.get(base)
# async def getAll():
#     return await service.getAllUser()

# @receiptsRoute.post(base)
# async def InsertUser(data: CreateUser):
#     return await service.InsertUser(data)


# @receiptsRoute.put(base+'{id}', status_code=status.HTTP_204_NO_CONTENT)
# async def updateUser(id, data: CreateUser):
#     await resultVerification(id)
#     done : bool = await service.updateUser(id,data);
#     return getResponse(done, errorMessage="An error occurred while editing the user information.")


# @receiptsRoute.delete(base+'{id}', status_code=status.HTTP_204_NO_CONTENT)
# async def deleteUser(id):
#     await resultVerification(id)
#     done : bool = await service.deleteUser(id);
#     return getResponse(done, errorMessage="There was an error.")   

