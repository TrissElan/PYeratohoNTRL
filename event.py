import MODULE.SystemModule as SM
import MODULE.MapModule as MM
import random as rd
from COMMAND import COM001
import MODULE.InformModule as IM

SYSTEM = SM.System()

class Game:
    global SYSTEM
    def __init__(self):
        self.current = 0
        SYSTEM.after(0, self.game_loop)  # 초기 게임 루프 시작

    def game_loop(self):
        if self.current == 0:
            SYSTEM.delText(0)
            SYSTEM.delText(1)
            SYSTEM.delText(2)
            MM.showMap(SYSTEM.CHARACTERS[self.current].CFLAG[11].ID)
            SYSTEM.setText(0, SYSTEM.timeInfo)
            IM.showParam(1, SYSTEM.MASTER)
            SYSTEM.setText(2, "선택된 환녀/방문자/최면좌의 정보 출력")
            IM.showExp(4, self.current)
            SYSTEM.after(0, self.player_action)
        else:
            SYSTEM.after(0, self.npc_actions)
    
    def player_action(self):
        SYSTEM.setText(0, " / 현재위치 : " + SYSTEM.CHARACTERS[self.current].CFLAG[11].NAME)
        SYSTEM.delButton()

        command = {1: "이동하기",2:"밥먹기",3:"잠자기",4:"대기1",5:"대기2",6:"대기3", 7:"대기4"}
        
        RESULT = SYSTEM.input(command)
        if RESULT == 1:                                                                           
            print(SYSTEM.CHARACTERS[self.current].NAME + " : 이동하기")
            COM001.COM001(self.current)
        elif RESULT == 2:
            print(SYSTEM.CHARACTERS[self.current].NAME + " : 밥먹기")
        elif RESULT == 3:
            print(SYSTEM.CHARACTERS[self.current].NAME + " : 잠자기")
        
        self.current += 1
        SYSTEM.after(0, self.npc_actions)

    def npc_actions(self):
        if self.current < len(SYSTEM.CHARACTERS):
            command = {1: "이동하기",2:"밥먹기",3:"잠자기"}
            RESULT = rd.choice(list(command.keys()))
            if RESULT == 1:
                print(SYSTEM.CHARACTERS[self.current].NAME + " : 이동하기")
                COM001.COM001(self.current)
            elif RESULT == 2:
                print(SYSTEM.CHARACTERS[self.current].NAME + " : 밥먹기")
            elif RESULT == 3:
                print(SYSTEM.CHARACTERS[self.current].NAME + " : 잠자기")
            
            self.current += 1
            SYSTEM.after(0, self.npc_actions)  # 다음 NPC 행동으로 이동
        else:
            self.current = 0
            SYSTEM.after(0, self.game_loop)  # 플레이어 턴으로 돌아감

def simulation():
    game = Game()
