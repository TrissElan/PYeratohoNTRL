from json import load
from typing import Dict, List, Tuple, Optional, Any, Union
from PIL import Image, ImageTk
from MapModule import Node
from collections import defaultdict
from MODULE.VariableModule import IntegerVariable, InvertedVariable, TagedVariable

# 캐릭터의 데이터를 구성하기 위한 클래스
# - 여기서 모든 캐릭터의 수치 / 정보를 작성하고 관리함

class CharacterBase:
    def __init__(self, id: int) -> None:
        with open(f"DATA/CHARA{id}.json", "r", encoding="utf-8") as jsonFile:
            data: Dict[str, Any] = load(jsonFile)

        # __private : 없음

        # _protected
        self._id: int = data["ID"]
        self._name: Dict[str, str] = {"이름": data["NAME"], "애칭": data["NICK"]}
        self._img: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(f"./RESOURCE/{id}.png"))

        # public

        # 소질관리용 변수 - 기본값이 None인 defaultdict이니 주의할 것
        talent_dict: Dict[str, IntegerVariable] = {k: IntegerVariable(v) for k, v in data["TALENT"].items()}
        self.talent: defaultdict[str, IntegerVariable] = defaultdict(lambda: IntegerVariable(None), talent_dict)

        # 기본수치 관리용 변수 - 최대/최소가 존재하니 주의
        self.base: Tuple[TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable] = (
            TagedVariable("체력", 0, data["BASE"]["체력"]),
            TagedVariable("이성", 0, data["BASE"]["이성"]),
            TagedVariable("피로", 0, data["BASE"]["피로"]),
            TagedVariable("배설욕", 0, data["BASE"]["배설욕"]),
            TagedVariable(
                "정액량", 0, data["BASE"]["정액량"], self.talent["성별"].current != 0
            ),
            TagedVariable(
                "모유량", 0, data["BASE"]["모유량"], self.talent["성별"].current != -1
            ),
        )

        # 관계를 기록하는 변수 : 딕셔너리의 키로 캐릭터의 이름(문자열)을 사용함
        self.attr: defaultdict[str, InvertedVariable] = defaultdict(
            lambda: InvertedVariable(["호의", "적의"])
        )
        self.trst: defaultdict[str, InvertedVariable] = defaultdict(
            lambda: InvertedVariable(["신뢰", "의심"])
        )
        self.subm: defaultdict[str, InvertedVariable] = defaultdict(
            lambda: InvertedVariable(["S성향", "M성향"])
        )

        # 감정을 기록하는 변수 : 딕셔너리의 키로 캐릭터의 이름(문자열)을 사용함
        self.mood: defaultdict[str, Tuple[InvertedVariable, InvertedVariable, InvertedVariable, InvertedVariable, InvertedVariable, InvertedVariable, InvertedVariable]] = defaultdict(
            lambda: (
                InvertedVariable(["기쁨", "슬픔"]),
                InvertedVariable(["기대", "공포"]),
                InvertedVariable(["흥분", "권태"]),
                InvertedVariable(["욕망", "혐오"]),
                InvertedVariable(["안정", "불안"]),
                InvertedVariable(["자존", "수치"]),
                InvertedVariable(["관심", "무심"]),
            )
        )

        # 쾌감을 기록하는 변수
        self.plsr: Tuple[TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable] = (
            TagedVariable(("P" if self.talent["성별"].current != 1 else "C") + "쾌감"),
            TagedVariable("A쾌감"),
            TagedVariable("B쾌감"),
            TagedVariable("M쾌감"),
            TagedVariable("V쾌감", isValid=self.talent["성별"].current != -1),
            TagedVariable("W쾌감", isValid=self.talent["성별"].current != -1),
        )

        # 캐릭터가 선택한 대상을 기록하는 변수
        self.target: Optional[CharacterBase] = None

        # 위치 관리를 위한 변수
        self.currL: Optional[Node] = None  # CFLAG[11] - 현재위치
        self.pastL: Optional[Node] = None  # CFLAG[12] - 이전위치
        self.route: List[Node] = []

        # 그 외 각종 flag기록 변수
        self.cflag: List[int] = [0 for i in range(100)]
        for key, value in data["FLAG"].items():
            self.cflag[int(key)] = value

        # 경험을 기록하는 변수 : 각각 자각 / 무자각 / NTR로 구분
        self.exp1: defaultdict[str, Tuple[TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable]] = defaultdict(
            lambda: (
                TagedVariable(
                    ("P" if self.talent["성별"].current != 1 else "C") + "절정경험", 0
                ),
                TagedVariable("A절정경험", 0),
                TagedVariable("B절정경험", 0),
                TagedVariable("M절정경험", 0),
                TagedVariable("V절정경험", 0, isValid=self.talent["성별"].current != -1),
                TagedVariable("W절정경험", 0, isValid=self.talent["성별"].current != -1),
            )
        )
        self.exp2: defaultdict[str, Tuple[TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable]] = defaultdict(
            lambda: (
                TagedVariable(
                    ("P" if self.talent["성별"].current != 0 else "C") + "개발경험", 0
                ),
                TagedVariable("A개발경험", 0),
                TagedVariable("B개발경험", 0),
                TagedVariable("M개발경험", 0),
                TagedVariable("V개발경험", 0, isValid=self.talent["성별"].current != -1),
                TagedVariable("W개발경험", 0, isValid=self.talent["성별"].current != -1),
            )
        )
        self.exp3: defaultdict[str, Tuple[TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable]] = defaultdict(
            lambda: (
                TagedVariable(
                    ("P" if self.talent["성별"].current != 1 else "C") + "성교경험", 0
                ),
                TagedVariable("A성교경험", 0),
                TagedVariable("B성교경험", 0),
                TagedVariable("M성교경험", 0),
                TagedVariable("V성교경험", 0, isValid=self.talent["성별"].current != -1),
                TagedVariable("W성교경험", 0, isValid=self.talent["성별"].current != -1),
            )
        )
        self.exp4: defaultdict[str, Tuple[TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable]] = defaultdict(
            lambda: (
                TagedVariable("업무경험", 0),
                TagedVariable("대화경험", 0),
                TagedVariable("봉사경험", 0),
                TagedVariable("이상경험", 0),
                TagedVariable("이성경험", 0),
                TagedVariable("동성경험", 0),
            )
        )
        self.exp5: defaultdict[str, Tuple[TagedVariable, TagedVariable, TagedVariable, None, None, None]] = defaultdict(
            lambda: (
                TagedVariable("NTR경험", 0),
                TagedVariable("SM경험", 0),
                TagedVariable("노출경험", 0),
                None,
                None,
                None,
            )
        )

        # 능력을 기록하는 변수 - 최대 10 / 최소 0
        self.abl1: Tuple[TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable] = (
            TagedVariable(
                ("P" if self.talent["성별"].current != 0 else "C") + "감도", 0, 10
            ),
            TagedVariable("A감도", 0, 10),
            TagedVariable("B감도", 0, 10),
            TagedVariable("M감도", 0, 10),
            TagedVariable(
                "V감도", 0, 10, self.talent["성별"].current != -1
            ),
            TagedVariable(
                "W감도", 0, 10, self.talent["성별"].current != -1
            ),
        )
        self.abl2: Tuple[TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable] = (
            TagedVariable("입기술", 0, 10),
            TagedVariable("손기술", 0, 10),
            TagedVariable("발기술", 0, 10),
            TagedVariable("허리기술", 0, 10),
            TagedVariable("봉사기술", 0, 10),
            TagedVariable("NTR기술", 0, 10),
        )
        self.abl3: Tuple[TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable, TagedVariable] = (
            TagedVariable("S끼", 0, 10),
            TagedVariable("M끼", 0, 10),
            TagedVariable("변태도", 0, 10),
            TagedVariable("중독도", 0, 10),
            TagedVariable("노출벽", 0, 10),
            TagedVariable("바람끼", 0, 10),
        )
