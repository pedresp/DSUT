class Drone:
    def __init__(self, id:str, speed:float =10, acc:float =10) -> None:
        self.id = id
        self.speed = speed
        self.acc = acc