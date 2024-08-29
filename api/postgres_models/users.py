from sqlalchemy import String, Integer, Column, TIMESTAMP, text
from api.config.postgresql import Base

class Users(Base):
    __tablename__ = 'users'


    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(String, nullable=False)
    last_modified = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'), onupdate=text('Now()'))
