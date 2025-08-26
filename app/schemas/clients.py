from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class ClientInDB(ClientBase):
    id: int

    class Config:
        from_attributes = True

class Client(ClientInDB):
    pass

class ClientResponse(BaseModel):
    message: str
    client: ClientInDB

    class Config:
        from_attributes = True

class GetResponse(BaseModel):
    message: str
    clients: List[ClientInDB]

    class Config:
        from_attributes = True
