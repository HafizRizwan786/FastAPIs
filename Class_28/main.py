from contextlib import asynccontextmanager
from Class_28.core.exceptions import add_exception_handlers
from fastapi import  FastAPI
from scalar_fastapi import get_scalar_api_reference
from Class_28.database.session import create_db_tables
from Class_28.api.router import master_router
from Class_28.api.tag import APITag


@asynccontextmanager
async def life_span_handler(app: FastAPI):
    await create_db_tables()
    yield


description="""
    Delivery Management System for sellers and delivery agents
    ### Seller
    - Submit shipment effortlessly
    - Share tracking link with customer
    
    ### Delivery Agent
    - Auto accept shipment
    - Track and update shipment status
    - Email and SMS notification
"""


app=FastAPI(
    lifespan=life_span_handler,
    title="FastShip",
    description=description,
    docs_url=None,
    redoc_url=None,
    version="0.1.0",
    terms_of_service="http://fastship.com/terms/",
    contact={
        "name" : "Fastship Support",
        "url" : "https://fastship.com/support",
        "email" : "support@fastship.com"
    },
    openapi_tags=[
        {
            "name" : APITag.SHIPMENT,
            "description" : "Operation related to shipment"
        },
        {
            "name" : APITag.SELLER,
            "description" : "Operation related to seller"
        },
        {
            "name" : APITag.PARTNER,
            "description" : "Operation related to delivery partner"
        },
    ]
)

app.include_router(master_router)

add_exception_handlers(app)

# Scalar Document
@app.get("/docs")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )
