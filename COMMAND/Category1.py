import MODULE.SystemModule as SM
import random as rd
import MODULE.CharacterModule as CM

SYSTEM = SM.System()

def COM001(CHARA:CM.Character):
    global SYSTEM
    locations = {}
    for location in CHARA.CFLAG[11].LINK:
        locations[location.ID] = location.NAME
    if CHARA == SYSTEM.CHARACTERS[SYSTEM.MASTER]:
        SYSTEM.input(locations, 10, 5)
        RESULT = SYSTEM.RESULT
    else:
        RESULT = rd.choice(list(locations.keys()))
    CHARA.CFLAG[11].SPACE.remove(CHARA)
    CHARA.CFLAG[12] = CHARA.CFLAG[11]
    SYSTEM.MAP[RESULT].SPACE.append(CHARA)
    CHARA.CFLAG[11] = SYSTEM.MAP[RESULT]
    # 나중게 경로에 따라 작동하도록 만들어야 할텐데...

def COM006(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    
    # EXP 증가

    # PARAM 증가

    # 호감도 증가

    # 커맨드 구상 출력 영역
    SYSTEM.setText(4, f"{CHARA.NAME("은는")} {TARGET.NAME("와과")} 가벼운 대화를 시작했다.\n")
    if TARGET.CFLAG[20][CHARA.NAME()] <= 100:
        SYSTEM.setText(4, "별 관심이 없어 보인다...\n")
    elif TARGET.CFLAG[20][CHARA.NAME()] <= 200:
        SYSTEM.setText(4, "가끔씩 미소를 짓는데 너무나 눈부시다...\n")
    elif TARGET.CFLAG[20][CHARA.NAME()] <= 300:
        SYSTEM.setText(4, "날 바라보며 빛나는 미소를 지어준다...\n")
    else:
        SYSTEM.setText(4, "나와 대화를 하는 것이 즐거운 듯 하다...\n")
    
