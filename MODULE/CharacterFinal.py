from typing import List
from MODULE.SystemModule import SYSTEM
from MODULE.CharacterMethod2 import CharacterType2

class Character(CharacterType2):
    pass

# 게임 내에서 등장하는 캐릭터 목록을 준비하는 함수
def prepare() -> List[Character]:
    chara_list: List[Character] = []

    # 기초 정보를 토대로 캐릭터를 생성함
    for i in range(9):
        chara_list.append(Character(i))
    
    # 생성된 캐릭터를 지정한 위치에 배치함
    for chara in chara_list:
        chara.currL = SYSTEM.MAP[chara.cflag[10]]
        chara.currL.space.append(chara)

    return chara_list
