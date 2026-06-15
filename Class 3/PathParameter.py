from fastapi import FastAPI
from typing import Any

app = FastAPI()

@app.get('/shipment/{id}')
def get_shipment(id: int) -> dict[str,Any]:
    return {
        'id' : id,
        'weight':1.2,
        'content' : 'Wooden Blocks',
        'status' : 'In Transit'
    }
    
