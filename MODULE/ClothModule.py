import json
from collections import defaultdict


def prepareClothData():
    with open("DATA/CLOTHLIST.json", "r", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
    clothList = defaultdict(None)
    for cloth in data:
        clothList[cloth["category"] * 100 + cloth["id"]] = cloth
    return clothList


def setCloth(CHARA, index, CLOTHLIST):
    for i in range(len(CHARA.CFLAG[index])):
        if i == 0:
            CHARA.EQUIP[i] = CHARA.CFLAG[index][i]
        elif CHARA.CFLAG[index][i] == 0:
            continue
        else:
            CHARA.EQUIP[i] = Cloth(CHARA, **CLOTHLIST[CHARA.CFLAG[index][i]])


class Cloth:
    def __init__(self, chara, **clothList):
        self.OWNER = chara
        self.stain = "깨끗한"
        self.smell = f"{chara.NAME()} + 의 체취"
        self.__MOVABLE = clothList["shiftable"]  # 젓힐 수 있는지 여부
        self.STATUS = False  # 상태 / True이면 젓힌 상태
        self.CATEGORY = clothList["category"]  # 부위 인식용 카테고리번호
        self.ID = clothList["id"]  # 카테고리별 복장 인식용 번호
        self.NAME = f"{chara.NAME()}의 {clothList['name']}"  # 복장의 명칭

    def shift(self) -> bool:
        if not self.__MOVABLE:
            return False
        else:
            self.__status = not self.__status
            return True
