from fastapi import FastAPI
from contextlib import asynccontextmanager
from rich import print,panel
@asynccontextmanager
async def life_span_handler(app: FastAPI):
    print(panel.Panel("server is starting.....",border_style="green"))
    yield
    print(panel.Panel("...Server is closing",border_style="red"))


app=FastAPI(lifespan=life_span_handler)

@app.get('/')
def root():
    return {"detail":"Server Life span learning"}