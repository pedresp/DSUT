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

    def __str__(self) -> str:
        return f"<id = {self.id}, speed = {self.speed}, acc = {self.acc}, tof = {self.tof}, sweep_width = {self.sweep_width}, coord = ({self.coordx}, {self.coordy})>"
    
    def __repr__(self) -> str:
        return self.__str__()
    
def dronson(drone: Drone):
    if (isinstance(drone, Drone)):
        return { "id": drone.id, "speed": drone.speed, "acc": drone.acc, "tof": drone.tof, "sweep_width": drone.sweep_width,\
                 "coordx": drone.coordx, "coordy": drone.coordy}
    raise TypeError("obj cannot be serialized")

def jsondrone(drones_bag: dict):
    for key, value in drones_bag.items():
        drones_bag[key] = Drone(value['id'], value['speed'], value['acc'], \
                                value['tof'], value['sweep_width'], value['coordx'], value['coordy']) 