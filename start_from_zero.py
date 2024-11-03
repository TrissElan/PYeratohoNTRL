import MODULE.MapModule as MM

import MODULE.CharacterModule as CM
import start_shop as SS
from MODULE.SystemModule import SYSTEM


class PrepareEnvironments:
    def __init__(self):
        SYSTEM.RESULT = 0
        SYSTEM.clearImgArea()
        SYSTEM.clearTextArea()
    
    def start(self):
        SYSTEM.after(self.phase0)

    def phase0(self):
        # 기반설정 - 맵 생성
        SYSTEM.MAP = MM.generateMap()

        # 기반설정 - 옷 준비
        SYSTEM.CLOTHLIST = None

        # 기반설정 - 플레이어 지정
        SYSTEM.MASTER = 0

        # 기반설정 - 캐릭터 준비(나중에 로딩구현시 이 부분에 반영하면 됨)
        SYSTEM.CHARACTERS = CM.prepareCharacters()
            
        # 준비된 캐릭터에게 각종 설정 적용
        # - 지정한 위치에 배치함
        for chara in SYSTEM.CHARACTERS:
            chara.currL = SYSTEM.MAP[chara.cflag[10]]
            chara.currL.space.append(chara)


        SYSTEM.after(self.phase1)

    def phase1(self):
        SYSTEM.delText(4)
        SYSTEM.delText(5)
        SYSTEM.setText(4, "필요에 따라 각종 캐릭터의 수정/설정을 제공합니다.")
        SYSTEM.after(self.phase2)

    def phase2(self):
        commands = {
            1: ("캐릭터 수정", None),
            2: ("복장 수정", None),
            3: ("후타나리화 적용", None),
            4: ("준비 완료", None),
        }
        SYSTEM.input(commands, 10, 1, "left")
        SYSTEM.after(self.phase3)

    def phase3(self):
        RESULT = SYSTEM.result
        # (1) 아나타에 대한 커스텀
        if RESULT == 1:
            SYSTEM.after(self.phase1)
        # (2) 복장 수정
        elif RESULT == 2:
            SYSTEM.after(self.phase1)
        # (3) 후타나리화
        elif RESULT == 3:
            SYSTEM.after(self.phase1)
        # (4) 준비완료
        elif RESULT == 4:
            SYSTEM.after(SS.shop)


def preprare():
    game = PrepareEnvironments()
    game.start()
