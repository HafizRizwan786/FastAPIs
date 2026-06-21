import time
from rich import print

def end_point(route):
    print(f">> handling {route}")
    time.sleep(1)
    print(f"<< response {route}")
    

def server():
    tests=(
        "Get/Shipment?id=1",
        "Patch/Shipment?id=4",
        "Get/Shipment?id=3"
    )
    
    start=time.perf_counter()
    
    for route in tests:
        end_point(route)
    
    end=time.perf_counter()
    print(f"Time taken : {end-start:.2f}")
    

server()