'''Class to represent a drone and its characteristics'''
class Drone:
    def __init__(self, id:str, speed:float =10, acc:float =10, tof:float =50.0, sweep_width:float =20.0, coordx:float =-200, coordy:float =0.0 ) -> None:
        self.id = id
        self.speed = speed
        self.acc = acc
        self.tof = tof
        self.sweep_width = sweep_width
        self.coordx = coordx
        self.coordy = coordy