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
            SYSTEM.delText(3)
            SYSTEM.delText(4)

            SYSTEM.setText(0, SYSTEM.timeInfo + " / 현재위치 : " + SYSTEM.CHARACTERS[self.current].CFLAG[11].NAME)
            
            IM.showParam(1, SYSTEM.MASTER)
            if SYSTEM.TARGET != None:
                IM.showParam(2, SYSTEM.TARGET)
            
            MM.showMap(SYSTEM.CHARACTERS[self.current].CFLAG[11].ID)

            # 현재 위치에 있는 캐릭터 목록을 출력하고, 선택할 수 있는 메서드
            # -> 함수로 빼자
            char_names = ' | '.join(char.NAME for char in SYSTEM.CHARACTERS[self.current].CFLAG[11].SPACE)
            SYSTEM.setText(4, char_names + "\n", align="top")

            current_text = SYSTEM.DISPLAY.textArea[4].get("1.0", "end-1c")
            start_index = 0
            for i, char in enumerate(SYSTEM.CHARACTERS[self.current].CFLAG[11].SPACE):
                if char == SYSTEM.CHARACTERS[SYSTEM.MASTER]:
                    continue
                start_index = current_text.find(char.NAME, start_index)
                end_index = start_index + len(char.NAME)
                tagName = f"CHAR_{i}"
                SYSTEM.DISPLAY.textArea[4].tag_add(tagName, f"1.{start_index}", f"1.{end_index}")
                SYSTEM.DISPLAY.textArea[4].tag_bind(tagName, "<Enter>", lambda e, tag=tagName: SM.on_enter(e, tag))
                SYSTEM.DISPLAY.textArea[4].tag_bind(tagName, "<Leave>", lambda e, tag=tagName: SM.on_leave(e, tag))
                SYSTEM.DISPLAY.textArea[4].tag_bind(tagName, "<Button-1>", lambda e, target = char: self.select_character(target))
                start_index = end_index + 3  # +3 for the ' | '
            
            SYSTEM.after(0, self.player_action)
        else:
            SYSTEM.after(0, self.npc_actions)
    
    def select_character(self, target):
        SYSTEM.TARGET = SYSTEM.CHARACTERS.index(target)
        SYSTEM.setText(4, f"\n선택된 캐릭터: {SYSTEM.CHARACTERS[SYSTEM.TARGET].NAME}")

    def player_action(self):
        SYSTEM.delButton()

        command = {1: "이동하기",2:"밥먹기",3:"잠자기",4:"대기1",5:"대기2",6:"대기3", 7:"대기4"}
        
        RESULT = SYSTEM.input(command)
        if RESULT == 1:                                                                           
            print(SYSTEM.CHARACTERS[SYSTEM.MASTER].NAME + " : 이동하기")
            COM001.COM001(self.current)
        elif RESULT == 2:
            print(SYSTEM.CHARACTERS[SYSTEM.MASTER].NAME + " : 밥먹기")
        elif RESULT == 3:
            print(SYSTEM.CHARACTERS[SYSTEM.MASTER].NAME + " : 잠자기")
        
        self.current += 1
        SYSTEM.after(0, self.npc_actions)

    def npc_actions(self):
        if self.current < len(SYSTEM.CHARACTERS):
            command = {1: "이동하기",2:"밥먹기",3:"잠자기",4:"대기1",5:"대기2",6:"대기3", 7:"대기4"}
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
