import sys
sys.path.append('./MODULE')
sys.path.append('./COMMAND')

import MODULE.SystemModule as SM
import prepareEnv as PE

SYSTEM = SM.System()

def startMenu():
    global SYSTEM
    SYSTEM.setText(4, "\n" * 4)
    SYSTEM.drawLine(4, "-")
    SYSTEM.setText(4, "\n" * 4)
    SYSTEM.setText(4, SYSTEM.SETTING["ANOUNCE"]+"\n\n\n", "center")
    SYSTEM.drawLine(4, "-")
    SYSTEM.setText(4, "\n" * 4)

    command = {1:SYSTEM.SETTING["START"], 2:SYSTEM.SETTING["LOAD"]}

    RESULT = SYSTEM.input(command, align = "n")
    if RESULT == 1:
        PE.prepareEnv()
    elif RESULT == 2:
        print("로딩기능!")
    
    SYSTEM.mainloop()

startMenu()
