import MODULE.SystemModule as SM
import random as rd
import MODULE.CharacterModule as CM

SYSTEM = SM.System()

def COM000(chara:CM.Character):
    global SYSTEM
    locations = {}
    for location in chara.CFLAG[11].LINK:
        locations[location.ID] = location.NAME
    if chara == SYSTEM.CHARACTERS[SYSTEM.MASTER]:
        RESULT = SYSTEM.input(locations)
    else:
        RESULT = rd.choice(list(locations.keys()))
    chara.CFLAG[11].SPACE.remove(chara)
    chara.CFLAG[12] = chara.CFLAG[11]
    SYSTEM.MAP[RESULT].SPACE.append(chara)
    chara.CFLAG[11] = SYSTEM.MAP[RESULT]

def COM007(chara:CM.Character):
    global SYSTEM
    SYSTEM.setText(4, f"{chara.NAME("은는")} {chara.TARGET.NAME("와과")} 가벼운 대화를 시작했다.\n")
    if chara.TARGET.CFLAG[20][chara] <= 100:
        SYSTEM.setText(4, "별 관심이 없어 보인다...\n")
    elif chara.TARGET.CFLAG[20][chara] <= 200:
        SYSTEM.setText(4, "가끔씩 미소를 짓는데 너무나 눈부시다...\n")
    chara.EXP[96] += 1
    chara.TARGET.EXP[96] += 1
