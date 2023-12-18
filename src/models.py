from .database import Base
from sqlalchemy import Column, Integer, String, Float


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    types = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    name_type = Column(String, nullable=False)
    username = Column(String, nullable=False)
    emails = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
