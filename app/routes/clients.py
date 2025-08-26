from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.clients import Client as ClientBase, ClientCreate, ClientUpdate, ClientResponse as Response, GetResponse
from model.clients import Client as DBClient
from datetime import datetime, timezone

router = APIRouter()

@router.post("/clients", response_model=Response, status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        if not client.name or not client.email:
            return JSONResponse(status_code=400, content={"message": "Name and email are required."})
        existing_client = db.query(DBClient).filter(DBClient.email == client.email).first()
        if existing_client:
            return JSONResponse(status_code=400, content={"message": "Client with this email already exists."})
        
        now_iso = datetime.now(timezone.utc).isoformat()
        client.created_at = now_iso
        client.updated_at = now_iso

        new_client = DBClient(**client.model_dump())
        db.add(new_client)
        db.commit()
        db.refresh(new_client)

        return {
            "message": "Client created successfully.",
            "client": ClientBase.model_validate(new_client)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
       
@router.get("/clients/{client_id}", response_model=Response, status_code=200)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return {
        "message": "Client retrieved successfully.",
        "client": ClientBase.model_validate(client)
    }

@router.get("/clients", response_model=GetResponse, status_code=200)
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(DBClient).all()
    print(f"Retrieved {len(clients)} clients from the database.")
    return {
        "message": "All clients retrieved successfully.",
        "clients": [ClientBase.model_validate(client) for client in clients]
    }

@router.put("/clients/{client_id}", response_model=Response, status_code=200)
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    client_in_db = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not client_in_db:
        raise HTTPException(status_code=404, detail="Client not found")
    update_data = client.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(client_in_db, key, value)
    db.commit()
    db.refresh(client_in_db)
    return {
        "message": "Client updated successfully.",
        "client": ClientBase.model_validate(client_in_db)
    }

@router.delete("/clients/{client_id}", response_model=Response, status_code=200)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {
        "message": "Client deleted successfully.",
        "client": ClientBase.model_validate(client)
    }
