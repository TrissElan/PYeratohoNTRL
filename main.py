import sys
sys.path.append('./MODULE')
sys.path.append('./COMMAND')

import MODULE.SystemModule as SM
import prepareEnv as PE

SYSTEM = SM.System()

class StartMenu:
    def __init__(self):
        global SYSTEM
        self.menu()
        SYSTEM.mainloop()

    def menu(self):
        global SYSTEM
        SYSTEM.delText(4)
        SYSTEM.delButton()
        
        SYSTEM.setText(4, "\n" * 5)
        SYSTEM.drawLine(4, "-")
        SYSTEM.setText(4, "\n" * 4 + SYSTEM.SETTING["ANOUNCE"] + "\n" * 4, "center")
        SYSTEM.drawLine(4, "-")

        self.action()
    
    def action(self):
        command = {1:SYSTEM.SETTING["START"], 2:SYSTEM.SETTING["LOAD"]}
        RESULT = SYSTEM.input(command, align = "n")
        if RESULT == 1:
            SYSTEM.after(0,PE.prepareEnv)
        elif RESULT == 2:
            SYSTEM.after(0,self.menu)
  
game = StartMenu()
