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