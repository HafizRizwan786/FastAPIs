# Simple Variables with Type Hinting
text: str="Hafiz Rizwan"
part: int=3
temp: float= 2.3
number: int | float = 3


# List with Type Hinting
lst: list[int] = [1,2,3,4,5]

# tuple with Type Hinting
tup: tuple[str, int] = ("Hafiz", 3)
tp: tuple[int, ...] = (1,2,3,4,5)

# Dictionary with Type Hinting
from typing import Any

dct: dict[str, int | float] = {
    "Hafiz": 3,
    "Rizwan": 2.3
    }

dct1: dict[str, Any] = {
    "Hafiz": 3,
    "Rizwan": 2.3,
    "content" : "hello world",
    }


# Function with Type Hinting
def root(num: int,exp: float | None = .5) -> float:
    if exp is None:
        exp = 0.5

    return pow(num,exp)

rt=root(2,None)
print(rt)



# Class with Type Hinting
class Person:
    def __init__(self, name, age):
        self.name=name
        self.age=age
        
p=Person("Hafiz",20)
t: tuple[Person,int]=(p,2)