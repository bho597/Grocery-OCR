import requests

# from io import BytesIO
from fastapi import APIRouter
# from fastapi.responses import StreamingResponse
from fastapi import status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
# from azure.core.exceptions import ResourceExistsError

from api.config.postgresql import get_db
# from api.config.azure_container import upload_to_cloud_store, generate_url
# from api.config.azure_document_intelligence import azure_document_analysis
from api.schemas.line_items import LineItem, SplitRequest
from api.services import line_items as line_items_service
from api.services import receipts as receipt_service

lineItemsRoute = APIRouter()
base = '/line_items'
# base_image = '/receipts-image'
# unverified_base = '/unverified_receipts'



@lineItemsRoute.post(base)
async def create_line_item(line_item: LineItem, db: Session = Depends(get_db)):
    receipt_id = line_item.receipt_id
    result = await receipt_service.get_receipt_by_id(db=db, id=receipt_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Could not find provided receipt_id in database: {receipt_id}.")
    return await line_items_service.upload_line_item(db=db, line_item_dict=line_item.model_dump())
    

@lineItemsRoute.get(base)
async def get_line_items_by_receipt(receipt_id: int, db: Session = Depends(get_db)):
    receipt = await receipt_service.get_receipt_by_id(db=db, id=receipt_id)
    line_items = await line_items_service.get_line_items_by_receipt_id(db=db, receipt_id=receipt.id)
    return line_items


@lineItemsRoute.get(base+'/{line_item_id}')
async def get_line_item(line_item_id: int, db: Session = Depends(get_db)):
    line_item = await line_items_service.get_line_item_by_id(db=db, id=line_item_id)
    if line_item is None:
        raise HTTPException(status_code=404, detail=f"Could not find line item with the given Id: {line_item_id}.")
    return line_item


@lineItemsRoute.put(base+'/{line_item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_line_item(line_item_id, data: LineItem, db: Session = Depends(get_db)):
    result = await line_items_service.get_line_item_by_id(db=db, id=line_item_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Could not find line item with the given Id: {line_item_id}.")
    await line_items_service.update_line_item(db=db, update_post=result, data=data.model_dump())
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@lineItemsRoute.delete(base+'/{line_item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_line_item(line_item_id: int, db: Session = Depends(get_db)):
    result = await line_items_service.get_line_item_by_id(db=db, id=line_item_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Could not find line item with the given Id: {line_item_id}.")
    await line_items_service.delete_line_item(db=db, delete_post=result)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@lineItemsRoute.put(base+'/{line_item_id}/split', status_code=status.HTTP_204_NO_CONTENT)
async def split_line_item(line_item_id: int, data: SplitRequest, db: Session = Depends(get_db)):
    result = await line_items_service.get_line_item_by_id(db=db, id=line_item_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Could not find line item with the given Id: {line_item_id}.")

    await line_items_service.split_line_item(db=db, splits=data.quantity, total_price=result.item_total_price, split_post=result)
    await line_items_service.delete_line_item(db=db, delete_post=result)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
