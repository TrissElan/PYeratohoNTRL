import sys
sys.path.append('./MODULE')
sys.path.append('./COMMAND')

import MODULE.SystemModule as SM
import prepareEnv as PE

SYSTEM = SM.System()
SYSTEM.prepareCommand()

class StartMenu:
    def __init__(self):
        global SYSTEM
        SYSTEM.after(self.phase0)
        SYSTEM.mainloop()
    
    def phase0(self):
        SYSTEM.delText(4)
        SYSTEM.delText(5)
        SYSTEM.after(self.phase1)

    def phase1(self):
        global SYSTEM
        SYSTEM.drawLine(4, "-")
        SYSTEM.setText(4, "\n" * 4 + SYSTEM.SETTING["ANOUNCE"] + "\n" * 4, "center")
        SYSTEM.drawLine(4, "-")
        SYSTEM.after(self.phase2)
    
    def phase2(self):
        commands = {1:(SYSTEM.SETTING["START"],None), 2:(SYSTEM.SETTING["LOAD"], None)}
        SYSTEM.input(commands, 8, 1)
        SYSTEM.after(self.phase3)
    
    def phase3(self):
        RESULT = SYSTEM.RESULT
        if RESULT == 1:
            SYSTEM.after(PE.preprare)
        elif RESULT == 2:
            SYSTEM.after(self.phase0)

def startGame():
    game = StartMenu()

startGame()