from fastapi import FastAPI, HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from .schemas import Shipment,ShipmentStatus

app=FastAPI()

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

# Get Method
@app.get('/shipment',response_model=Shipment)
def get_shipment(id: int):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Given id does not exist'
        )
    return shipments[id]


# Post Method
@app.post('/shipment')
def submit_shipment(shipment: Shipment)-> dict[str,int]:
    
    new_id=max(shipments.keys())+1
    shipments[new_id]={
        "weight":shipment.weight,
        "content":shipment.content,
        "destination": shipment.dest,
        "status": "placed"
    }
    
    return {"id" : new_id}




# Update Shipment Status
@app.patch('/shipment')
def patch_shipment(id: int,body: dict[str,ShipmentStatus]) ->dict[str,Any]:
    
    shipment=shipments[id]
    shipment.update(body)
    shipments[id]=shipment
    return shipment



# Delete Shipment
@app.delete('/shipment')
def del_shipment(id: int) ->dict[str,str]:
    shipments.pop(id)
    return {"Detail": f"Shipment with id #{id} have been deleted!"}



# Scalar Document
@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )