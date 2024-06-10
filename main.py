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
    SYSTEM.setButton(lambda:PE.prepareEnv(), SYSTEM.SETTING["START"], align='n')
    SYSTEM.setButton(lambda:print("테스트2!"), SYSTEM.SETTING["LOAD"], align='n')
    SYSTEM.mainloop()

startMenu()
