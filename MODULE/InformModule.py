import MODULE.SystemModule as SM

SYSTEM = SM.System()

def PARAMLV(param)->str:
    global SYSTEM
    # PARAM값을 Lv로 변환시켜주기 위한 함수
    # 기준은 아래와 같이 설정하고, 나중에 파일로 빼서 변경이 가능하도록 설정함 0 ~ 10까지 총 11단계
    # 0/1000/2000/4000/8000/16000/32000/64000/128000/256000/512000
    standard = SYSTEM.LV["PARAMLV"]
    if param >= standard[-1]:
        return "LvEX"
    elif param >= standard[-2]:
        return "Lv09"
    elif param >= standard[-3]:
        return "Lv08"
    elif param >= standard[-4]:
        return "Lv07"
    elif param >= standard[-5]:
        return "Lv06"
    elif param >= standard[-6]:
        return "Lv05"
    elif param >= standard[-7]:
        return "Lv04"
    elif param >= standard[-8]:
        return "Lv03"
    elif param >= standard[-9]:
        return "Lv02"
    elif param >= standard[-10]:
        return "Lv01"
    else:
        return "Lv00"

def EXPLV(exp)->str:
    global SYSTEM
    # EXP값을 Lv로 변환시켜주기 위한 함수
    # 기준은 아래와 같이 설정하고, 나중에 파일로 빼서 변경이 가능하도록 설정함 0 ~ 10까지 총 11단계
    # 0/25/50/100/200/400/800/1600/3200/6400/12800
    standard = SYSTEM.LV["EXPLV"]
    if exp >= standard[-1]:
        return "Lv.EX"
    elif exp >= standard[-2]:
        return "Lv.09"
    elif exp >= standard[-3]:
        return "Lv.08"
    elif exp >= standard[-4]:
        return "Lv.07"
    elif exp >= standard[-5]:
        return "Lv.06"
    elif exp >= standard[-6]:
        return "Lv.05"
    elif exp >= standard[-7]:
        return "Lv.04"
    elif exp >= standard[-8]:
        return "Lv.03"
    elif exp >= standard[-9]:
        return "Lv.02"
    elif exp >= standard[-10]:
        return "Lv.01"
    else:
        return "Lv.00"

def BASELV(base)->str:
    if base >= 750:
        return "MAX"
    elif base >= 500:
        return "MED"
    elif base >= 250:
        return "MIN"
    else:
        return "EMP"

def ELECTLV(elect)->str:
    if elect == 0:
        return "무발기"
    elif elect <= 250:
        return "약간 발기함"
    elif elect <= 500:
        return "발기했음"
    elif elect <= 750:
        return "눈에 보임"
    else:
        return "풀발기"

def showParam(CHARA, area):
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]

    # 기본정보 설정
    BaseInfo = CHARA % f" - HP : [{SYSTEM.fstr(CHARA.PARAM[0][0][0],4)}/{SYSTEM.fstr(CHARA.PARAM[0][0][1],4)}] MP : [{SYSTEM.fstr(CHARA.PARAM[0][1][0],4)}/{SYSTEM.fstr(CHARA.PARAM[0][1][1],4)}]\n"

    # 추가정보1
    AddInfo1 = ""
    # - 남성이나 후타나리이면 정액수치 출력
    if CHARA.TALENT[0] >= 1:
        AddInfo1 += f"정액 : [{SYSTEM.fstr(CHARA.PARAM[1][0][0],4)}/{SYSTEM.fstr(CHARA.PARAM[1][0][1],4)}] | "
    # - 여성이나 후타나리이면 모유수치 출력
    if CHARA.TALENT[0] != 1:
        # - 단, 모유수치가 None이 아닌 경우에만 가능함
        if CHARA.PARAM[1][1][0] is not None:
            AddInfo1 += f"모유 : [{SYSTEM.fstr(CHARA.PARAM[1][1][0],4)}/{SYSTEM.fstr(CHARA.PARAM[1][1][1],4)}] | "
    # - 기본적으로 시오/소변/대변 정보 출력(옵션에서 선택 가능하게 될 예정)
    AddInfo1_3 = f"시오 : [{SYSTEM.fstr(CHARA.PARAM[1][2][0],4)}/{SYSTEM.fstr(CHARA.PARAM[1][2][1],4)}] | "
    AddInfo1_4 = f"소변욕구 : [{BASELV(CHARA.PARAM[1][3][0])}] | "
    AddInfo1_5 = f"대변욕구 : [{BASELV(CHARA.PARAM[1][4][0])}]"
    AddInfo1 += AddInfo1_3 + AddInfo1_4 + AddInfo1_5
    AddInfo1 += "\n"

    # 추가정보2
    AddInfo2 = ""
    # - 남성이나 후타나리이면 클리가 아닌 자지로 출력됨
    if CHARA.TALENT[0] >= 1:
        name = "자지"
    else:
        name = "클리"
    AddInfo2 += f"{name}상태 : {SYSTEM.fstr(ELECTLV(CHARA.PARAM[2][0][0]),6)} 유두상태 : {SYSTEM.fstr(ELECTLV(CHARA.PARAM[2][1][0]),6)}\n"

    # 추가정보3
    AddInfo3 = ""
    # - 남성 및 후타나리는 P로 바꿔서 표현하고 여성은 C로 표현함
    if CHARA.TALENT[0] >= 1:
        name = "P"
    else:
        name = "C"
    AddInfo3 += f"{name} : {PARAMLV(CHARA.PARAM[3][0])} | "
    # - 여성 및 후타나리는 보지가 있음
    if CHARA.TALENT[0] != 1:
        AddInfo3 += f"V : {PARAMLV(CHARA.PARAM[3][1])} | "
    AddInfo3 += f"A : {PARAMLV(CHARA.PARAM[3][2])} | "
    AddInfo3 += f"B : {PARAMLV(CHARA.PARAM[3][3])} | "
    AddInfo3 += f"M : {PARAMLV(CHARA.PARAM[3][4])}"
    # - 여성 및 후타나리는 자궁이 있음
    if CHARA.TALENT[0] != 1:
        AddInfo3 += f" | W : {PARAMLV(CHARA.PARAM[3][5])}\n"
    else:
        AddInfo3 += "\n"
    result = BaseInfo + AddInfo1 + AddInfo2 + AddInfo3

    # 추가정보4 / 5는 상호작용중인 캐릭터에 대한 정보로써 출력됨
    # - 해당 캐릭터가 나에 대해 어떻게 느끼고, 나는 대상 캐릭터에 대해 어떻게 느끼는지가 출력됨

    TARGET = None
    if CHARA is not MASTER:
        TARGET = MASTER
    elif MASTER.TARGET is not None:
        TARGET = MASTER.TARGET
    
    if TARGET is not None:
        # 추가정보4 - 긍정수치
        AddInfo4 = f"호의 : {PARAMLV(CHARA.PARAM[4][TARGET][0])} | 굴복 : {PARAMLV(CHARA.PARAM[4][TARGET][1])} | 수용 : {PARAMLV(CHARA.PARAM[4][TARGET][2])} | 욕정 : {PARAMLV(CHARA.PARAM[4][TARGET][3])} | 노출 : {PARAMLV(CHARA.PARAM[4][TARGET][4])}\n"
        # 추가정보5 - 부정수치
        AddInfo5 = f"적의 : {PARAMLV(CHARA.PARAM[5][TARGET][0])} | 반항 : {PARAMLV(CHARA.PARAM[5][TARGET][1])} | 거부 : {PARAMLV(CHARA.PARAM[5][TARGET][2])} | 고통 : {PARAMLV(CHARA.PARAM[5][TARGET][3])} | 수치 : {PARAMLV(CHARA.PARAM[5][TARGET][4])}\n"
        result += TARGET % "에 대한 감정\n" + AddInfo4 + AddInfo5
    
    result = result.replace("None", "----")

    SYSTEM.setText(area, result)

def showExp(area, chara):
    global SYSTEM
    # 내용물 재구성해야 함
    # SYSTEM.setText(area, result)