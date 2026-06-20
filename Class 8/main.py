from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import  FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .database.models import Shipment,ShipmentStatus
from .database.session import SessionDep, create_db_tables
from .SchemaWithDB import ShipmentCreate, ShipmentRead, ShipmentUpdate


@asynccontextmanager
async def life_span_handler(app: FastAPI):
    create_db_tables()
    yield


app=FastAPI(lifespan=life_span_handler)


# Get Method
@app.get('/shipment',response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    shipment=session.get(Shipment,id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Given id does not exist'
        )
    return shipment


# Post Method
@app.post('/shipment')
def submit_shipment(shipment: ShipmentCreate,session:SessionDep)-> dict[str,int]:
    new_shipment=Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id" : new_shipment.id}


# Update Shipment Status
@app.patch('/shipment',response_model=ShipmentRead)
def patch_shipment(id: int,shipment_update: ShipmentUpdate, session: SessionDep):
    update=shipment_update.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not update is provided"
        )
    
    shipment=session.get(Shipment,id)
    shipment.sqlmodel_update(shipment_update)
    
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment



# Delete Shipment
@app.delete('/shipment')
def del_shipment(id: int,session: SessionDep) ->dict[str,str]:
    session.delete(
        session.get(Shipment,id)
    )
    session.commit()
    return {"Detail": f"Shipment with id #{id} have been deleted!"}


# Scalar Document
@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )
