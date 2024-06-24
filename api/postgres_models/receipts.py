from sqlalchemy import String, Boolean, Integer, Float, Column, text, TIMESTAMP, Date, Time
from api.config.postgresql import Base

class Receipts(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True, nullable=False)
    blob_name = Column(String, nullable=False)
    merchant_name = Column(String)
    subtotal = Column(Float)
    total_tax = Column(Float)
    total_tax_percent = Column(Float)
    discount = Column(Float)
    total = Column(Float, nullable=False)
    transaction_date = Column(Date)
    transaction_time = Column(Time)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    last_modified = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'), onupdate=text('Now()'))
    textract_verified = Column(Boolean, nullable=False, server_default=text('false'))
    payment_settled = Column(Boolean, nullable=False, server_default=text('false'))
    paid_by = Column(Integer)
    
