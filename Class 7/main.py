from fastapi import FastAPI, HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from .schema import ShipmentRead,ShipmentCreate,ShipmentUpdate
from .JsonData import shipments,save

app=FastAPI()



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
@app.post('/shipment')
def submit_shipment(shipment: ShipmentCreate)-> dict[str,int]:
    
    new_id=max(shipments.keys())+1
    shipments[new_id]={
        'id':new_id,
        **shipment.model_dump(),
        "status": "placed"
    }
    save()
    return {"id" : new_id}




# Update Shipment Status
@app.patch('/shipment',response_model=ShipmentRead)
def patch_shipment(id: int,body: ShipmentUpdate):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    shipments[id].update(body.model_dump(exclude_none=True))
    save()
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
    save()
    return {"Detail": f"Shipment with id #{id} have been deleted!"}



# Scalar Document
@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )
