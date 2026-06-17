from fastapi import FastAPI, HTTPException ,status
from typing import Any
from scalar_fastapi import get_scalar_api_reference


app=FastAPI()

shipments = {
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
def submit_shipment(weight: float,data: dict[str,str])-> dict[str,int]:
    content=data['content']
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Weight can not be more than 25 kg"
        )
        
    new_id=max(shipments.keys())+1
    shipments[new_id]={
        "weight":weight,
        "content":content,
        "status": "placed"
    }
    
    return {"id" : new_id}

@app.get('/shipment/{field}')
def get_shipment_field(field: str,id: int) -> dict[str,Any]:
    return {
        field:shipments[id][field]
    }
    
    
@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )