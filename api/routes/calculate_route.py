from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from api.config.postgresql import get_db
from api.services import receipts as receipt_service
from api.services import line_items as line_items_service
from api.services import users as users_service
from api.services import calculate

calculateRoute = APIRouter()
base = '/calculate/'

HEADER = ['id', 'item_description', 'item_total_price', 'bought_by']

@calculateRoute.get(base+'verify')
async def verify_textract(db: Session = Depends(get_db)):
    unverified_receipts = await receipt_service.get_all_unverified_receipts(db=db)
    failed_verify_total = []
    failed_verify_line_items = []
    success = []
    for receipt in unverified_receipts:
        if receipt.subtotal is None:
            await calculate.update_subtotal(db=db, receipt=receipt)
        
        if not calculate.verify_total(receipt):
            failed_verify_total.append(receipt.id)
            continue
        
        line_items = await line_items_service.get_line_items_by_receipt_id(db=db, receipt_id=receipt.id)
        if not calculate.verify_line_items(receipt=receipt, line_items=line_items):
            failed_verify_line_items.append(receipt.id)
            continue
        
        await receipt_service.confirm_textract(db=db, receipt=receipt)
        success.append(receipt.id)

    return {
        'failed_verify_total': failed_verify_total,
        'failed_verify_line_items': failed_verify_line_items,
        'success': success,
    }
    
@calculateRoute.get(base+'google_sheets/{receipt_id}')
async def export_receipt_to_google_sheet(
    receipt_id: int,
    db: Session = Depends(get_db),
    header: str = HEADER,
    ids: List[int] = Query(default=None, description="List of integer IDs")
):
    receipt = await receipt_service.get_receipt_by_id(db=db, id=receipt_id)
    line_items = await line_items_service.get_line_items_by_receipt_id(db=db, receipt_id=receipt.id)

    data = [header]
    for line_item in line_items:
        line_item_dict = vars(line_item)
        values = [line_item_dict[col] for col in header]
        data.append(values)

    users = [await users_service.get_name_by_id(db=db, id=id) for id in ids]
    users += ['All']

    await calculate.export_receipt_to_google_sheets(data, users)


@calculateRoute.put((base+'google_sheets/{receipt_id}'))
async def update_line_items_from_google_sheet(receipt_id: int, db: Session = Depends(get_db)):

    line_items = await line_items_service.get_line_items_by_receipt_id(db=db, receipt_id=receipt_id)

    values = calculate.read_google_sheet(range_name=f'Sheet1!A1:D{len(line_items) + 1}')
    
    if not values or len(values) < 2:
        raise HTTPException(status_code=400, detail="Invalid or empty data from the Google Sheet")


    # Skip the header row and update the line items in the database
    for value in values[1:]:
        line_item = await line_items_service.get_line_item_by_id(db=db, id=value[0])
        line_item_dict = {header: getattr(line_item, header) for header in line_item.__table__.columns.keys()}
        bought_by = await users_service.get_user_id_by_name(db=db, user=value[-1]) if value[-1] != 'All' else 0
        line_item_dict['bought_by'] = bought_by
        await line_items_service.update_line_item(db=db, update_post=line_item, data=line_item_dict)