import event as event
import MODULE.SystemModule as SM

SYSTEM = SM.System()


def shopCallBack(key):
    global SYSTEM


def setWakeupTime():
    SYSTEM = SM.System()
    print("기상시간설정 인터페이스 준비!")


def purchaseItem():
    SYSTEM = SM.System()
    print("아이템구매 인터페이스 준비!")


def loadData():
    SYSTEM = SM.System()
    print("로딩 인터페이스!")


def saveData():
    SYSTEM = SM.System()
    print("세이브 인터페이스!")


def startShop():
    global SYSTEM
    for i in range(6):
        SYSTEM.delText(i)
    SYSTEM.setText(4, "오늘도 힘쎄고 강한 아침이다!")
    commands = {
        1: ("기상하기", None),
        2: ("기상시간 설정", None),
        3: ("도구구매", None),
        4: ("저장하기", None),
        5: ("불러오기", None),
        6: ("옵션설정", None),
    }
    SYSTEM.input(commands, 10, 1, "left")
    func = {
        1: event.simulation,
        2: setWakeupTime,
        3: purchaseItem,
        4: saveData,
        5: loadData,
        6: lambda: print("테스트5"),
    }
    RESULT = SYSTEM.RESULT

    SYSTEM.after(func[RESULT])
    if RESULT != 1:
        SYSTEM.after(startShop)
