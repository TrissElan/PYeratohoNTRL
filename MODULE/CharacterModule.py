from json import load
from csv import reader as read
from collections import defaultdict

def setValue(target:list|dict, source:dict):
    for key in source:
        target[int(key)] = source[key]

def getList(value:any, size:int, source:dict = None):
    lst = [value for i in range(size)]
    if source != None: setValue(lst, source)
    return lst

class Character:
    def __init__(self, id, VARSIZE):
        with open(f"DATA/CHARA{id}.json", "r", encoding="utf-8") as jsonFile:
            result = load(jsonFile)
        
        # JSON파일에 들어있어야 하는 파트
        self.ID = result["ID"]
        self.__NAME = result["NAME"]
        self.__ANAME = result["ANAME"]
        self.TALENT = getList(-3, VARSIZE["TALENT"], result["TALENT"])
        self.BODY = getList(-3, VARSIZE["BODY"], result["BODY"])
        self.CFLAG = getList(0, VARSIZE["CFLAG"], result["FLAG"])
        self.ABL = getList(0, VARSIZE["ABL"], source = result["ABL"] if "ABL" in result else None)
        
        # 경험치 기록을 위한 DB 생성
        self.EXP = getList(None, VARSIZE["EXP"])
        with open("DATA/EXP.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    if row[1] != "0":
                        self.EXP[int(row[0])] = [[0 for i in range(int(row[2]))] for i in range(int(row[1]))]
                    else:
                        self.EXP[int(row[0])] = [0 for i in range(int(row[2]))]

        # 파라미터 기록을 위한 DB 생성
        self.PARAM = getList(None, VARSIZE["PARAM"])
        with open("DATA/PARAM.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    if row[1] != "0":
                        self.PARAM[int(row[0])] = [[0 for i in range(int(row[2]))] for i in range(int(row[1]))]
                    else:
                        self.PARAM[int(row[0])] = [0 for i in range(int(row[2]))]
        
        # JSON파일에 들어있으며 안되는 파트
        self.ITEM = getList(None, VARSIZE["ITEM"])

        # EQUIP은 분리하는걸 재설계하자
        # -> CLOTHEQUIP : 복장
        # -> BODYEQUIP : 도구장착
        self.EQUIP = getList(None, VARSIZE["EQUIP"])

        # STAIN을 추가해서 흔적이 남도록 만들어줘야 함

        # 위치 관리를 위한 변수
        self.CFLAG[12] = None
        self._route = []

        # 호감도를 관리하기 위한 변수
        self.CFLAG[20] = defaultdict(int)

        # 부가된 명령을 수행하는데 걸리는 소요시간을 기록하는 변수
        self.remainTime = 0

        # 현재 선택된 행동이 무엇인지 확인하는 변수
        self._currentAction = None

        # 캐릭터가 선택한 대상을 기록하는 변수
        self.TARGET:Character = None
    
    def NAME(self, after:str|None = None):
        if after is None:
            return self.__NAME
        else:
            # 한글 유니코드 범위: 0xAC00 ~ 0xD7A3
            min_code = 0xAC00
            max_code = 0xD7A3

            # 이름의 마지막 글자의 코드값 취득
            final_code = ord(self.__NAME[-1])

            # 판별결과를 기록함 - 받침의 유무를 기록함
            hasFinal = not (final_code < min_code or final_code > max_code or (final_code - min_code) % 28 == 0)

            # 해당되는 받침을 찾음
            afterList = ("은는", "이가", "을를", "과와")
            for afters in afterList:
                # 받침을 찾았으면 받침유무에 따라 최종적으로 사용할 문자를 선택함
                if after in afters:
                    return self.__NAME +  (afters[0] if hasFinal else afters[1])
            # 못찾았으면 그대로 반환
            return self.__NAME + after
    
    def ANAME(self, after:str|None = None):
        if after is None:
            return self.__ANAME
        else:
            # 한글 유니코드 범위: 0xAC00 ~ 0xD7A3
            min_code = 0xAC00
            max_code = 0xD7A3

            # 별명의 마지막 글자의 코드값 취득
            final_code = ord(self.__ANAME[-1])

            # 판별결과를 기록함 - 받침의 유무를 기록함
            hasFinal = not (final_code < min_code or final_code > max_code or (final_code - min_code) % 28 == 0)

            # 해당되는 받침을 찾음
            afterList = ("은는", "이가", "을를", "과와")
            for afters in afterList:
                # 받침을 찾았으면 받침유무에 따라 최종적으로 사용할 문자를 선택함
                if after in afters:
                    return self.__ANAME +  (afters[0] if hasFinal else afters[1])
            # 못찾았으면 그대로 반환
            return self.__ANAME + after
            
    def __str__(self):
        return self.__ANAME
    
    def __add__(self, msg:str):
        if msg[0] == ' ' or msg[:2] == "에게" or msg[:2] == "한테":
            return self.ANAME() + msg
        else:
            return self.ANAME(msg[0]) + msg[1:]
    
    
    
def prepareCharacters(VARSIZE):
    cList = []
    for index in range(VARSIZE["CHARA"]):
        cList.append(Character(index, VARSIZE))
    return cList