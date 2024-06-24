from fastapi import APIRouter
from fastapi import status, UploadFile, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from azure.core.exceptions import ResourceExistsError

from api.config.postgresql import get_db
from api.config.azure_container import upload_to_cloud_store, generate_url
from api.config.azure_document_intelligence import azure_document_analysis
from api.schemas.receipts import Receipt
from api.services import database as db_service

receiptsRoute = APIRouter()
base = '/receipts'
unverified_base = '/unverified_receipts'



@receiptsRoute.post(base)
async def create_receipt(files: list[UploadFile], db: Session = Depends(get_db)):
    success, fail = [], []
    for file in files:
        try:
            upload_data = True
            if not file.content_type.startswith("image/"):
                raise HTTPException(status_code=415, detail="Unsupported Media Type. Only images are allowed.")
            content = await file.read()
            try:
                await upload_to_cloud_store(receipt_file=content, blob_name=file.filename)
            except ResourceExistsError as e:
                # TODO: Change to log
                print(f'Blob name "{file.filename} already exists in cloud store.')
            except Exception as e:
                upload_data = False
                raise HTTPException(status_code=500, detail=f'Azure Container Error: ' + str(e))
            finally:
                if upload_data:
                    image_url = generate_url(blob_name=file.filename)
                    analysis_dict = azure_document_analysis(blob_url=image_url)
                    receipt_dict, line_item_list, word_list = analysis_dict['receipt'], analysis_dict['line_items'], analysis_dict['words']
                    if await db_service.blob_name_verification(db=db, blob_name=file.filename):
                        raise HTTPException(status_code=409, detail=f"Receipt blob_name '{file.filename}' already exists in the database.")
                    else:
                        await db_service.upload_receipt_to_database(db=db, receipt_dict=receipt_dict, filename=file.filename)
                        receipt_id = await db_service.get_receipt_id_by_blob_name(db=db, blob_name=file.filename)
                        await db_service.upload_line_items_to_database(db=db, line_item_list=line_item_list, receipt_id=receipt_id)
                        await db_service.upload_words_to_database(db=db, word_list=word_list, receipt_id=receipt_id)
        except Exception as e:
            print(str(e))
            fail.append(file.filename)
        else:
            success.append(file.filename)
            
    return {
        'sucessful_uploads': success,
        'failed_uploads': fail
    }
    


@receiptsRoute.get(base)
async def get_receipts(db: Session = Depends(get_db)):
    all_products = await db_service.get_all_receipts(db=db)
    return all_products


@receiptsRoute.get(base+'/{id}')
async def get_receipt(id: int, db: Session = Depends(get_db)):
    result = await db_service.get_receipt_by_id(db=db, id=id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Could not find user with the given Id: {id}.")
    return result


@receiptsRoute.get(unverified_base)
async def get_unverified_receipts(db: Session = Depends(get_db)):
    unverified_receipts = await db_service.get_all_unverified_receipts(db=db)
    return unverified_receipts



@receiptsRoute.put(base+'/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_receipt(id, data: Receipt, db: Session = Depends(get_db)):
    result = await db_service.get_receipt_by_id(db=db, id=id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Could not find user with the given Id: {id}.")
    else:
        await db_service.update_receipt_by_id(db=db, update_post=result, data=data.model_dump())
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@receiptsRoute.delete(base+'/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_receipt(id: int, db: Session = Depends(get_db)):
    result = await db_service.get_receipt_by_id(db=db, id=id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Could not find user with the given Id: {id}.")
    else:
        await db_service.delete_receipt_by_id(db=db, delete_post=result)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



