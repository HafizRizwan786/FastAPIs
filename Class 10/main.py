from contextlib import asynccontextmanager
from fastapi import  FastAPI
from scalar_fastapi import get_scalar_api_reference
from database.session import create_db_tables
from api.router import router

@asynccontextmanager
async def life_span_handler(app: FastAPI):
    await create_db_tables()
    yield


app=FastAPI(lifespan=life_span_handler)

app.include_router(router)


# Scalar Document
@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )
