from fastapi import FastAPI, HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from .schema3 import ShipmentRead,ShipmentCreate,ShipmentUpdate

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
@app.get('/shipment',response_model=ShipmentRead)
def get_shipment(id: int):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Given id does not exist'
        )
    return shipments[id]


# Post Method
@app.post('/shipment',response_model=None) # ab read validation check nhi kry ga
def submit_shipment(shipment: ShipmentCreate)-> dict[str,int]:
    
    new_id=max(shipments.keys())+1
    shipments[new_id]={
        **shipment.model_dump(),
        "status": "placed"
    }
    
    return {"id" : new_id}




# Update Shipment 
@app.patch('/shipment',response_model=ShipmentRead)
def patch_shipment(id: int,body: ShipmentUpdate):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    shipments[id].update(body.model_dump(exclude_none=True))
    return shipments[id]



# Delete Shipment
@app.delete('/shipment')
def del_shipment(id: int) ->dict[str,str]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    shipments.pop(id)
    return {"Detail": f"Shipment with id #{id} have been deleted!"}



# Scalar Document
@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )
