from typing import Callable, Any

routes: dict[str, Callable[..., Any]] = {}

def route(path: str):
    def register_route(func):
        routes[path] = func
        return func
    return register_route


@route('/home')
def home():
    return "Welcome to Home Page"

# Flow of Working
# decorator=route('/home')  --> return register_route
# another_func=decorator(home) -->  routes={'/home': home} then  return home


request = ''

while request != 'quit':
    request = input("> ")

    if request == 'quit':
        break
    
    if request in routes:
        print(routes[request]())
    else:
        print("404 Not Found")