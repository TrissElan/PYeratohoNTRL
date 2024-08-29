import MODULE.SystemModule as SM
import MODULE.MapModule as MM
import MODULE.CharacterModule as CM
import MODULE.InformModule as IM

SYSTEM = SM.System()

class Game:
    def __init__(self):
        global SYSTEM
        self.__current = 0
        self.commands = None
        SYSTEM.GFLAG[0] = 3
        # SYSTEM.delText(4)
        SYSTEM.after(self.phase0)

        # 정보출력을 위한 임시옵션 설정
        SYSTEM.GFLAG[100] = True
        SYSTEM.GFLAG[101] = True
        SYSTEM.GFLAG[102] = True
        SYSTEM.GFLAG[103] = True
        SYSTEM.GFLAG[104] = True
        SYSTEM.GFLAG[105] = True
    
    @property
    def current(self):
        return self.__current
    
    @current.setter
    def current(self, value):
        global SYSTEM
        self.__current = value
        if self.__current == len(SYSTEM.CHARACTERS):
            self.current = 0
    
    def select_target(self, OTHER:CM.Character):
        global SYSTEM

        MASTER:CM.Character = SYSTEM.CHARACTERS[SYSTEM.MASTER]
        CHARA:CM.Character = SYSTEM.CHARACTERS[self.current]

        CHARA.TARGET = OTHER
        if CHARA in MASTER.CFLAG[11].SPACE:
            if OTHER.TARGET == None:
                msg = CHARA % "는 " +  OTHER % "에게 가까이 다가간다...\n"
            elif OTHER.TARGET == CHARA:
                msg = CHARA % "는 자신에게 다가온 " + OTHER % "에게 시선을 돌렸다.\n"
            else:
                msg = CHARA % "는 "  + OTHER.TARGET % "과 " + OTHER % " 사이에 끼어들었다!\n"
            SYSTEM.setText(4, msg)
        if self.current == SYSTEM.MASTER:
            SYSTEM.delText(1)
            SYSTEM.delImageArea(1)
            SYSTEM.delText(2)
            SYSTEM.delImageArea(2)
            IM.showParam(MASTER, 1)
            IM.showParam(OTHER, 2)
    
    def current_info(self):
        global SYSTEM
        CHARA:CM.Character = SYSTEM.CHARACTERS[self.current]
        PLACE:MM.Node = CHARA.CFLAG[11]

        target_list = [target for target in PLACE.SPACE if target != CHARA]
        target_text = ' | '.join(target.NAME() for target in target_list)

        SYSTEM.setText(0, f"{SYSTEM.timeInfo} / 현재위치 : {PLACE.NAME()} < {target_text} > ")

        current_text = SYSTEM.DISPLAY.textArea[0].get("1.0", "end-1c")
        start_index = current_text.find('<') + 1 
        for i, char in enumerate(target_list):
            if char == CHARA:
                continue
            start_index = current_text.find(char.NAME(), start_index)
            end_index = start_index + len(char.NAME())
            tagName = f"CHAR_{i}"
            SYSTEM.DISPLAY.textArea[0].tag_add(tagName, f"1.{start_index}", f"1.{end_index}")
            SYSTEM.DISPLAY.textArea[0].tag_bind(tagName, "<Enter>", lambda e, tag=tagName: SM.on_enter(e, tag))
            SYSTEM.DISPLAY.textArea[0].tag_bind(tagName, "<Leave>", lambda e, tag=tagName: SM.on_leave(e, tag))
            SYSTEM.DISPLAY.textArea[0].tag_bind(tagName, "<Button-1>", lambda e, target = char : self.select_target(target))
            start_index = end_index + 3  # +3 for the ' | '
    
    # 기본설정
    def phase0(self):
        global SYSTEM
        MASTER:CM.Character = SYSTEM.CHARACTERS[SYSTEM.MASTER]
        CHARA:CM.Character = SYSTEM.CHARACTERS[self.current]

        SYSTEM.RESULT = 0

        # 대상의 존재여부 확인 / 같은 방에 있어야만 선택된 상태로 유지됨
        if CHARA.TARGET != None:
            if CHARA.TARGET not in CHARA.CFLAG[11].SPACE:
                CHARA.TARGET = None
        
        # 대상이 없을 경우 대상을 선택함 / 현재는 33.3% 확률로 선정함
        if CHARA != MASTER and CHARA.TARGET == None and len(CHARA.CFLAG[11].SPACE) > 1:
            RESULT = SYSTEM.RANDOM(3)
            targets = [chara for chara in CHARA.CFLAG[11].SPACE if chara != CHARA]
            if RESULT == 1:
                self.select_target(SYSTEM.CHOICE(targets))

        # 플레이어 턴인지 여부를 확인함
        if self.current == SYSTEM.MASTER:
            SYSTEM.after(self.phase1)
        else:
            SYSTEM.after(self.phase2)

    # 화면에 출력할 정보 준비
    def phase1(self):
        global SYSTEM

        # 최신정보 출력을 위해 기존 내역을 전부 제거함
        SYSTEM.clearImgArea()
        SYSTEM.delText(0)
        SYSTEM.delText(1)
        SYSTEM.delText(2)
        SYSTEM.delText(3)
        # SYSTEM.delText(4)
        SYSTEM.delText(5)
        # SYSTEM.delImageArea(1)
        # SYSTEM.delImageArea(2)

        # 캐릭터와 캐릭터가 상호작용중인 대상 준비
        CHARA:CM.Character = SYSTEM.CHARACTERS[self.current]
        TARGET:CM.Character = CHARA.TARGET

        # 0번 텍스트 위젯 : 시간 및 선택가능한 캐릭터 출력
        self.current_info()

        # 1번 텍스트 위젯 - 아나타의 파라미터 출력
        IM.showParam(CHARA, 1)

        # 2번 텍스트 위젯 - 선택된 캐릭터가 있을 경우 선택된 캐릭터의 파라미터 출력
        if TARGET != None:
            IM.showParam(CHARA.TARGET, 2)
            
        # 3번 텍스트 위젯 - 지도 출력
        MM.showMap(CHARA.CFLAG[11].ID)

        SYSTEM.after(self.phase2)
        
    # 메뉴를 출력하고 입력을 받음 - 사용자 턴일 경우
    def phase2(self):
        global SYSTEM
        if self.current == SYSTEM.MASTER:
            SYSTEM.input(SYSTEM.COM, 20, 5, "left")
        else:
            SYSTEM.inputr(SYSTEM.COM)
        
        SYSTEM.after(self.phase3)
    
    # 선택된 메뉴에 따라 행동을 실행함
    def phase3(self):
        global SYSTEM
        RESULT = SYSTEM.RESULT
        CHARA:CM.Character = SYSTEM.CHARACTERS[self.current]

        if SYSTEM.COM[RESULT] == None and RESULT != 0:
            SYSTEM.setText(4, "명령어가 구현되어 있지 않습니다.\n")
        else:
            SYSTEM.COM[RESULT][1](CHARA)
            
        SYSTEM.after(self.phase4)
        SYSTEM.after(SYSTEM.see_end)
    
    # 커맨드 실행후 결과값에 따라 phase 시작위치를 지정함
    def phase4(self):
        global SYSTEM
        RESULT = SYSTEM.RESULT
        if RESULT == 1001:
            SYSTEM.after(self.phase1)
        elif RESULT == 1002:
            SYSTEM.after(self.phase2)
        elif RESULT == 1003:
            SYSTEM.after(self.phase3)
        elif RESULT == 1004:
            SYSTEM.after(self.phase4)
        else:
            SYSTEM.after(self.phase0)
            self.current += 1

def simulation():
    game = Game()
