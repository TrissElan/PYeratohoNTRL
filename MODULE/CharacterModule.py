from json import load
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
        self.MAXBASE = getList(-3, VARSIZE["BASE"], result["BASE"])
        self.BASE = getList(-3, VARSIZE["BASE"])
        self.TALENT = getList(-3, VARSIZE["TALENT"], result["TALENT"])
        self.BODY = getList(-3, VARSIZE["BODY"], result["BODY"])
        self.CFLAG = getList(0, VARSIZE["CFLAG"], result["FLAG"])
        self.ABL = getList(0, VARSIZE["ABL"], source = result["ABL"] if "ABL" in result else None)
        self.PARAM = getList(0, VARSIZE["PARAM"])
        self.EXP = getList(0, VARSIZE["EXP"])
        
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
        self.TARGET:int|None = None
    
    def NAME(self, josa:str|None = None):
        if josa == None:
            return self.__NAME
        else:
            base_code, jungsung = 0xAC00, 28
            last_char = self.__NAME[-1]
            # 한글 유니코드 범위: 0xAC00 ~ 0xD7A3
            if base_code <= ord(last_char) <= 0xD7A3:
                char_code = ord(last_char) - base_code
                jongseong = char_code % jungsung
                if jongseong == 0:
                    # 받침이 없는 경우
                    if josa == '은는':
                        return self.__NAME + '는'
                    elif josa == '이가':
                        return self.__NAME + '가'
                    elif josa == '와과':
                        return self.__NAME + '와'
                else:
                    # 받침이 있는 경우
                    if josa == '은는':
                        return self.__NAME + '은'
                    elif josa == '이가':
                        return self.__NAME + '이'
                    elif josa == '와과':
                        return self.__NAME + '과'
            else:
                # 한글이 아닌 경우, 받침이 없다고 간주
                if josa == '은는':
                    return self.__NAME + '는'
                elif josa == '이가':
                    return self.__NAME + '가'
                elif josa == '와과':
                    return self.__NAME + '와'
    
    def ANAME(self, josa:str|None = None):
        if josa == None:
            return self.__ANAME
        else:
            base_code, jungsung = 0xAC00, 28
            last_char = self.__ANAME[-1]
            # 한글 유니코드 범위: 0xAC00 ~ 0xD7A3
            if base_code <= ord(last_char) <= 0xD7A3:
                char_code = ord(last_char) - base_code
                jongseong = char_code % jungsung
                if jongseong == 0:
                    # 받침이 없는 경우
                    if josa == '은는':
                        return self.__NAME + '는'
                    elif josa == '이가':
                        return self.__NAME + '가'
                    elif josa == '와과':
                        return self.__NAME + '와'
                else:
                    # 받침이 있는 경우
                    if josa == '은는':
                        return self.__NAME + '은'
                    elif josa == '이가':
                        return self.__NAME + '이'
                    elif josa == '와과':
                        return self.__NAME + '과'
            else:
                # 한글이 아닌 경우, 받침이 없다고 간주
                if josa == '은는':
                    return self.__NAME + '는'
                elif josa == '이가':
                    return self.__NAME + '가'
                elif josa == '와과':
                    return self.__NAME + '와'
    
def prepareCharacters(VARSIZE):
    cList = []
    for index in range(VARSIZE["CHARA"]):
        cList.append(Character(index, VARSIZE))
    return cList