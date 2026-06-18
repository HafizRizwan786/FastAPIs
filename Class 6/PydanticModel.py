from fastapi import FastAPI, HTTPException ,status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from pydantic import BaseModel

app=FastAPI()

class Shipment(BaseModel):
    weight: float
    content: str
    dest: int

shipments={
    12301 : {
        'weight':1.2,
        'content' : 'Tables',
        'status' : 'In Transit',
        'destination' : 11234
    },
    12302 : {
        'weight':1.3,
        'content' : 'Books',
        'status' : 'In Transit',
        'destination' : 11235
    },
    12303 : {
        'weight':1.4,
        'content' : 'Chuss',
        'status' : 'In Transit',
        'destination' : 11236
    },
    12304 : {
        'weight':1.5,
        'content' : 'ABCE',
        'status' : 'In Transit',
        'destination' : 11237
    },
}



@app.get('/shipment')
def get_shipment(id: int | None = None) -> dict[str,Any]:
    if not id:
        id=max(shipments.keys())
        return shipments[id]
    
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist"
        )
        
    return shipments[id]
    


@app.post('/shipment')
def submit_shipment(shipment: Shipment)-> dict[str,int]:
    
    if shipment.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Weight can not be more than 25 kg"
        )
        
    new_id=max(shipments.keys())+1
    shipments[new_id]={
        "weight":shipment.weight,
        "content":shipment.content,
        "destination": shipment.dest,
        "status": "placed"
    }
    
    return {"id" : new_id}



@app.get('/scalar')
def get_scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )