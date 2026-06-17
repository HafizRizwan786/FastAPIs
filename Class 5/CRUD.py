from fastapi import FastAPI, HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app=FastAPI()

shipments={
    12301 : {
        'weight':1.2,
        'content' : 'Tables',
        'status' : 'In Transit'
    },
    12302 : {
        'weight':1.3,
        'content' : 'Books',
        'status' : 'In Transit'
    },
    12303 : {
        'weight':1.4,
        'content' : 'Chuss',
        'status' : 'In Transit'
    },
    12304 : {
        'weight':1.5,
        'content' : 'ABCE',
        'status' : 'In Transit'
    },
}

# Get Method
@app.get('/shipment')
def get_shipment(id: int)->dict[str,Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Given id does not exist'
        )
    return shipments[id]


# Post Method
@app.post('/shipment')
def submit_shipment(content: str,weight: float) -> dict[str, int]:
    if weight>50:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Weight can not be more than 50'
        )
        
    new_id=max(shipments.keys()) + 1
    shipments[new_id]={
        'weight':weight,
        'content':content,
        'status':'placed'
    }
    
    return {'id':new_id}


# Update Shipment (Update All Fields)
@app.put('/shipment')
def update_shipment(id: int,content: str,weight: float,status: str) ->dict[str,Any]:
    shipments[id]={
        'weight':weight,
        'content':content,
        'status':status
    }
    
    return shipments[id]


"""
# Update Shipment (Update Few Fields)  --- Not Good Method
@app.patch('/shipment')
def patch_shipment(
    id: int,
    content: str | None =None,
    weight: float | None =None,
    status: str | None =None
    ) ->dict[str,Any]:
    
    shipment=shipments[id]
    
    if content:
        shipment['content']=content
    if weight:
        shipment['weight']=weight
    if status:
        shipment['status']=status
    
    shipments[id]=shipment
    return shipment
"""



# Update Shipment (Update Few Fields)  --- Good Method
@app.patch('/shipment')
def patch_shipment(id: int,body: dict[str,Any]) ->dict[str,Any]:
    
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