import MODULE.SystemModule as SM
import random as rd

SYSTEM = SM.System()

def COM001(chara:int):
    global SYSTEM
    player = SYSTEM.CHARACTERS[chara]
    locations = {}
    for location in player.CFLAG[11].LINK:
        locations[location.ID] = location.NAME
    if chara == 0:
        RESULT = SYSTEM.input(locations)
    else:
        RESULT = rd.choice(list(locations.keys()))
    player.CFLAG[11].SPACE.remove(player)
    player.CFLAG[12] = player.CFLAG[11]
    SYSTEM.MAP[RESULT].SPACE.append(player)
    player.CFLAG[11] = SYSTEM.MAP[RESULT]
    print(player.NAME + " : " + player.CFLAG[11].NAME + "으로 이동함")