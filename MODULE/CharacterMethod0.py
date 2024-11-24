from typing import Union, Literal
from MODULE.CharacterBase import CharacterBase

# 변수로써 사용시의 편의성을 추가하기 위한 클래스
# - 매직메서드 및 getter, setter, 프로퍼티 데코레이터 등이 여기에 포함됨
class CharacterType0(CharacterBase):
    def name(self, after: Union[str, None] = None, select: Literal["이름", "애칭"] = "애칭") -> str:
        if after is None:
            return self._name[select]
        else:
            # 한글 유니코드 범위: 0xAC00 ~ 0xD7A3
            min_code: int = 0xAC00
            max_code: int = 0xD7A3

            # 이름의 마지막 글자의 코드값 취득
            final_code: int = ord(self._name[select][-1])

            # 판별결과를 기록함 - 받침의 유무를 기록함
            hasFinal: bool = not (
                final_code < min_code
                or final_code > max_code
                or (final_code - min_code) % 28 == 0
            )

            # 해당되는 받침을 찾음
            afterList: tuple[str, ...] = ("은는", "이가", "을를", "과와")
            for afters in afterList:
                # 받침을 찾았으면 받침유무에 따라 최종적으로 사용할 문자를 선택함
                if after in afters:
                    return self._name[select] + (afters[0] if hasFinal else afters[1])
            # 못찾았으면 그대로 반환
            return self._name[select] + after

    def __mod__(self, msg: str) -> str:
        if msg[0] == " " or msg[:2] == "에게" or msg[:2] == "한테":
            return self.name() + msg
        else:
            return self.name(msg[0]) + msg[1:]
