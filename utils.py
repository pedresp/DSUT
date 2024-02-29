def next_drone(dicctionary: dict) -> str:
    count = 0
    candidate_name = "drone_" + str(count)
    
    while(hasKey(dicctionary, candidate_name)):
        count = count+1
        candidate_name = "drone_" + str(count)

    return candidate_name

def hasKey(dictionary: dict, key:str) -> bool:
    try:
        dictionary[key]
        return True
    except:
        return False