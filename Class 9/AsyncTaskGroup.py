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
    
    async with asyncio.TaskGroup() as taskgroup:
        tasks=[
            taskgroup.create_task(end_point(route))
            for route in tests
        ]
        
        print(await tasks[0])
    
    end=time.perf_counter()
    print(f"Time taken : {end-start:.2f}")
    
asyncio.run(
    server()
)
