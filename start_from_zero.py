import MODULE.MapModule as MM

import MODULE.CharacterFinal as CM
import start_shop
from MODULE.SystemModule import SYSTEM


class PrepareEnvironments:
    def __init__(self):
        self.__commands = {
            1: "성벽 설정 완료",
            2: "캐릭터 수정",
            3: "복장 수정",
            4: "후타나리화 적용",
        }
        
    def start(self):
         # 기반설정 - 맵 생성
        SYSTEM.MAP = MM.generateMap()

        # 기반설정 - 옷 준비
        SYSTEM.CLOTHLIST = None

        # 기반설정 - 플레이어 지정
        SYSTEM.MASTER = 0

        # 기반설정 - 캐릭터 준비(나중에 로딩구현시 이 부분에 반영하면 됨)
        SYSTEM.CHARACTERS = CM.prepare()

        SYSTEM.after(self.phase0)

    def phase0(self):
        SYSTEM.clearImgArea()
        SYSTEM.clearTextArea()
        SYSTEM.after(self.phase1)

    def phase1(self):
        SYSTEM.setText("필요에 따라 각종 캐릭터의 수정/설정을 제공합니다.")
        SYSTEM.after(self.phase2)
        

    def phase2(self):
        SYSTEM.input(self.__commands, width=10, col=1, align="left")
        SYSTEM.after(self.phase3)

    def phase3(self):
        # (1) 준비완료
        if SYSTEM.result == 1:
            SYSTEM.after(start_shop.main)
        else:
            # (2) 아나타에 대한 커스텀
            if SYSTEM.result == 2:
                pass
            # (3) 복장 수정
            elif SYSTEM.result == 3:
                pass
            # (4) 후타나리화
            elif SYSTEM.result == 4:
                pass
            SYSTEM.after(self.phase0)

def main():
    game = PrepareEnvironments()
    game.start()
