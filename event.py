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
        self.commands = None
        SYSTEM.GFLAG[0] = 3
        SYSTEM.delText(4)
        self.phase0()
    
    def select_target(self, target):
        global SYSTEM
        chara:CM.Character = SYSTEM.CHARACTERS[self.current]
        chara.TARGET = target
        SYSTEM.setText(4, f"{SYSTEM.CHARACTERS[self.current].NAME("은는")} {target.NAME()}에게 가까이 다가간다...\n")
        SYSTEM._RESULT.set(1000)
    
    def current_info(self):
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
    
    def phase0(self):
        chara:CM.Character = SYSTEM.CHARACTERS[self.current]

        # 대상의 존재여부 확인 / 같은 방에 있어야만 선택된 상태로 유지됨
        if chara.TARGET != None:
            if chara.TARGET not in chara.CFLAG[11].SPACE:
                chara.TARGET = None
        
        # 대상이 없을 경우 대상을 선택함 / 현재는 33.3% 확률로 선정함
        if chara.TARGET == None:
            RESULT = SYSTEM.RANDOM(3)
            if len(chara.CFLAG[11].SPACE) >= 2 and RESULT == 1:
                target_list = [target for target in chara.CFLAG[11].SPACE if target != chara]
                chara.TARGET = target_list[SYSTEM.RANDOM(len(target_list))]
        
        # 사용할 커맨드 준비
        self.commands = {1: "이동하기",2:"밥먹기",3:"잠자기",4:"휴식", 5:"대기"}
        if chara.TARGET != None:
            acommands = {6:"대화하기", 7:"장난치기", 8:"스킨쉽"}
            self.commands.update(acommands)

        # 플레이어 턴인지 여부를 확인함
        if self.current == SYSTEM.MASTER:
            self.phase1()
        else:
            self.phase3()

    def phase1(self):
        global SYSTEM

        # 최신정보 출력을 위해 기존 내역을 전부 제거함
        SYSTEM.delText(0)
        SYSTEM.delText(1)
        SYSTEM.delText(2)
        SYSTEM.delText(3)
        SYSTEM.delText(5)

        chara:CM.Character = SYSTEM.CHARACTERS[self.current]

        # 0번 텍스트 위젯 : 시간 및 선택가능한 캐릭터 출력
        self.current_info()

            # 1번 텍스트 위젯 - 아나타의 파라미터 출력
        IM.showParam(1, chara)

            # 2번 텍스트 위젯 - 선택된 캐릭터가 있을 경우 선택된 캐릭터의 파라미터 출력
        if chara.TARGET != None:
            IM.showParam(2, chara.TARGET)
            
        # 3번 텍스트 위젯 - 지도 출력
        MM.showMap(chara.CFLAG[11].ID)

        self.phase2()
        
    def phase2(self):
        global SYSTEM
        if self.current == SYSTEM.MASTER:
            SYSTEM.input(self.commands, 20, 3, "left")
        
        self.phase3()
        
    def phase3(self):
        global SYSTEM
        if self.current == SYSTEM.MASTER:
            RESULT = SYSTEM.RESULT
        else:
            RESULT = SYSTEM.RANDOM(len(self.commands)) + 1

        if RESULT == 0:
            return
        else:
            if RESULT == 1000:
                self.phase0()
            else:
                chara:CM.Character = SYSTEM.CHARACTERS[self.current]
                func = {
                    1:Category1.COM001,
                    2:lambda chara : print(chara.NAME() + " : 밥먹는 중"),
                    3:lambda chara : print(chara.NAME() + " : 잠자는 중"),
                    4:lambda chara : print(chara.NAME() + " : 휴식하는 중"),
                    5:lambda chara : print(chara.NAME() + " : 대기중 중"),
                }
                if chara.TARGET != None:
                    afunc = {
                        6:Category1.COM006,
                        7:lambda chara : print(chara.NAME() + " : 장난치는 중"),
                        8:lambda chara : print(chara.NAME() + " : 스킨쉽을 즐기는 중"),
                    }
                    func.update(afunc)
                
                func[RESULT](chara)
            
                self.current += 1
                if self.current == (len(SYSTEM.CHARACTERS) - 1):
                    self.current = 0
                SYSTEM.see_end()
                self.phase0()

def simulation():
    game = Game()
