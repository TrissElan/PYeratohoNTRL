import MODULE.SystemModule as SM
import MODULE.CharacterModule as CM

SYSTEM = SM.System()

# 모든 커맨드는 매개변수로 특정 커맨드를 실행하는 캐릭터를 받음


# 101 - 이동한다
def COM101(CHARA: CM.Character):
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
    # 그렇지 않을 경우 정상 실행으로 간주함
    else:
        SYSTEM.RESULT = 1000

    # 마스터와 같은 방에 있을 때 떠나는 경우의 배경텍스트 출력
    if CHARA is not MASTER and MASTER in CHARA.CFLAG[11].SPACE:
        SYSTEM.setText(4, CHARA % "는 " + SYSTEM.MAP[RESULT] % "으로 이동했다.\n")

    # 실제 커맨드 실행구간 - 나중에 경로에 따라 작동하도록 만들어야 할텐데...
    DESTINATION = SYSTEM.MAP[RESULT]
    CHARA.CFLAG[11].SPACE.remove(CHARA)
    CHARA.CFLAG[12] = CHARA.CFLAG[11]
    DESTINATION.SPACE.append(CHARA)
    CHARA.CFLAG[11] = DESTINATION

    # 이동한 방이 마스터와 같은 방일 경우의 배경텍스트 출력
    if CHARA is not MASTER and MASTER in CHARA.CFLAG[11].SPACE:
        SYSTEM.setText(4, CHARA % "가 " + DESTINATION % "에 왔다.\n")


# 102 - 대화한다
def COM102(MASTER: CM.Character):
    global SYSTEM
    PLAYER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    TARGET = MASTER.TARGET

    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    # 커맨드 정상실행
    else:
        SYSTEM.RESULT = 1000

    # EXP 증가
    MASTER.EXP[9][1] += 1
    TARGET.EXP[9][1] += 1

    # PARAM 증감
    # - 커맨드를 실행하는 캐릭터
    MASTER.updateBASE1(VIT=-10, RAT=-1, FTG=1)
    MASTER.updateBASE2()
    MASTER.updateBASE3()
    MASTER.updatePLSR()
    MASTER.updateMOOD(TARGET.NAME(index=0))

    # - 커맨드의 대상 캐릭터
    TARGET.updateBASE1(VIT=-10, RAT=-1, FTG=1)
    TARGET.updateBASE2()
    TARGET.updateBASE3()
    TARGET.updatePLSR()
    TARGET.updateMOOD(MASTER.NAME(index=0))

    # 호감도 증가

    # 커맨드 구상 출력 영역
    if MASTER not in MASTER.CFLAG[11].SPACE:
        return
    else:
        if MASTER == PLAYER or MASTER.TARGET == PLAYER:
            SYSTEM.setText(4, MASTER % "는 " + TARGET % "과 가벼운 대화를 시작했다.\n")
        else:
            SYSTEM.setText(
                4,
                MASTER % "는 자신이 아닌 " + TARGET % "과 가벼운 대화를 시작했다...\n",
            )
        if TARGET.CFLAG[20][MASTER.NAME()] <= 100:
            SYSTEM.setText(4, "별 관심이 없어 보인다...\n")
        elif TARGET.CFLAG[20][MASTER.NAME()] <= 200:
            SYSTEM.setText(4, "가끔씩 미소를 짓는데 너무나 눈부시다...\n")
        elif TARGET.CFLAG[20][MASTER.NAME()] <= 300:
            SYSTEM.setText(4, "미소를 지어준다...\n")
        else:
            SYSTEM.setText(4, "환한 미소를 만들고 있다...\n")


# 103 - 차를 탄다
def COM103(CHARA: CM.Character):
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
def COM104(CHARA: CM.Character):
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
def COM105(CHARA: CM.Character):
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
def COM106(CHARA: CM.Character):
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
def COM107(CHARA: CM.Character):
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
def COM108(CHARA: CM.Character):
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
def COM109(CHARA: CM.Character):
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
def COM110(CHARA: CM.Character):
    global SYSTEM
    TARGET = CHARA.TARGET

    # 커맨드 취소구간
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return

    # 실제 커맨드 실행구간

    # 정상실행시에 준비되는 값 - phase0부터 시작함을 의미함
    SYSTEM.RESULT = 1000
