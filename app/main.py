from fastapi import FastAPI
from routes import client, product, order

app = FastAPI()

# Inclusion des routes avec préfixes
app.include_router(client.router, prefix="/clients", tags=["Clients"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API de PayeTonKawa"}
