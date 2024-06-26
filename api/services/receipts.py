from sqlalchemy.orm import Session

from api.schemas.receipts import Receipt
from api.postgres_models.receipts import Receipts



async def blob_name_verification(db: Session, blob_name: str) -> bool:
    return db.query(Receipts).filter(Receipts.blob_name == blob_name).first() is not None

async def get_receipt_id_by_blob_name(db: Session, blob_name: str) -> int:
    receipt = db.query(Receipts).filter(Receipts.blob_name == blob_name).first()
    return receipt.id if receipt else None

async def get_all_receipts(db: Session):
    all_products = db.query(Receipts).all()
    return all_products

async def upload_receipt(db: Session, receipt_dict, filename: str):
    receipt = Receipt(**receipt_dict, blob_name=filename)
    new_receipt = Receipts(**receipt.model_dump())

    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)


async def get_receipt_by_id(db: Session, id: int) -> dict:
    receipt = db.query(Receipts).filter(Receipts.id == id).first()
    return receipt

async def delete_receipt_by_id(db: Session, delete_post) -> dict:
    db.delete(delete_post)
    db.commit()
    return True

async def update_receipt_by_id(db: Session, update_post, data) -> dict:
    for key, value in data.items():
        setattr(update_post, key, value)
    db.commit()
    return True

async def get_all_unverified_receipts(db: Session) -> dict:
    unverified_receipts = db.query(Receipts).filter_by(textract_verified=False).all()
    return unverified_receipts


