# Simple Decorator
def fence(func):
    def wrapper():
        print("+" * 10 )
        func()
        print("+" * 10 )
    return wrapper

@fence
def log():
    print("Decorated!")
    
log()

# Flow of Working
# another_func=fence(log)  --> return wrapper
# another_func()



# Simple Decorator Without Wrapper
def fence1(func):
    print("!" * 10 )
    func()
    print("!" * 10 )
    

@fence1
def log1():
    print("Decorated!")

# Flow of Working
# another_func=fence(log)




# Decorator with Parameter
def custom_fence(fen: str = '+'):
    def add_fence(func):
        def wrapper(text: str):
            print(fen * len(text))
            func(text)
            print(fen * len(text))
        return wrapper
    return add_fence


@custom_fence('%')
def log2(text: str):
    print(text)

log2("Hafiz")

# Flow of Working
# decorator= custom_fence('%')  --> return add_fence
# another_func=decorator(log2) --> return wrapper
# another_func("Hafiz") --> print %%%%%, Hafiz, %%%%%


# Decorator with Multiple Parameters
from typing import Callable, Any

def decorator(func: Callable[[Any], Any]) -> Callable[..., Any]:
    pass

# Callable ye bata ta ha ky function call ho ga or phela parameter jo list ha wo inputs ka ha or dusra return ka