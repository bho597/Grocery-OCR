from sqlalchemy import func
from sqlalchemy.orm import Session

from api.schemas.line_items import LineItem
from api.postgres_models.line_items import LineItems


async def upload_line_item(db: Session, line_item_dict):
    new_line_item = LineItems(**line_item_dict)
    db.add(new_line_item)
    db.commit()
    db.refresh(new_line_item)

    return new_line_item

async def upload_line_items(db: Session, line_item_list, receipt_id: int):
    line_item_dicts = [LineItem(**line_item_dict, receipt_id=receipt_id, line_item_number=i+1) for i, line_item_dict in enumerate(line_item_list)]
    line_item_instances = [LineItems(**line_item_dict.model_dump()) for line_item_dict in line_item_dicts]
    
    db.add_all(line_item_instances)
    db.commit()
    for instance in line_item_instances:
        db.refresh(instance)

    return line_item_instances

async def get_line_item_by_id(db: Session, id: int):
    line_item = db.query(LineItems).filter_by(id=id).first()
    return line_item

async def get_line_items_by_receipt_id(db: Session, receipt_id: int):
    line_items = db.query(LineItems).filter_by(receipt_id=receipt_id).all()
    return line_items

async def get_next_line_number(db: Session, receipt_id: int):
    line_number = db.query(func.max(LineItems.line_item_number)).filter(LineItems.receipt_id == receipt_id).scalar() + 1
    return line_number

async def update_line_item_by_id(db: Session, update_post, data) -> dict:
    for key, value in data.items():
        setattr(update_post, key, value)
    db.commit()
    return True

async def delete_line_item_by_id(db: Session, delete_post) -> dict:
    db.delete(delete_post)
    db.commit()
    return True