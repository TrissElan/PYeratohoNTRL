import start_simulation
from MODULE.SystemModule import SYSTEM

class ShopPhase:
    def __init__(self):
        self.__commands = {
            1: "기상하기",
            2: "기상시간 설정",
            3: "도구구매",
            4: "저장하기",
            5: "불러오기",
            6: "옵션설정",
        }

    def setWakeupTime(self):
        print("기상시간설정 인터페이스 준비!")

    def purchaseItem(self):
        print("아이템구매 인터페이스 준비!")

    def loadData(self):
        print("로딩 인터페이스!")

    def saveData(self):
        print("세이브 인터페이스!")
    
    def start(self):
        SYSTEM.clearImgArea()
        SYSTEM.clearTextArea()
        SYSTEM.after(self.phase1)

    def phase0(self):
        for i in range(6):
            SYSTEM.delText(i)
        SYSTEM.after(self.phase1)
    
    def phase1(self):
        SYSTEM.setText("오늘도 힘쎄고 강한 아침이다!")
        SYSTEM.after(self.phase2)
    
    def phase2(self):
        SYSTEM.input(self.__commands, width=10, col=1, align="left")
        SYSTEM.after(self.phase3)

    def phase3(self):
        if SYSTEM.result == 1:
            SYSTEM.after(start_simulation.main)
        else:
            if SYSTEM.result == 2:
                SYSTEM.after(self.setWakeupTime)
            elif SYSTEM.result == 3:
                SYSTEM.after(self.purchaseItem)
            elif SYSTEM.result == 4:
                SYSTEM.after(self.saveData)
            elif SYSTEM.result == 5:
                SYSTEM.after(self.loadData)
            elif SYSTEM.result == 6:
                print("테스트중")
            SYSTEM.after(self.phase0)

def main():
    shop = ShopPhase()
    shop.start()
