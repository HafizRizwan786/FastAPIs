import time
from rich import print
import asyncio

async def end_point(route):
    print(f">> handling {route}")
    await asyncio.sleep(1)
    print(f"<< response {route}")
    return route
    

async def server():
    tests=(
        "Get/Shipment?id=1",
        "Patch/Shipment?id=4",
        "Get/Shipment?id=3"
    )
    
    start=time.perf_counter()
    
    for route in tests:
        result=await end_point(route)
        print(f"Result back: {result}")
    
    end=time.perf_counter()
    print(f"Time taken : {end-start:.2f}")
    
asyncio.run(
    server()
)
