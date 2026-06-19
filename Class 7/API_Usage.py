from fastapi import FastAPI, HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from .SchemaWithDB import ShipmentRead,ShipmentCreate,ShipmentUpdate
from .DataBase2 import Database

app=FastAPI()

db=Database()


# Get Method
@app.get('/shipment',response_model=ShipmentRead)
def get_shipment(id: int):
    shipment=db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Given id does not exist'
        )
    return shipment


# Post Method
@app.post('/shipment')
def submit_shipment(shipment: ShipmentCreate)-> dict[str,int]:
    new_id=db.create(shipment)
    return {"id" : new_id}


# Update Shipment Status
@app.patch('/shipment',response_model=ShipmentRead)
def patch_shipment(id: int,body: ShipmentUpdate):
    shipment=db.update(id,body)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
        
    return shipment



# Delete Shipment
@app.delete('/shipment')
def del_shipment(id: int) ->dict[str,str]:
    db.delete(id)
    return {"Detail": f"Shipment with id #{id} have been deleted!"}


# Scalar Document
@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )
