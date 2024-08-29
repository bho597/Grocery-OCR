from sqlalchemy import String, Integer, Float, Column, TIMESTAMP, text
from api.config.postgresql import Base

class Words(Base):
    __tablename__ = 'words'


    id = Column(Integer, primary_key=True, nullable=False)
    word = Column(String, nullable=False)
    word_index = Column(Integer, nullable=False)
    line_index = Column(Integer)
    confidence = Column(Float)
    min_x = Column(Integer, nullable=False)
    min_y = Column(Integer, nullable=False)
    max_x = Column(Integer, nullable=False)
    max_y = Column(Integer, nullable=False)
    receipt_id = Column(Integer, nullable=False)
    last_modified = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'), onupdate=text('Now()'))
