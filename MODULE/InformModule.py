import MODULE.SystemModule as SM

SYSTEM = SM.System()

def PARAMLV(param, index)->str:
    global SYSTEM
    # PARAM값을 Lv로 변환시켜주기 위한 함수
    # 기준은 아래와 같이 설정하고, 나중에 파일로 빼서 변경이 가능하도록 설정함 0 ~ 10까지 총 11단계
    # 0/1000/2000/4000/8000/16000/32000/64000/128000/256000/512000
    standard = SYSTEM.LV["PARAMLV"]
    if param[index] >= standard[-1]:
        return "Lv.EX"
    elif param[index] >= standard[-2]:
        return "Lv.09"
    elif param[index] >= standard[-3]:
        return "Lv.08"
    elif param[index] >= standard[-4]:
        return "Lv.07"
    elif param[index] >= standard[-5]:
        return "Lv.06"
    elif param[index] >= standard[-6]:
        return "Lv.05"
    elif param[index] >= standard[-7]:
        return "Lv.04"
    elif param[index] >= standard[-8]:
        return "Lv.03"
    elif param[index] >= standard[-9]:
        return "Lv.02"
    elif param[index] >= standard[-10]:
        return "Lv.01"
    else:
        return "Lv.00"

def EXPLV(exp, index)->str:
    global SYSTEM
    # EXP값을 Lv로 변환시켜주기 위한 함수
    # 기준은 아래와 같이 설정하고, 나중에 파일로 빼서 변경이 가능하도록 설정함 0 ~ 10까지 총 11단계
    # 0/25/50/100/200/400/800/1600/3200/6400/12800
    standard = SYSTEM.LV["EXPLV"]
    if exp[index] >= standard[-1]:
        return "Lv.EX"
    elif exp[index] >= standard[-2]:
        return "Lv.09"
    elif exp[index] >= standard[-3]:
        return "Lv.08"
    elif exp[index] >= standard[-4]:
        return "Lv.07"
    elif exp[index] >= standard[-5]:
        return "Lv.06"
    elif exp[index] >= standard[-6]:
        return "Lv.05"
    elif exp[index] >= standard[-7]:
        return "Lv.04"
    elif exp[index] >= standard[-8]:
        return "Lv.03"
    elif exp[index] >= standard[-9]:
        return "Lv.02"
    elif exp[index] >= standard[-10]:
        return "Lv.01"
    else:
        return "Lv.00"

def showParam(CHARA):
    global SYSTEM
    MASTER = SYSTEM.CHARACTERS[SYSTEM.MASTER]
    if CHARA is MASTER:
        area = 1
    else:
        area = 2
    
    line1 = CHARA.NAME % f"HP : [][][]"
    line2 = ""
    line3 = ""
    line4 = ""
    # 내용물 재구성해야 함
    # SYSTEM.setText(area, result)

def showExp(area, chara):
    global SYSTEM
    # 내용물 재구성해야 함
    # SYSTEM.setText(area, result)