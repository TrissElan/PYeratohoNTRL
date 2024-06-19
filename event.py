import MODULE.SystemModule as SM
import MODULE.MapModule as MM
import MODULE.CharacterModule as CM
from COMMAND import Category1
import MODULE.InformModule as IM

SYSTEM = SM.System()

class Game:
    def __init__(self):
        global SYSTEM
        self.current = 0
        SYSTEM.after(0, self.game_loop)  # 초기 게임 루프 시작
    
    def select_target(self, target):
        global SYSTEM
        chara:CM.Character = SYSTEM.CHARACTERS[self.current]
        chara.TARGET = target
        SYSTEM.setText(4, f"{SYSTEM.CHARACTERS[self.current].NAME("은는")} {target.NAME()}에게 가까이 다가간다...\n")
        SYSTEM.RESULT = 1000
    
    def showEnvInfo(self):
        global SYSTEM
        chara:CM.Character = SYSTEM.CHARACTERS[self.current]
        target_list = [target for target in chara.CFLAG[11].SPACE if target != chara]
        target_text = ' | '.join(target.NAME() for target in target_list)
        SYSTEM.setText(0, f"{SYSTEM.timeInfo} / 현재위치 : {chara.CFLAG[11].NAME} < {target_text} > ")
    
        current_text = SYSTEM.DISPLAY.textArea[0].get("1.0", "end-1c")
        start_index = 0
        for i, char in enumerate(target_list):
            if char == chara:
                continue
            start_index = current_text.find(char.NAME(), start_index)
            end_index = start_index + len(char.NAME())
            tagName = f"CHAR_{i}"
            SYSTEM.DISPLAY.textArea[0].tag_add(tagName, f"1.{start_index}", f"1.{end_index}")
            SYSTEM.DISPLAY.textArea[0].tag_bind(tagName, "<Enter>", lambda e, tag=tagName: SM.on_enter(e, tag))
            SYSTEM.DISPLAY.textArea[0].tag_bind(tagName, "<Leave>", lambda e, tag=tagName: SM.on_leave(e, tag))
            SYSTEM.DISPLAY.textArea[0].tag_bind(tagName, "<Button-1>", lambda e, target = char : self.select_target(target))
            start_index = end_index + 3  # +3 for the ' | '

    def game_loop(self):
        global SYSTEM
        chara:CM.Character = SYSTEM.CHARACTERS[self.current]
        if chara.TARGET != None:
            if chara.TARGET not in chara.CFLAG[11].SPACE:
                chara.TARGET = None

        if self.current == SYSTEM.MASTER:
            SYSTEM.delText(0)
            SYSTEM.delText(1)
            SYSTEM.delText(2)
            SYSTEM.delText(3)
            SYSTEM.delButton()

            # 0번 텍스트 위젯 - 전역정보 출력
            self.showEnvInfo()

            # 1번 텍스트 위젯 - 아나타의 정보 출력
            IM.showParam(1, chara)

            # 2번 텍스트 위젯 - 선택된 캐릭터가 있을 경우 선택된 캐릭터 출력
            if chara.TARGET != None:
                IM.showParam(2, chara.TARGET)

            # 3번 텍스트 위젯 - 지도 출력
            MM.showMap(chara.CFLAG[11].ID)    

            # 4번 텍스트 위젯은 언제나 최신 내용을 추적함
            SYSTEM.see_end()
            
        SYSTEM.after(0, self.action)
        
    
    def action(self):
        global SYSTEM
        chara:CM.Character = SYSTEM.CHARACTERS[self.current]
        command = {0: "이동하기",1:"밥먹기",2:"잠자기",3:"대기1",4:"대기2",5:"대기3", 6:"대기4"}
        if chara.TARGET != None:
            add_command = {7:"대화하기", 8:"장난치기", 9:"스킨쉽"}
            command.update(add_command)

        
        
        # 플레이어 동작
        if self.current == 0:
            RESULT = SYSTEM.input(command)
        # NPC 동작
        else:
            RESULT = SYSTEM.input(command, isRandom=True)

        # 어느쪽이든 선택한 결과에 따라 커맨드 실행
        if RESULT == 1000:
            SYSTEM.after(0, self.game_loop)
            return
        elif RESULT == 9999:
            return
        else:
            if RESULT == 0:                                                                           
                print(chara.NAME() + " : 이동하기")
                Category1.COM000(chara)
            elif RESULT == 1:
                print(chara.NAME() + " : 밥먹기")
            elif RESULT == 2:
                print(chara.NAME() + " : 잠자기")
            elif RESULT == 7:
                Category1.COM007(chara)

        if self.current == (len(SYSTEM.CHARACTERS) - 1):
            self.current = 0
            SYSTEM.after(0, self.game_loop)  # 플레이어 턴으로 돌아감
        else:
            self.current += 1
            SYSTEM.after(0, self.action)  # 다음 NPC 행동으로 이동

def simulation():
    game = Game()
