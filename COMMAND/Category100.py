import MODULE.SystemModule as SM
import MODULE.CharacterModule as CM
from MODULE.MapModule import Node


"""
# 모든 커맨드는 매개변수로 특정 커맨드를 실행하는 캐릭터를 받음
# 아래는 커맨드 함수의 양식
def TEMPLATE000(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if MASTER == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력
"""

# 커맨드 클래스 : 캐릭터 클래스 객체에 커맨드를 추가하여 사용할 수 있도록 만드는 단순한 캡슐화방식
class CommandSystem1:
    def __init__(self, character: CM.Character, system: SM.System = SM.System()):
        self.__player = character
        self.__system = system
        self.__master = system.CHARACTERS[system.MASTER]

    @property
    def player(self):
        return self.__player

    @property
    def system(self):
        return self.__system

    @property
    def master(self):
        return self.__master

    # 001 - 이동한다
    def COM001(self):
        # 변수준비1 : 필요한 변수를 준비함
        locations = {}
        for location in self.player.currL.link:
            locations[location.ID] = (location.NAME(), None)
        if self.player == self.master:
            locations[1002] = ("취소", None)
            self.system.input(locations, 25, 4, "left")
        else:
            self.system.inputr(locations)
            RESULT = self.system.RESULT
        # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
        # 먼저 취소되는 사유를 작성함 - 오름차순으로
        if RESULT == 1002:
            return
        # 마지막에 정상 실행을 작성함
        else:
            SYSTEM.RESULT = 1000

        # 실제 커맨드 실행
        beforeHere = (
            self.player is not self.master
            and self.master in self.player.currL.space
        )  # 마스터와 이동전 같은 방인지 여부
        DESTINATION:Node = SYSTEM.MAP[RESULT]
        self.player.currL.space.remove(self.player)
        self.player.pastL = self.player.currL
        DESTINATION.space.append(self.player)
        self.player.currL = DESTINATION
        afterHere = (
            self.player is not self.master
            and self.master in self.player.currL.space
        )  # 마스터와 이동후 같은 방인지 여부

        # 커맨드 실행에 따른 EXP 증가
        # - 커맨드 수행 캐릭터
        # - 커맨드 대상 캐릭터

        # 커맨드 실행에 따른 PARAM 증가
        # - 커맨드 수행 캐릭터
        # - 커맨드 대상 캐릭터

        # 커맨드에 따른 호감도 증가
        # - 커맨드 수행 캐릭터
        # - 커맨드 대상 캐릭터

        # 커맨드 자체 대사 출력
        if beforeHere:
            SYSTEM.setText(
                4, self.player % "는 " + SYSTEM.MAP[RESULT] % "으로 이동했다.\n"
            )
        if afterHere:
            SYSTEM.setText(4, self.player % "가 " + DESTINATION % "에 왔다.\n")


SYSTEM = SM.System()


# 101 - 이동한다
def COM101(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수
    locations = {}
    for location in PLAYER.currL.link:
        locations[location.ID] = (location.NAME(), None)
    if PLAYER == MASTER:
        locations[1002] = ("취소", None)
        SYSTEM.input(locations, 25, 4, "left")
    else:
        SYSTEM.inputr(locations)
    RESULT = SYSTEM.RESULT

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if RESULT == 1002:
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행
    beforeHere = (
        PLAYER is not MASTER and MASTER in PLAYER.currL.space
    )  # 마스터와 이동전 같은 방인지 여부
    DESTINATION = SYSTEM.MAP[RESULT]
    PLAYER.currL.space.remove(PLAYER)
    PLAYER.pastL = PLAYER.currL
    DESTINATION.space.append(PLAYER)
    PLAYER.currL = DESTINATION
    afterHere = (
        PLAYER is not MASTER and MASTER in PLAYER.currL.space
    )  # 마스터와 이동후 같은 방인지 여부

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력
    if beforeHere:
        SYSTEM.setText(4, PLAYER % "는 " + SYSTEM.MAP[RESULT] % "으로 이동했다.\n")
    if afterHere:
        SYSTEM.setText(4, PLAYER % "가 " + DESTINATION % "에 왔다.\n")


# 102 - 대화한다
def COM102(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수
    TARGET = PLAYER.TARGET

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if TARGET == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    PLAYER.EXP[9][1] += 1
    # - 커맨드 대상 캐릭터
    TARGET.EXP[9][1] += 1

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    PLAYER.updateBASE1(VIT=-10, RAT=-1, FTG=1)
    PLAYER.updateBASE2()
    PLAYER.updateBASE3()
    PLAYER.updatePLSR()
    PLAYER.updateMOOD(TARGET.NAME(index=0))

    # - 커맨드 대상 캐릭터
    TARGET.updateBASE1(VIT=-10, RAT=-1, FTG=1)
    TARGET.updateBASE2()
    TARGET.updateBASE3()
    TARGET.updatePLSR()
    TARGET.updateMOOD(PLAYER.NAME(index=0))

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력
    if PLAYER not in MASTER.currL.space:
        return
    else:
        if MASTER == PLAYER or MASTER.TARGET == PLAYER:
            SYSTEM.setText(4, PLAYER % "는 " + TARGET % "과 가벼운 대화를 시작했다.\n")
        else:
            SYSTEM.setText(
                4,
                PLAYER % "는 자신이 아닌 " + TARGET % "과 가벼운 대화를 시작했다...\n",
            )

        if TARGET.attra[PLAYER.NAME(index=0)] <= 100:
            SYSTEM.setText(4, "별 관심이 없어 보인다...\n")
        elif TARGET.attra[PLAYER.NAME(index=0)] <= 200:
            SYSTEM.setText(4, "가끔씩 미소를 짓는데 너무나 눈부시다...\n")
        elif TARGET.attra[PLAYER.NAME(index=0)] <= 300:
            SYSTEM.setText(4, "미소를 지어준다...\n")
        else:
            SYSTEM.setText(4, "환한 미소를 만들고 있다...\n")


# 103 - 차를 탄다
def COM103(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if MASTER == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력


# 104 - 약을 탄다
def COM104(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if MASTER == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력


# 105 - 동행
def COM105(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if MASTER == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력


# 106 - 청소한다
def COM106(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if MASTER == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력


# 107 - 도와준다
def COM107(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if MASTER == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력


# 108 - 휴식한다
def COM108(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if MASTER == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력


# 109 - 화낸다
def COM109(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if MASTER == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력


# 110 - 사과한다
def COM110(PLAYER: CM.Character):
    # 변수 준비1 : 기본적으로 준비해놓고 쓰는 변수
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 변수 준비2 : 추가적으로 필요한 변수

    # 커맨드 취소구간 : 모종의 이유로 커맨드가 취소될 때 어느 페이즈부터 재시작하는지를 지정함
    # 먼저 취소되는 사유를 작성함 - 오름차순으로
    if MASTER == None:
        SYSTEM.RESULT = 1002
        return
    # 마지막에 정상 실행을 작성함
    else:
        SYSTEM.RESULT = 1000

    # 실제 커맨드 실행

    # 커맨드 실행에 따른 EXP 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 실행에 따른 PARAM 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드에 따른 호감도 증가
    # - 커맨드 수행 캐릭터
    # - 커맨드 대상 캐릭터

    # 커맨드 자체 대사 출력
