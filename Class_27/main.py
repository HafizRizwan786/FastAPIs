from contextlib import asynccontextmanager
from time import perf_counter
from Class_27.core.exceptions import add_exception_handlers
from fastapi import  FastAPI,Request,Response
from scalar_fastapi import get_scalar_api_reference
from Class_27.database.session import create_db_tables
from Class_27.api.router import master_router
from Class_27.worker.tasks import add_log
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def life_span_handler(app: FastAPI):
    await create_db_tables()
    yield


app=FastAPI(lifespan=life_span_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origin=["http://localhost:5500"],
    allow_method=["*"]
)

app.include_router(master_router)

add_exception_handlers(app)


# Scalar Document
@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title="Scalar API"
    )
