import MODULE.MapModule as MM
import MODULE.SystemModule as SM
import MODULE.CharacterModule as CaM
import MODULE.ClothModule as CoM
import shop

SYSTEM = SM.System()


class PrepareEnvironments:
    def __init__(self):
        global SYSTEM
        SYSTEM.after(self.phase0)

    def phase0(self):
        global SYSTEM

        # 기반설정 - 맵 생성
        if SYSTEM.MAP == None:
            SYSTEM.MAP = MM.generateMap()

        # 기반설정 - 옷 준비
        if SYSTEM.CLOTHLIST == None:
            SYSTEM.CLOTHLIST = CoM.prepareClothData()

        # 기반설정 - 플레이어 지정
        if SYSTEM.MASTER == None:
            SYSTEM.MASTER = 0

        # 기반설정 - 캐릭터 준비(나중에 로딩구현시 이 부분에 반영하면 됨)
        if SYSTEM.CHARACTERS == None:
            SYSTEM.CHARACTERS = CaM.prepareCharacters(SYSTEM.VARSIZE)

        # 캐릭터를 지정한 위치에 배치
        if SYSTEM.CHARACTERS != None:
            for CHARA in SYSTEM.CHARACTERS:
                CHARA.currL = SYSTEM.MAP[CHARA.CFLAG[10]]
                CHARA.currL.space.append(CHARA)

        # 기반설정 - 캐릭터 복장 설정
        if SYSTEM.CHARACTERS != None:
            for CHARA in SYSTEM.CHARACTERS:
                CoM.setCloth(CHARA, 0, SYSTEM.CLOTHLIST)

        SYSTEM.after(self.phase1)

    def phase1(self):
        global SYSTEM
        SYSTEM.delText(4)
        SYSTEM.delText(5)
        SYSTEM.setText(4, "필요에 따라 각종 캐릭터의 수정/설정을 제공합니다.")
        SYSTEM.after(self.phase2)

    def phase2(self):
        global SYSTEM
        commands = {
            1: ("캐릭터 수정", None),
            2: ("복장 수정", None),
            3: ("후타나리화 적용", None),
            4: ("준비 완료", None),
        }
        SYSTEM.input(commands, 10, 1, "left")
        SYSTEM.after(self.phase3)

    def phase3(self):
        global SYSTEM
        RESULT = SYSTEM.RESULT
        # (1) 아나타에 대한 커스텀
        if RESULT == 1:
            print("아나타 커스텀!")
            SYSTEM.after(self.phase1)
        # (2) 복장 수정
        elif RESULT == 2:
            print("복장 수정")
            SYSTEM.after(self.phase1)
        # (3) 후타나리화
        elif RESULT == 3:
            print("후타나리화!")
            SYSTEM.after(self.phase1)
        # (4) 준비완료
        elif RESULT == 4:
            print("준비완료!")
            SYSTEM.after(shop.startShop)


def preprare():
    game = PrepareEnvironments()
