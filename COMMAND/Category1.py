import MODULE.SystemModule as SM
import random as rd

SYSTEM = SM.System()

def COM001(chara:int):
    global SYSTEM
    player = SYSTEM.CHARACTERS[chara]
    locations = {}
    for location in player.CFLAG[11].LINK:
        locations[location.ID] = location.NAME
    if chara == SYSTEM.MASTER:
        RESULT = SYSTEM.input(locations)
    else:
        RESULT = rd.choice(list(locations.keys()))
    player.CFLAG[11].SPACE.remove(player)
    player.CFLAG[12] = player.CFLAG[11]
    SYSTEM.MAP[RESULT].SPACE.append(player)
    player.CFLAG[11] = SYSTEM.MAP[RESULT]
    print(player.NAME + " : " + player.CFLAG[11].NAME + "으로 이동함")

def COM002(chara:int):
    global SYSTEM
    SYSTEM.delText(4)
    player = SYSTEM.CHARACTERS[chara]
    SYSTEM.setText(4, f"{player}은 {player.TARGET}과 가벼운 대화를 시작했다.\n")
    if player.TARGET.CFLAG[20][player] <= 100:
        SYSTEM.setText(4, "별 관심이 없어 보인다...\n")
    elif player.TARGET.CFLAG[20][player] <= 200:
        SYSTEM.setText(4, "가끔씩 미소를 짓는데 너무나 눈부시다...\n")
    player.EXP[96] += 1
    player.TARGET.EXP[96] += 1

    SYSTEM.DISPLAY.textArea[4].bind("<Button-1>", lambda e: SYSTEM.delText(4))
