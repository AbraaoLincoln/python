from threading import Thread

def background(f):
    def inner(*args):
        print("Starting thread")
        thread = Thread(target=f, args=args)
        thread.start()
    
    return inner

class Service:
    def execute(self):
        self.__register("x")
        self.__register2("x", 1)
    
    @background
    def __register(self, x: str) -> None:
        print("Registring", x)
    
    @background
    def __register2(self, x: str, y: int) -> None:
        print("Registring", x, y)

service = Service()
service.execute()