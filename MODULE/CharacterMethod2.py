from MODULE.CharacterMethod1 import CharacterType1
from MODULE.SystemModule import SYSTEM

# 일상계 커맨드를 추가하기 위한 클래스
# - 각종 기본적인 조작이 여기에 포함됨
class CharacterType2(CharacterType1):
    '''
    100,이동한다
    101,대화한다
    102,차를 탄다
    103,약을 탄다
    104,동행
    105,청소한다
    106,도와준다
    107,휴식한다
    108,화낸다
    109,사과한다
    '''
    def COM100(self):
        locations = {}
        for location in self.currL.link:
            locations[location.ID] = (location.name(), None)
        if self._id == SYSTEM.MASTER:
            locations[1002] = ("취소", None)
            SYSTEM.input(locations, 25, 4, "left")
        else:
            SYSTEM.inputr(locations)
        if SYSTEM.result == 1002:
            return
        else:
            master = SYSTEM.CHARACTERS[SYSTEM.MASTER]
            beforeHere = (
            self is not master
            and master in self.currL.space
            )  # 마스터와 이동전 같은 방인지 여부
            destination = SYSTEM.MAP[SYSTEM.result]
            self.currL.space.remove(self)
            self.pastL = self.currL
            destination.space.append(self)
            self.currL = destination
            afterHere = (
                self is not master
                and master in self.currL.space
            )
            if beforeHere:
                SYSTEM.setText(
                    self % "는 " + SYSTEM.MAP[SYSTEM.result] % "으로 이동했다.\n"
                )
            if afterHere:
                SYSTEM.setText(self % "가 " + destination % "에 왔다.\n")
            SYSTEM.result = 1000
        
        
        

