from json import load
from PIL import Image, ImageTk
from MapModule import Node
from collections import defaultdict
from typing import Dict, Optional


class IntegerVariable:
    def __init__(
        self, data: int = 0, min: Optional[int] = None, max: Optional[int] = None
    ):
        self.__data = data
        if self.__data is None:
            self.isValid = False
        else:
            self.isValid = True
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


class InvertedVariable:
    def __init__(self, name: list[str], value=0):
        self.__name = tuple(name)
        self.isValid = True
        self.__data = IntegerVariable(value)

    @property
    def name(self):
        if self.__data.get() >= 0:
            return self.__name[0]
        else:
            return self.__name[1]

    @property
    def data(self):
        return self.__data


class TagedVariable:
    def __init__(self, name: str, minValue=None, maxValue=None, isValid=True, value=0):
        self.__name = name
        self.isValid = isValid
        if self.isValid:
            self.__data = IntegerVariable(value, minValue, maxValue)
        else:
            self.__data = IntegerVariable(None)

    @property
    def name(self):
        return self.__name

    @property
    def data(self):
        return self.__data


#
class Character:
    def __init__(self, id):
        with open(f"DATA/CHARA{id}.json", "r", encoding="utf-8") as jsonFile:
            data = load(jsonFile)

        self.IMG = ImageTk.PhotoImage(Image.open(f"./RESOURCE/{id}.png"))

        # -------- 신규 파트 ---------
        self.__id = data["ID"]
        self.__name = {"이름": data["NAME"], "애칭": data["NICK"]}

        # 소질관리용 변수 - 기본값이 0인 defaultdict이니 주의할 것
        self.talent = defaultdict(IntegerVariable, data["TALENT"])

        # 기본수치 관리용 변수 - 최대/최소가 존재하니 주의
        self.base = (
            TagedVariable("체력", 0, data["BASE"]["체력"]),
            TagedVariable("정신력", 0, data["BASE"]["정신력"]),
            TagedVariable("피로도", 0, data["BASE"]["피로도"]),
            TagedVariable("욕망", 0, data["BASE"]["욕망"]),
            TagedVariable("배설욕", 0, data["BASE"]["배설욕"]),
            TagedVariable(
                "정액량", 0, data["BASE"]["정액량"], self.talent["성별"] != 0
            ),
            TagedVariable(
                "모유량", 0, data["BASE"]["모유량"], self.talent["성별"] != 1
            ),
        )

        # 쾌감을 기록하는 변수 - 최대 / 최소 없음
        # - 클래스를 따로 준비해서 생성된 객체의 메서드를 활용하도록 분리하여 설계됨
        self.plsr = (
            TagedVariable(("P" if self.talent["성별"] != 0 else "C") + "쾌감"),
            TagedVariable("A쾌감"),
            TagedVariable("B쾌감"),
            TagedVariable("M쾌감"),
            TagedVariable("V쾌감", isValid=self.talent["성별"] != 1),
            TagedVariable("W쾌감", isValid=self.talent["성별"] != 1),
        )

        # 경험을 기록하는 변수 - 최대 / 최소 없음
        self.exp1 = defaultdict(
            lambda: (
                TagedVariable(("P" if self.talent["성별"] != 0 else "C") + "절정경험"),
                TagedVariable("A절정경험"),
                TagedVariable("B절정경험"),
                TagedVariable("M절정경험"),
                TagedVariable("V절정경험", isValid=self.talent["성별"] != 1),
                TagedVariable("W절정경험", isValid=self.talent["성별"] != 1),
            )
        )
        self.exp2 = defaultdict(
            lambda: (
                TagedVariable(("P" if self.talent["성별"] != 0 else "C") + "개발경험"),
                TagedVariable("A개발경험"),
                TagedVariable("B개발경험"),
                TagedVariable("M개발경험"),
                TagedVariable("V개발경험", isValid=self.talent["성별"] != 1),
                TagedVariable("W개발경험", isValid=self.talent["성별"] != 1),
            )
        )
        self.exp3 = defaultdict(
            lambda: (
                TagedVariable(("P" if self.talent["성별"] != 0 else "C") + "성교경험"),
                TagedVariable("A성교경험"),
                TagedVariable("B성교경험"),
                TagedVariable("M성교경험"),
                TagedVariable("V성교경험", isValid=self.talent["성별"] != 1),
                TagedVariable("W성교경험", isValid=self.talent["성별"] != 1),
            )
        )
        self.exp4 = defaultdict(
            lambda: (
                None,
                None,
                None,
                None,
                None,
                None,
            )
        )
        


        # 부위를 관리하는 변수 - 최대 1000 / 최소 0
        # - 클래스를 따로 준비해서 생성된 객체의 메서드를 활용하도록 분리하여 설계됨
        self.body = (
            TagedVariable(
                ("C" if self.talent[0].get() == 0 else "P") + "상태", 0, 1000
            ),
            TagedVariable("A상태", 0, 1000),
            TagedVariable("B상태", 0, 1000),
            TagedVariable("M상태", 0, 1000),
            TagedVariable("V상태", 0, 1000, self.talent["성별"] != 1),
            TagedVariable("W상태", 0, 1000, self.talent["성별"] != 1),
        )

        # 관계를 기록하는 변수
        # - defaultdict에 캐릭터 이름(문자열)로 직접 접근하여 사용 / 단기적인 행동에 의하여 누적되는 장기적인 관계지표
        self.attr = defaultdict(  # 호감도 : 상대방에 대하여 양수는 호의 / 음수는 적의
            lambda: InvertedVariable(["호의", "적의"])
        )
        self.trst = defaultdict(  # 신뢰도 : 상대방에 대하여 양수는 신뢰 / 음수는 불신
            lambda: InvertedVariable(["신뢰", "불신"])
        )
        self.subm = defaultdict(  # 관계도 : 상대방에 대하여 양수는 S성향 / 음수는 M성향
            lambda: InvertedVariable(["S성향", "M성향"])
        )

        # 감정을 기록하는 변수
        # - defaultdict에 캐릭터 이름(문자열)로 직접 접근하여 사용 / 단기적인 행동에 의하여 나타나는/누적되는 관계지표
        self.mood = defaultdict(
            lambda: (
                InvertedVariable(["기쁨", "슬픔"]),
                InvertedVariable(["분노", "공포"]),
                InvertedVariable(["혐오", "수용"]),
                InvertedVariable(["기대", "놀람"]),
                InvertedVariable(["욕망", "평정"]),
                InvertedVariable(["친밀감", "소외감"]),
                InvertedVariable(["수치짐", "자신감"]),
            )
        )

        # 부가된 명령을 수행하는데 걸리는 소요시간을 기록하는 변수
        self.remainTime = 0

        # 현재 선택된 행동이 무엇인지 확인하는 변수
        self._currentAction = None

        # 캐릭터가 선택한 대상을 기록하는 변수
        self.TARGET: Character = None

        # 위치 관리를 위한 변수
        self.currL: Node = None  # CFLAG[11] - 현재위치
        self.pastL: Node = None  # CFLAG[12] - 이전위치
        self.route: list[Node] = []

    def name(self, after: str | None = None, select="애칭"):
        if after is None:
            return self.__name[select]
        else:
            # 한글 유니코드 범위: 0xAC00 ~ 0xD7A3
            min_code = 0xAC00
            max_code = 0xD7A3

            # 이름의 마지막 글자의 코드값 취득
            final_code = ord(self.__name[select][-1])

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
                    return self.__name[select] + (afters[0] if hasFinal else afters[1])
            # 못찾았으면 그대로 반환
            return self.__name[select] + after

    def __mod__(self, msg: str):
        if msg[0] == " " or msg[:2] == "에게" or msg[:2] == "한테":
            return self.name() + msg
        else:
            return self.name(msg[0]) + msg[1:]


# 게임 내에서 등장하는 캐릭터 목록을 준비하는 함수
def prepareCharacters():
    cList = []

    # 기초 정보를 토대로 캐릭터를 생성함
    for i in range(9):
        cList.append(Character(i))

    return cList
