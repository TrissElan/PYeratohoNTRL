import MODULE.SystemModule as SM
import random as rd
import MODULE.CharacterModule as CM

SYSTEM = SM.System()

# 101 - 이동한다
def COM101(CHARA:CM.Character):
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]
    locations = {}
    for location in CHARA.CFLAG[11].LINK:
        locations[location.ID] = (location.NAME, None)
    if CHARA == MASTER:
        locations[1002] = ("취소", None)
        SYSTEM.input(locations, 25, 4, "left")
    else:
        SYSTEM.inputr(locations)
    RESULT = SYSTEM.RESULT
    if RESULT == 1002:
        return
    else:
        DESTINATION = SYSTEM.MAP[RESULT]

        if CHARA != MASTER and MASTER in CHARA.CFLAG[11].SPACE:
            SYSTEM.setText(4, f"{CHARA.NAME("은는")} {DESTINATION.NAME}으로 이동했다.\n")
        
        # 나중게 경로에 따라 작동하도록 만들어야 할텐데...
        CHARA.CFLAG[11].SPACE.remove(CHARA)
        CHARA.CFLAG[12] = CHARA.CFLAG[11]
        DESTINATION.SPACE.append(CHARA)
        CHARA.CFLAG[11] = DESTINATION

        if CHARA != MASTER and MASTER in CHARA.CFLAG[11].SPACE:
            SYSTEM.setText(4, f"{CHARA.NAME("이가")} {DESTINATION.NAME}에 왔다.\n")
        

# 102 - 대화한다
def COM102(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    if TARGET == None:
        return
    
    # EXP 증가

    # PARAM 증가

    # 호감도 증가

    # 커맨드 구상 출력 영역
    if CHARA not in MASTER.CFLAG[11].SPACE:
        return
    else:
        if CHARA == MASTER or CHARA.TARGET == MASTER:
            SYSTEM.setText(4, f"{CHARA.NAME("은는")} {TARGET.NAME("와과")} 가벼운 대화를 시작했다.\n")
        else:
            SYSTEM.setText(4, f"{CHARA.NAME("은는")} 자신이 아닌 {TARGET.NAME("와과")} 가벼운 대화를 시작했다...\n")
        if TARGET.CFLAG[20][CHARA.NAME()] <= 100:
            SYSTEM.setText(4, "별 관심이 없어 보인다...\n")
        elif TARGET.CFLAG[20][CHARA.NAME()] <= 200:
            SYSTEM.setText(4, "가끔씩 미소를 짓는데 너무나 눈부시다...\n")
        elif TARGET.CFLAG[20][CHARA.NAME()] <= 300:
            SYSTEM.setText(4, "날 바라보며 미소를 지어준다...\n")
        else:
            SYSTEM.setText(4, "나와 대화를 하는 것이 즐거운 듯 하다...\n") 

# 103 - 차를 탄다
def COM103(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    if TARGET == None:
        return

# 104 - 약을 탄다
def COM104(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    if TARGET == None:
        return

# 105 - 동행
def COM105(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    if TARGET == None:
        return

# 106 - 청소한다
def COM106(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    if TARGET == None:
        return

# 107 - 도와준다
def COM107(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    if TARGET == None:
        return

# 108 - 휴식한다
def COM108(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    if TARGET == None:
        return

# 109 - 화낸다
def COM109(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    if TARGET == None:
        return

# 110 - 사과한다
def COM110(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    if TARGET == None:
        return