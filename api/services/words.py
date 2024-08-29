from sqlalchemy.orm import Session

from api.schemas.words import Word
from api.postgres_models.words import Words

async def upload_words(db: Session, word_list, receipt_id: int):
    word_dicts = [Word(**word_dict, receipt_id=receipt_id) for word_dict in word_list]
    word_instances = [Words(**word_dict.model_dump()) for word_dict in word_dicts]
    
    db.add_all(word_instances)
    db.commit()
    for instance in word_instances:
        db.refresh(instance)