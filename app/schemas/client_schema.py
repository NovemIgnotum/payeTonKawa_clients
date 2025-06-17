from pydantic import BaseModel, EmailStr

class ClientCreate(BaseModel):
    nom: str
    email: EmailStr

class ClientResponse(ClientCreate):
    id: int

    class Config:
        orm_mode = True
