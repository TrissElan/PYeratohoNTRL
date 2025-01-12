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
        locations = {location.ID: location.name() for location in self.currL.link}
        if self._id == SYSTEM.MASTER:
            locations[1002] = "취소"
            SYSTEM.input(locations, width=25, col=4, align="left")
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
            
    
    def COM101(self):
        # 대화 커맨드
        if self.target is None:
            SYSTEM.result = 1002
            return

        # 경험치 증가
        self.exp4["자각"][1].data += 1  # 대화경험
        self.target.exp4["자각"][1].data += 1

        # 파라미터 증가
        self.base[0].data -= 10  # 체력
        self.base[1].data -= 1   # 이성
        self.base[2].data += 1   # 피로

        self.target.base[0].data -= 10
        self.target.base[1].data -= 1
        self.target.base[2].data += 1

        SYSTEM.result = 1000

        # 대사 출력
        master = SYSTEM.CHARACTERS[SYSTEM.MASTER]
        if master not in self.target.currL.space:
            return
        else:
            if master == self or master.target == self:
                SYSTEM.setText(self % "는 " + self.target % "과 가벼운 대화를 시작했다.\n")
            else:
                SYSTEM.setText(self % "는 자신이 아닌 " + self.target % "과 가벼운 대화를 시작했다...\n")

            if self.target.attr[self.name()].data.current <= 100:
                SYSTEM.setText("별 관심이 없어 보인다...\n")
            elif self.target.attr[self.name()].data.current <= 200:
                SYSTEM.setText("재미다는 듯 가끔 미소를 짓는다...\n")
            elif self.target.attr[self.name()].data.current <= 300:
                SYSTEM.setText("미소를 지어준다...\n")
            else:
                SYSTEM.setText("환한 미소를 만들고 있다...\n")
