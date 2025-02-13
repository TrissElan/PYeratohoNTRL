import sys
sys.path.append("./MODULE")
sys.path.append("./COMMAND")

from MODULE.SystemModule import SYSTEM
import start_from_zero

class StartMenu:
    def __init__(self):
        self.__commands = {
            1: SYSTEM.setting2["start"],
            2: SYSTEM.setting2["load"],
        }

    def start(self):
        SYSTEM.after(self.phase0)
        SYSTEM.mainloop()
        
    def phase0(self):
        SYSTEM.clearImgArea()
        SYSTEM.clearTextArea()
        SYSTEM.after(self.phase1)

    def phase1(self):
        SYSTEM.drawLine("-")
        SYSTEM.setText(SYSTEM.setting2["message"], "center")
        SYSTEM.drawLine("-")
        SYSTEM.after(self.phase2)

    def phase2(self):
        SYSTEM.input(self.__commands, width=8, col=1)
        SYSTEM.after(self.phase3)

    def phase3(self):
        if SYSTEM.result == 1:
            SYSTEM.after(start_from_zero.main)
        else:
            SYSTEM.after(self.phase0)

def main():
    game = StartMenu()
    game.start()

if __name__ == "__main__":
    main()
