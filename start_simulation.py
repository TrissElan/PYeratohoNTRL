import MODULE.SystemModule as SM
import MODULE.MapModule as MM
from MODULE.CharacterBase import CharacterBase
from MODULE.CharacterMethod0 import CharacterType0
from MODULE.CharacterMethod1 import CharacterType1
from MODULE.CharacterMethod2 import CharacterType2
from MODULE.CharacterFinal import Character

from MODULE.SystemModule import SYSTEM


class Simulation:
    def __init__(self):
        self.__current = 0

        SYSTEM.GFLAG[0] = 3

        # 정보출력을 위한 임시옵션 설정
        SYSTEM.GFLAG[-6] = True
        SYSTEM.GFLAG[-5] = True
        SYSTEM.GFLAG[-4] = True
        SYSTEM.GFLAG[-3] = True
        SYSTEM.GFLAG[-2] = True
        SYSTEM.GFLAG[-1] = True

    @property
    def master(self) -> Character:
        return SYSTEM.CHARACTERS[SYSTEM.MASTER]

    @property
    def current_player(self) -> Character:
        return SYSTEM.CHARACTERS[self.current]

    @property
    def current(self) -> int:
        return self.__current

    def next_turn(self):
        self.__current += 1
        if self.__current >= len(SYSTEM.CHARACTERS):
            self.__current = 0

    def current_info(self):
        try:
            self.current_player  # CHARA = SYSTEM.CHARACTERS[self.current]
            self.current_player.currL  # PLACE = CHARA.currL

            # 현재 캐릭터를 제외한 같은 장소의 캐릭터들 리스트
            others = [
                other
                for other in self.current_player.currL.space
                if other != self.current_player
            ]

            # 기본 정보 표시
            location_info = (
                f"{SYSTEM.timeInfo} / 현재위치 : {self.current_player.currL.name()}"
            )

            # 다른 캐릭터가 있을 경우에만 추가 정보 표시
            if others:
                target_text = " | ".join(other.name() for other in others)
            else:
                target_text = ""
            location_info += f" < {target_text} > "

            SYSTEM.setText(location_info, index=0)

            # 다른 캐릭터가 있을 경우에만 태그 처리
            if others:
                text_widget = SYSTEM.DISPLAY.textArea[0]
                current_text = text_widget.get("1.0", "end-1c")

                # < 기호 이후부터 처리 시작
                start_pos = current_text.find("<")
                if start_pos != -1:
                    start_pos += 1  # < 다음 위치부터 시작

                    for i, char in enumerate(others):
                        char_name = char.name()
                        name_start = current_text.find(char_name, start_pos)

                        if name_start != -1:
                            name_end = name_start + len(char_name)
                            tag_name = f"CHAR_{i}"

                            # 태그 추가 및 바인딩
                            text_widget.tag_add(
                                tag_name, f"1.{name_start}", f"1.{name_end}"
                            )

                            text_widget.tag_bind(
                                tag_name,
                                "<Enter>",
                                lambda e, tag=tag_name: SM.on_enter(e, tag),
                            )
                            text_widget.tag_bind(
                                tag_name,
                                "<Leave>",
                                lambda e, tag=tag_name: SM.on_leave(e, tag),
                            )
                            text_widget.tag_bind(
                                tag_name, "<Button-1>", (lambda e, target = char : self.select_target(target))
                            )

                            start_pos = name_end + 3  # 다음 이름 검색을 위해 위치 이동
        except Exception as e:
            SYSTEM.setText(f"정보 표시 중 오류 발생: {str(e)}\n")

    def select_target(self, other: Character):
        if self.current_player.target == other:
            pass
        else:
            self.current_player.target = other
            if self.master in other.currL.space:
                msg = self.current_player.name() % "는 "
                if other.target is None:
                    msg += other.name() % "에게 가까이 다가간다...\n"
                elif other.target == self.current_player:
                    msg += " 자신을 바라보고 있는 " + other.name() % "에게 시선을 돌렸다.\n"
                else:
                    msg += other.name() % "과" + other.target.name() % "의 사이에 끼어들었다!\n"
                SYSTEM.setText(msg)

    def check_target(self):
        if self.current_player.target is not None:
            if self.current_player.target not in self.current_player.currL.space:
                self.current_player.target = None

    def start(self):
        SYSTEM.after(self.phase0)

    def phase0(self):
        SYSTEM.clearImgArea()
        SYSTEM.clearTextArea()
        SYSTEM.after(self.phase1)

    def phase1(self):
        self.check_target()
        
        if self.current_player == self.master:
            self.current_info()
            MM.showMap(self.current_player.currL.ID)
            self.current_player.short_info(1)
            if self.current_player.target is not None:
                self.current_player.target.short_info(2)

        else:
            others = [
                other
                for other in self.current_player.currL.space
                if other != self.current_player
            ]
            if SYSTEM.random(3) == 1 and others:
                self.select_target(SYSTEM.choice(others))

        SYSTEM.after(self.phase2)

    def phase2(self):
        if self.current_player == self.master:
            SYSTEM.input(SYSTEM.COM, 20, 5, "left")
        else:
            SYSTEM.inputr(SYSTEM.COM)

        SYSTEM.after(self.phase3)

    def phase3(self):
        CHARA = SYSTEM.CHARACTERS[self.current]

        if SYSTEM.COM[SYSTEM.result] is None and SYSTEM.result != 0:
            SYSTEM.setText(4, "명령어가 구현되어 있지 않습니다.\n")
        else:
            SYSTEM.COM[SYSTEM.result][1](CHARA)

        SYSTEM.after(self.phase4)
        SYSTEM.after(SYSTEM.see_end)

    def phase4(self):
        if SYSTEM.result == 1000:
            self.next_turn()
            SYSTEM.after(self.phase0)
        elif SYSTEM.result == 1001:
            SYSTEM.after(self.phase1)
        elif SYSTEM.result == 1002:
            SYSTEM.after(self.phase2)
        elif SYSTEM.result == 1003:
            SYSTEM.after(self.phase3)
        elif SYSTEM.result == 1004:
            SYSTEM.after(self.phase4)
        else:
            raise Exception(f"RESULT : {SYSTEM.result}")


def main():
    game = Simulation()
    game.start()
