from sqlalchemy import String, Boolean, Integer, Float, Column
from api.config.postgresql import Base

class LineItems(Base):
    __tablename__ = 'line_items'

    id = Column(Integer, primary_key=True, nullable=False)
    receipt_id = Column(Integer, nullable=False)
    item_price = Column(Float)
    is_taxed = Column(Boolean)
    bought_by = Column(Integer)
