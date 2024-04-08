'''Method that calculates the next standard name for a new drone'''
def next_drone(dicctionary: dict) -> str:
    count = 0
    candidate_name = "drone_" + str(count)
    
    while(hasKey(dicctionary, candidate_name)):
        count = count+1
        candidate_name = "drone_" + str(count)

    return candidate_name

'''Method to check if a dictionary has a key'''
def hasKey(dictionary: dict, key:str) -> bool:
    try:
        dictionary[key]
        return True
    except:
        return False
    
def read_coords(coord: str):
    coord_list = coord.split(sep="\n")
    if not len(coord_list):
        return None

    solut_list = []

    for elem in coord_list:
        pair = elem.split(sep=",")
        if not len(pair) == 2:
            return None
        solut_list.append([float(pair[0]), float(pair[1])])
    
    return solut_list