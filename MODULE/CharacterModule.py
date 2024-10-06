from json import load
from csv import reader as read
from PIL import Image, ImageTk
from MapModule import Node
from collections import defaultdict, namedtuple
from typing import Dict, Optional


def setValue(target: list | dict, source: dict):
    for key in source:
        target[int(key)] = source[key]


def getList(value: any, size: int, source: dict = None):
    lst = [value for i in range(size)]
    if source != None:
        setValue(lst, source)
    return lst


class IntergratedVariable:
    def __init__(
        self, data: int = 0, min: Optional[int] = None, max: Optional[int] = None
    ):
        self.__data = data
        self.__max = max
        self.__min = min

    def adjust(self):
        if self.__max is not None and self.__data > self.__max:
            self.__data = self.__max
        if self.__min is not None and self.__data < self.__min:
            self.__data = self.__min

    def checkType(self, other):
        if not isinstance(other, int):
            raise TypeError("Only Integer Granted")

    def __add__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            return self.__data + other

    def __radd__(self, other):
        if self.__data is None:
            return other
        else:
            self.checkType(other)
            return other + self.__data

    def __sub__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            return self.__data - other

    def __rsub__(self, other):
        if self.__data is None:
            return other
        else:
            self.checkType(other)
            return other - self.__data

    def __mul__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            return self.__data * other

    def __rmul__(self, other):
        if self.__data is None:
            return other
        else:
            self.checkType(other)
            return other * self.__data

    def __truediv__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            return int(self.__data / other)

    def __rtruediv__(self, other):
        if self.__data is None:
            return other
        else:
            self.checkType(other)
            return int(other / self.__data)

    def __iadd__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            self.__data += other
            self.adjust()
            return self

    def __isub__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            self.__data -= other
            self.adjust()
            return self

    def __imul__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            self.__data *= other
            self.adjust()
            return self

    def __itruediv__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            self.__data = int(self.__data / other)
            self.adjust()
            return self

    def set(self, other):
        self.__data = other
        self.adjust()

    def get(self):
        return self.__data
    
    def setMax(self, other):
        self.__max = other
    
    def setMin(self, other):
        self.__min = other


Plsr = namedtuple("Plsr", ["c", "a", "b", "m", "v", "w"])


def getPlsr(gender: 0 | 1 | 2):
    if gender == 1:
        return Plsr(
            IntergratedVariable(),
            IntergratedVariable(),
            IntergratedVariable(),
            IntergratedVariable(),
            IntergratedVariable(None),
            IntergratedVariable(None),
        )
    else:
        return Plsr(
            IntergratedVariable(),
            IntergratedVariable(),
            IntergratedVariable(),
            IntergratedVariable(),
            IntergratedVariable(),
            IntergratedVariable(),
        )


Part = namedtuple("Part", ["c", "a", "b", "v", "w"])


def getPart(gender: 0 | 1 | 2):
    if gender == 1:
        return Part(
            IntergratedVariable(min=0, max=1000),
            IntergratedVariable(min=0, max=1000),
            IntergratedVariable(min=0, max=1000),
            IntergratedVariable(None, min=0, max=1000),
            IntergratedVariable(None, min=0, max=1000),
        )
    else:
        return Part(
            IntergratedVariable(min=0, max=1000),
            IntergratedVariable(min=0, max=1000),
            IntergratedVariable(min=0, max=1000),
            IntergratedVariable(min=0, max=1000),
            IntergratedVariable(min=0, max=1000),
        )


class Character:
    def __init__(self, id, VARSIZE):
        with open(f"DATA/CHARA{id}.json", "r", encoding="utf-8") as jsonFile:
            result = load(jsonFile)

        self.IMG = ImageTk.PhotoImage(Image.open(f"./RESOURCE/{id}.png"))

        # JSON파일에 들어있어야 하는 파트
        self.ID = result["ID"]
        self.__NAME = [result["NAME"], result["ANAME"]]
        self.TALENT = getList(-3, VARSIZE["TALENT"], result["TALENT"])
        self.BODY = getList(-3, VARSIZE["BODY"], result["BODY"])
        self.CFLAG = getList(0, VARSIZE["CFLAG"], result["FLAG"])
        self.ABL = getList(
            0, VARSIZE["ABL"], source=result["ABL"] if "ABL" in result else None
        )

        # 경험치 기록을 위한 DB 생성 - 기록만 하면 되는거니 생성만 진행
        self.EXP = getList(None, VARSIZE["EXP"])
        with open("DATA/EXP.csv", "r", encoding="utf-8") as csvFile:
            for row in read(csvFile):
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    if row[1] != "0":
                        self.EXP[int(row[0])] = [
                            [0 for i in range(int(row[2]))] for i in range(int(row[1]))
                        ]
                    else:
                        self.EXP[int(row[0])] = [0 for i in range(int(row[2]))]

        # 파라미터 기록을 위한 DB 생성 - 최대값 설정도 변행해야 하니 같이 진행
        self.PARAM = getList(None, VARSIZE["PARAM"])
        with open("DATA/PARAM.csv", "r", encoding="utf-8") as csvFile:
            # 먼저 CSV에서 설정된 구조에 따라 DB를 생성함
            for row in read(csvFile):
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    if row[1] == "0":
                        self.PARAM[int(row[0])] = [0 for i in range(int(row[2]))]
                    else:
                        if row[2] == "dict":
                            self.PARAM[int(row[0])] = defaultdict(
                                lambda size=int(row[1]): [0 for i in range(size)]
                            )
                        else:
                            self.PARAM[int(row[0])] = [
                                [0 for i in range(int(row[2]))]
                                for i in range(int(row[1]))
                            ]
            # DB에 json에 설정해놓은 최대값이 존재하는 것들은 최대 값을 모두 기록함
            for i, alist in enumerate(result["PARAM"]):
                for j, maxValue in enumerate(alist):
                    self.PARAM[i][j][1] = maxValue

            # 이후 일부 파라미터에 대해 보정을 진행함
            # (1) 여성은 정액이 없음
            if self.TALENT[0] == 0:
                self.PARAM[0][5][0] = None
                self.PARAM[1][0][0] = None
            # (2) 남자는 질과 자궁이 없음
            if self.TALENT[0] == 1:
                self.PARAM[3][1] = None
                self.PARAM[3][5] = None
            # (3) 남자는 애초에 모유가 없고, 여성과 후타나리는 임신하지 않으면 모유가 없음
            self.PARAM[0][6][0] = None
            self.PARAM[1][1][0] = None

        # JSON파일에 들어있으며 안되는 파트
        self.ITEM = getList(None, VARSIZE["ITEM"])

        # EQUIP은 분리하는걸 재설계하자
        # -> CLOTHEQUIP : 복장
        # -> BODYEQUIP : 도구장착
        self.EQUIP = getList(None, VARSIZE["EQUIP"])

        # STAIN을 추가해서 흔적이 남도록 만들어줘야 함

        # -------- 신규 파트 ---------

        # 위치 관리를 위한 변수
        self.currL: Node = None  # CFLAG[11] - 현재위치
        self.pastL: Node = None  # CFLAG[12] - 이전위치
        self.route: list[Node] = []

        # 관계를 기록하는 변수
        # - defaultdict에 캐릭터 이름(문자열)로 직접 접근하여 사용
        self.attr = defaultdict(IntergratedVariable)  # 호감도 : 양수는 호의 / 음수는 적의
        self.trst = defaultdict(IntergratedVariable)  # 신뢰도 : 양수는 신뢰 / 음수는 불신
        self.subm = defaultdict(IntergratedVariable)  # 굴복도 : 양수는 순응 / 음수는 반항

        # 감정을 기록하는 변수
        # - defaultdict에 캐릭터 이름(문자열)로 직접 접근하여 사용 / 어느 감정에 변화를 주는지 인덱스로 지정함
        self.mood: Dict[str, tuple[IntergratedVariable]] = defaultdict(lambda: (IntergratedVariable() for i in range(5)))

        # 쾌감을 기록하는 변수 - 0:C, 1:A, 2:B, 3:M, 4:V, 5:W
        # - 클래스를 따로 준비해서 생성된 객체의 메서드를 활용하도록 분리하여 설계됨
        self.plsr: Plsr = getPlsr("""TALENT[0]를 반영해야 됨""")

        # 부위를 관리하는 변수 - 0:C, 1:A, 2:B, 3:V, 4:W
        # - 클래스를 따로 준비해서 생성된 객체의 메서드를 활용하도록 분리하여 설계됨
        self.part: Part = getPart("""TALENT[0]를 반영해야 됨""")

        # 부가된 명령을 수행하는데 걸리는 소요시간을 기록하는 변수
        self.remainTime = 0

        # 현재 선택된 행동이 무엇인지 확인하는 변수
        self._currentAction = None

        # 캐릭터가 선택한 대상을 기록하는 변수
        self.TARGET: Character = None

    def NAME(self, after: str | None = None, index=1):
        if after is None:
            return self.__NAME[index]
        else:
            # 한글 유니코드 범위: 0xAC00 ~ 0xD7A3
            min_code = 0xAC00
            max_code = 0xD7A3

            # 이름의 마지막 글자의 코드값 취득
            final_code = ord(self.__NAME[index][-1])

            # 판별결과를 기록함 - 받침의 유무를 기록함
            hasFinal = not (
                final_code < min_code
                or final_code > max_code
                or (final_code - min_code) % 28 == 0
            )

            # 해당되는 받침을 찾음
            afterList = ("은는", "이가", "을를", "과와")
            for afters in afterList:
                # 받침을 찾았으면 받침유무에 따라 최종적으로 사용할 문자를 선택함
                if after in afters:
                    return self.__NAME[index] + (afters[0] if hasFinal else afters[1])
            # 못찾았으면 그대로 반환
            return self.__NAME[index] + after

    def __mod__(self, msg: str):
        if msg[0] == " " or msg[:2] == "에게" or msg[:2] == "한테":
            return self.NAME() + msg
        else:
            return self.NAME(msg[0]) + msg[1:]

    # updateBASE1 메서드 : 심신과 관련된 수치를 반영하기 위한 메서드
    # - 호출할 때는 2가지 유형으로 호출함
    # chara.updateBASE1(1,2,3) or chara.updateBASE1(MLK = 100)
    def updateBASE1(self, VIT=0, RAT=0, ARL=0, FTG=0, SLP=0, SEM=0, MLK=0):
        self.PARAM[0][0][0] += VIT  # 체력
        self.PARAM[0][1][0] += RAT  # 이성
        self.PARAM[0][2][0] += ARL  # 성욕
        self.PARAM[0][3][0] += FTG  # 피로
        self.PARAM[0][4][0] += SLP  # 수면
        # 남성이나 후타나리이면 정액수치를 반영함
        if self.TALENT[0] >= 1:
            self.PARAM[0][5][0] += SEM  # 정액
        # 여성이나 후타나리이면 모유수치를 반영함 / 단, 어디까지나 None일 경우에만 가능함
        if self.TALENT[0] != 1 and self.PARAM[0][6][0] is not None:
            self.PARAM[0][6][0] += MLK  # 모유

        # 현재치가 최대치를 초과했을 경우 최대치로 변경함
        for param in self.PARAM[0]:
            if param[0] is not None:
                if param[0] > param[1]:
                    param[0] = param[1]
        # 현재치가 최소치(0) 미만일 경우 최소치로 변경함
        for param in self.PARAM[0]:
            if param[0] is not None:
                if param[0] < 0:
                    param[0] = 0

    # updateBASE2 메서드 : 욕구와 관련된 수치를 반영하기 위한 메서드
    # - 호출할 때는 updateBASE1과 동일한 방식으로 호출함
    def updateBASE2(self, SEM=0, MLK=0, SIO=0, PEE=0, POO=0):
        # 남성이나 후타나리이면 사정욕구를 반영함
        if self.TALENT[0] >= 1:
            self.PARAM[1][0][0] += SEM  # 사정욕구
        # 여성이나 후타나리이면 분유욕구를 반영함 / 단, 어디까지나 None일 경우에만 가능함
        if self.TALENT[0] != 1 and self.PARAM[1][1][0] is not None:
            self.PARAM[1][1][0] += MLK  # 분유욕구
        self.PARAM[1][2][0] += SIO  # 시오후키
        self.PARAM[1][3][0] += PEE  # 소변욕구
        self.PARAM[1][4][0] += POO  # 대변욕구

        # 현재치가 최대치를 초과했을 경우 최대치로 변경함
        for param in self.PARAM[1]:
            if param[0] is not None:
                if param[0] > param[1]:
                    param[0] = param[1]
        # 현재치가 최소치(0) 미만일 경우 최소치로 변경함
        for param in self.PARAM[1]:
            if param[0] is not None:
                if param[0] < 0:
                    param[0] = 0


# 게임 내에서 등장하는 캐릭터 목록을 준비하는 함수
def prepareCharacters(VARSIZE):
    cList = []

    # 기초 정보를 토대로 캐릭터를 생성함
    for i in range(VARSIZE["CHARA"]):
        cList.append(Character(i, VARSIZE))

    return cList
