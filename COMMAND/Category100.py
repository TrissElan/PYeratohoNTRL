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
        locations[location.ID] = (location.NAME(), None)
    if CHARA == MASTER:
        locations[1002] = ("취소", None)
        SYSTEM.input(locations, 25, 4, "left")
    else:
        SYSTEM.inputr(locations)
    RESULT = SYSTEM.RESULT

    # 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    if RESULT == 1002:
        return

    # 마스터와 같은 방에 있을 때 떠나는 경우의 배경텍스트 출력
    if CHARA is not MASTER and MASTER in CHARA.CFLAG[11].SPACE:
        SYSTEM.setText(4, (CHARA + "는 ") + (SYSTEM.MAP[RESULT] + "으로 이동했다.\n") )

    # 실제 커맨드 실행구간 - 나중에 경로에 따라 작동하도록 만들어야 할텐데...
    DESTINATION = SYSTEM.MAP[RESULT]
    CHARA.CFLAG[11].SPACE.remove(CHARA)
    CHARA.CFLAG[12] = CHARA.CFLAG[11]
    DESTINATION.SPACE.append(CHARA)
    CHARA.CFLAG[11] = DESTINATION

    # 이동한 방이 마스터와 같은 방일 경우의 배경텍스트 출력
    if CHARA is not MASTER and MASTER in CHARA.CFLAG[11].SPACE:
        SYSTEM.setText(4, (CHARA + "가 ") + (DESTINATION + "에 왔다.\n") )
        
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000

# 102 - 대화한다
def COM102(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    
    # EXP 증가

    # PARAM 증가

    # 호감도 증가

    # 커맨드 구상 출력 영역
    if CHARA not in MASTER.CFLAG[11].SPACE:
        return
    else:
        if CHARA == MASTER or CHARA.TARGET == MASTER:
            SYSTEM.setText(4, (CHARA + "는 ") + (TARGET + "과 가벼운 대화를 시작했다.\n") )
        else:
            SYSTEM.setText(4, (CHARA + "는 자신이 아닌 ") + (TARGET + "과 가벼운 대화를 시작했다...\n") )
        if TARGET.CFLAG[20][CHARA.NAME()] <= 100:
            SYSTEM.setText(4, "별 관심이 없어 보인다...\n")
        elif TARGET.CFLAG[20][CHARA.NAME()] <= 200:
            SYSTEM.setText(4, "가끔씩 미소를 짓는데 너무나 눈부시다...\n")
        elif TARGET.CFLAG[20][CHARA.NAME()] <= 300:
            SYSTEM.setText(4, "날 바라보며 미소를 지어준다...\n")
        else:
            SYSTEM.setText(4, "나와 대화를 하는 것이 즐거운 듯 하다...\n")
    
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000

# 103 - 차를 탄다
def COM103(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    
    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    
    # 실제 커맨드 실행구간
    
    # 실제 커맨드 실행구간
    
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000

# 104 - 약을 탄다
def COM104(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    
    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    
    # 실제 커맨드 실행구간
    
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000

# 105 - 동행
def COM105(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    
    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    
    # 실제 커맨드 실행구간
    
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000

# 106 - 청소한다
def COM106(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    
    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    
    # 실제 커맨드 실행구간
    
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000

# 107 - 도와준다
def COM107(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    
    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    
    # 실제 커맨드 실행구간
    
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000

# 108 - 휴식한다
def COM108(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    
    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    
    # 실제 커맨드 실행구간
    
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000

# 109 - 화낸다
def COM109(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    
    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    
    # 실제 커맨드 실행구간
    
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000

# 110 - 사과한다
def COM110(CHARA:CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET
    
    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    
    # 실제 커맨드 실행구간
    
    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000