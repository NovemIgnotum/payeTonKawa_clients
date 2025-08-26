from sqlalchemy import Column, VARCHAR, TIMESTAMP, Integer
from database.session import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(127), nullable=False)
    email = Column(VARCHAR(127), unique=True, nullable=False)
    phone = Column(VARCHAR(20), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    class Config:
        from_attributes = True
