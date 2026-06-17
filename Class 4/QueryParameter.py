from fastapi import FastAPI
from typing import Any

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
        return {
            'error' : 'Shipment not found'
        }
    return shipments[id]
    
