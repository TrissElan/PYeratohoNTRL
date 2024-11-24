from typing import Optional, List
from MODULE.CharacterMethod0 import CharacterType0
from MODULE.SystemModule import SYSTEM

# 캐릭터 정보에 대한 규격화된 인터페이스를 제공하기 위한 메서드
# - 이 클래스에서 각종 정보확인 메서드 등을 정의함
class CharacterType1(CharacterType0):
    def short_info(self, area: int) -> None:
        player_name: str = SYSTEM.CHARACTERS[SYSTEM.MASTER].name(select="이름")
        target_name: Optional[str] = None if self.target is None else self.target.name(select="이름")

        # 이미지 영역에 출력할 정보
        SYSTEM.setImage(area, self._img)
        tmp: List[str] = []
        for i in range(3):
            tmp.append(
                f"{self.base[i].name} : {SYSTEM.fstr(self.base[i].data.current,4)}/{SYSTEM.fstr(self.base[i].data.max,4)}"
            )
        tmp_str: str = "\n".join(tmp)
        SYSTEM.addTextAfterImg(area, tmp_str)

        base_info: str = f"□ {self.name(select="이름")}"
        # 1) 캐릭터가 선택한 대상과의 관계수치
        if target_name is not None:
            base_info += f"(호감 : {self.attr[player_name].data.current} | 신뢰 : {self.trst[player_name].data.current} | 관계 : {self.subm[player_name].data.current})\n"

        # 2) 캐릭터의 욕구
        base_info += "□ 생리적 욕구\n"
        tmp = []
        for i in range(3, 6):
            if self.base[i].isValid:
                tmp.append(
                    f"{self.base[i].name} : {SYSTEM.fstr(self.base[i].data.current,4)}/{SYSTEM.fstr(self.base[i].data.max,4)}"
                )
        tmp_str = "|".join(tmp)
        base_info += tmp_str + "\n"

        # 3) 캐릭터의 신체 상태
        base_info += "□ 신체상태 : 공사중\n"

        # 4) 캐릭터가 선택한 대상에 대한 감정 정보
        if target_name is not None:
            base_info += f"□ {player_name}에 대한 감정\n"
            tmp = []
            for i in range(7):
                tmp.append(
                    f"{self.mood[player_name][i].name} : {self.mood[player_name][i].data.current}"
                )
            tmp_str = "|".join(tmp)
            base_info += tmp_str + "\n"

        # 4) 쾌감 정보
        base_info += "□ 누적쾌감\n"
        tmp = []
        for i in range(6):
            if self.plsr[i].isValid:
                tmp.append(f"{self.plsr[i].name} : {self.plsr[i].data.current}")
        tmp_str = "|".join(tmp)
        base_info += tmp_str + "\n"

        SYSTEM.setText(base_info, index=area)

    def full_info(self) -> None:
        pass
