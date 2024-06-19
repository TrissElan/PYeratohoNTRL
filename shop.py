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

def shop():
    global SYSTEM
    for i in range(5): SYSTEM.delText(i)
    SYSTEM.delButton()
    SYSTEM.setText(4, "오늘도 힘쎄고 강한 아침이다!")
    command = {
        1:"기상하기",
        2:"기상시간 설정",
        3:"도구구매",
        4:"저장하기",
        5:"불러오기",
        6:"옵션설정"
    }
    RESULT = SYSTEM.input(command)
    function = {
        1:event.simulation,
        2:setWakeupTime,
        3:purchaseItem,
        4:saveData,
        5:loadData,
        6:lambda:print("테스트5")
    }
    function[RESULT]()
    if RESULT == 1:
        SYSTEM.delText(4)
        SYSTEM.DISPLAY.textArea[4].bind("<Button-3>", lambda e: SYSTEM.delText(4))
    if RESULT != 1:
        SYSTEM.after(0, shop)