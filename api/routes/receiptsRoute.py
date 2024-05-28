from fastapi import APIRouter
from fastapi import status, File, UploadFile, Depends
from sqlalchemy.orm import Session

from api.schemas.receipts import Receipt
from api.postgres_models.receipts import Receipts
from api.config.postgresql import get_db

receiptsRoute = APIRouter()
base = '/receipts/'
# UploadImage = f'{base}image-upload/'

# _notFoundMessage = "Could not find user with the given Id."

@receiptsRoute.post(base)
def create(receipt: Receipt, db: Session = Depends(get_db)):
    new_product = Receipts(**receipt.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@receiptsRoute.get(base)
def get_all(db: Session = Depends(get_db)):
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


# @receiptsRoute.post(UploadImage+'{id}', status_code=status.HTTP_204_NO_CONTENT)
# async def uploadUserImage(id: str, file: UploadFile = File(...)):
#     result = await resultVerification(id)
#     imageUrl = save_picture(file=file, folderName='users', fileName=result['name'])
#     done = await service.savePicture(id, imageUrl)
#     return getResponse(done, errorMessage="An error occurred while saving user image.")



# # Helpers

# async def resultVerification(id: objectid) -> dict:
#     result = await service.getById(id)
#     await riseHttpExceptionIfNotFound(result, message=_notFoundMessage)
#     return result