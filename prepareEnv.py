import MODULE.MapModule as MM
import MODULE.SystemModule as SM
import MODULE.CharacterModule as CaM
import MODULE.ClothModule as CoM
import shop

SYSTEM = SM.System()

def setFutanari():
    global SYSTEM
    pass

def prepareEnv():
    global SYSTEM

    # 맵준비
    if SYSTEM.MAP == None:
        SYSTEM.MAP = MM.generateMap()

    # 캐릭터준비
    if SYSTEM.CHARACTERS == None:
        SYSTEM.CHARACTERS = CaM.prepareCharacters(SYSTEM.VARSIZE)
        # 읽어들인 정보를 토대로 현재위치를 설정함
        for CHARA in SYSTEM.CHARACTERS.values():
            CHARA.CFLAG[11] = SYSTEM.MAP[CHARA.CFLAG[10]]
            CHARA.CFLAG[11].SPACE.append(CHARA)

    # 옷준비
    if SYSTEM.CLOTHLIST == None:
        SYSTEM.CLOTHLIST = CoM.prepareClothData()
        # 읽어들인 정보를 토대로 기본복장을 설정함
        for CHARA in SYSTEM.CHARACTERS.values():
            CoM.setCloth(CHARA, 0, SYSTEM.CLOTHLIST)
    
    # 플레이어 캐릭터 지정
    if SYSTEM.MASTER == None:
        SYSTEM.MASTER = 0

    command = {
        1:"캐릭터 수정",
        2:"후타나리화 적용",
        3:"준비 완료"
    }
    RESULT = SYSTEM.input(command)
    command = {
        1:lambda:print("커스텀모드!"),
        2:setFutanari,
        3:shop.shop,
    }
    command[RESULT]()
    if RESULT != 3:
        SYSTEM.after(0, prepareEnv)

    # (1) 사용자 입력에 따라 후타나리화 처리 진행

    # (2) 사용자가 요청한 경우 아나타에 대한 커스텀 진행

    # (3) 아나타의 복장에 대한 커스텀 진행

    # (4) 사용자가 요청한 경우 환녀의 능력치에 대한 커스텀 진행

    # (5) 사용자가 요청한 경우 방문자에 대한 커스텀 진행
    #     -> 이건 기본적으로, 이나타 커스텀을 사용자에 대해서 진행하도록 설정
    #     -> 방문자와 최면좌는 각각 -2 ,-1에 위치하니 까먹지 말 것