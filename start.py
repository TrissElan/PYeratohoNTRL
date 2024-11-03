import sys
sys.path.append("./MODULE")
sys.path.append("./COMMAND")

from MODULE.SystemModule import SYSTEM
import start_from_zero as SZ

SYSTEM.prepareCommand()


class StartUp:
    def __init__(self):
        SYSTEM.result = 0
        SYSTEM.clearImgArea()
        SYSTEM.clearTextArea()
       
    def start(self):
        SYSTEM.after(self.phase0)
        SYSTEM.mainloop()

    def phase0(self):
        SYSTEM.delText(4)
        SYSTEM.delText(5)
        SYSTEM.after(self.phase1)

    def phase1(self):
        SYSTEM.drawLine("-")
        SYSTEM.setText(SYSTEM.setting2["message"], "center")
        SYSTEM.drawLine("-")
        SYSTEM.after(self.phase2)

    def phase2(self):
        commands = {
            1: (SYSTEM.setting2["start"], None),
            2: (SYSTEM.setting2["load"], None),
            3: (SYSTEM.setting2["exit"], None),
        }
        SYSTEM.input(commands, 8, 1)
        SYSTEM.after(self.phase3)

    def phase3(self):
        if SYSTEM.result == 1:
            SYSTEM.after(SZ.preprare)
        else:
            SYSTEM.after(self.phase0)

    
if __name__ == "__main__":
    game = StartUp()
    game.start()
