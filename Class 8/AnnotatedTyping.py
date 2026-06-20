from typing import Annotated

temp: Annotated[float,"celsius"]=23.2

celsius=Annotated[float,"celsius"]
city_temp: celsius=34.2
print(celsius.__origin__)
print(celsius.__metadata__[0])