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

async def update_line_item(db: Session, update_post, data) -> bool:
    for key, value in data.items():
        print(f'{key}: {value}')
        setattr(update_post, key, value)
    db.commit()
    return True

async def delete_line_item(db: Session, delete_post) -> bool:
    db.delete(delete_post)
    db.commit()
    return True

async def split_line_item(db: Session, splits, total_price: int, split_post) -> bool:
    initial_splits = [total_price * s for s in splits]
    rounded_splits = [round(amount, 2) for amount in initial_splits]

    total_rounded = sum(rounded_splits)
    difference = round(total_price - total_rounded, 2)
    

    max_index = rounded_splits.index(max(rounded_splits))
    rounded_splits[max_index] += difference
    
    split_post_dict = dict((column.name, getattr(split_post, column.name)) for column in split_post.__table__.columns if column.name != 'id')
    line_item_instances = []
    for rounded_split in rounded_splits:
        new_instance_dict = split_post_dict.copy()
        new_instance_dict['item_total_price'] = rounded_split
        new_instance = LineItems(**new_instance_dict)
        line_item_instances.append(new_instance)

    db.add_all(line_item_instances)
    db.commit()

    for instance in line_item_instances:
        db.refresh(instance)
    return True