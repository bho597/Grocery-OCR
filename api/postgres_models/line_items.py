from sqlalchemy import String, Boolean, Integer, Float, Column, TIMESTAMP, text
from api.config.postgresql import Base

class LineItems(Base):
    __tablename__ = 'line_items'

    id = Column(Integer, primary_key=True, nullable=False)
    item_description = Column(String)
    item_total_price = Column(Float)
    line_item_number = Column(Integer)
    receipt_id = Column(Integer, nullable=False)
    is_taxed = Column(Boolean)
    bought_by = Column(Integer)
    last_modified = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'), onupdate=text('Now()'))
