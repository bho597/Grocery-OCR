from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from api.config.postgresql import get_db
from api.services import receipts as receipt_service
from api.services import line_items as line_items_service
from api.services import calculate

calculateRoute = APIRouter()
base = '/calculate/'


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
    
