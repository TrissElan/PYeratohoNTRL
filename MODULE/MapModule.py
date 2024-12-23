import MODULE.SystemModule as SM
from collections import deque
import re


class Node:
    def __init__(self, name, id=None, desc=""):
        self.ID = id
        self.__name = name
        self.smell = None
        self.stain = None
        self.link = []
        self.space = []

    def name(self, after: str | None = None):
        if after is None:
            return self.__name
        else:
            # 한글 유니코드 범위: 0xAC00 ~ 0xD7A3
            min_code = 0xAC00
            max_code = 0xD7A3

            # 별명의 마지막 글자의 코드값 취득
            t_code = ord(self.__name[-1])

            # 판별결과를 기록함 - 받침의 유무를 기록함
            hasFinal = not (
                t_code < min_code or t_code > max_code or (t_code - min_code) % 28 == 0
            )

            # 판별이 필요한 것인지 확인함
            if after not in "으로":
                return self.__name + after
            else:
                # 판별이 필요한 것이면 구별해서 자동 선택됨
                return self.__name + ("으로" if hasFinal else "로")
            
    def __contains__(self, chara):
        return chara in self.space

    def __str__(self):
        return f"{self.name()} ({self.smell}, {self.stain})"

    def __mod__(self, msg: str = None):
        if msg[0] == "로":
            return self.name(msg[0]) + msg[1:]
        elif msg[:2] == "으로":
            return self.name(msg[:2]) + msg[2:]
        else:
            return self.name() + msg


def generateMap():
    # 외부 영역 / 6개 | // 10 == 0
    floorE = {
        0: Node("저택 정문", 0),
        1: Node("정원", 1),
        2: Node("홍 메이링의 방", 2),
        3: Node("외부 화장실", 3),
        4: Node("외부 창고", 4),
        5: Node("저택 뒷문", 5),
    }

    # 지하 영역 / 7개 | // 10 == 1
    floor0 = {
        10: Node("1/지하 계단", 10),
        11: Node("지하복도", 11),
        12: Node("감옥1", 12),
        13: Node("감옥2", 13),
        14: Node("플랑도르 개인실", 14),
        15: Node("탈의실", 15),
        16: Node("대욕탕", 16),
    }

    # 1층 영역 / 9 + 중복1 | // 10 == 2
    floor1 = {
        20: Node("1층 복도", 20),
        21: Node("주방", 21),
        22: Node("식당", 22),
        23: Node("응접실", 23),
        24: Node("1층 화장실", 24),
        25: Node("도서관", 25),
        26: Node("파츄리 개인실", 26),
        27: Node("소악마 개인실", 27),
        28: Node("1/2층계단", 28),
        10: floor0[10],
    }

    # 2층 영역 / 6 + 중복1 | // 10 == 3
    floor2 = {
        30: Node("2층 복도", 30),
        31: Node("아나타 개인실", 31),
        32: Node("사쿠야 개인실", 32),
        33: Node("2층 화장실", 33),
        34: Node("메이드 대기소", 34),
        35: Node("2/3층 계단", 35),
        28: floor1[28],
    }
    # 3층 영역 / 2 + 중복1 | // 10 == 4
    floor3 = {
        40: Node("레밀리아 개인실", 40),
        41: Node("발코니", 41),
        35: floor2[35],
    }

    # 외부영역 맵핑
    floorE[0].link = [floorE[1], floorE[2], floorE[3]]
    floorE[1].link = [floorE[0], floorE[2], floorE[3], floor1[20]]
    floorE[2].link = [floorE[0], floorE[1], floorE[5]]
    floorE[3].link = [floorE[0], floorE[4], floorE[1]]
    floorE[4].link = [floorE[3], floorE[5]]
    floorE[5].link = [floorE[2], floorE[4], floor1[21]]

    # 지하 맵핑
    floor0[10].link = [floor1[20], floor0[11]]
    floor0[11].link = [floor0[10], floor0[12], floor0[13], floor0[14], floor0[15]]
    floor0[12].link = [floor0[11]]
    floor0[13].link = [floor0[11]]
    floor0[14].link = [floor0[11]]
    floor0[15].link = [floor0[11], floor0[16]]
    floor0[16].link = [floor0[15]]

    # 1층 맵핑
    floor1[20].link = [
        floor1[23],
        floor1[24],
        floor1[22],
        floor1[21],
        floor1[25],
        floor1[28],
        floor1[10],
        floorE[1],
    ]
    floor1[21].link = [floorE[5], floor1[20], floor1[22]]
    floor1[22].link = [floor1[21], floor1[20]]
    floor1[23].link = [floor1[24], floor1[20]]
    floor1[24].link = [floor1[23], floor1[20]]
    floor1[25].link = [floor1[20], floor1[26], floor1[27]]
    floor1[26].link = [floor1[25]]
    floor1[27].link = [floor1[25]]
    floor1[28].link = [floor1[20], floor2[30]]

    # 2층 맵핑
    floor2[30].link = [
        floor2[31],
        floor2[32],
        floor2[33],
        floor2[34],
        floor2[28],
        floor2[35],
    ]
    floor2[31].link = [floor2[30]]
    floor2[32].link = [floor2[30]]
    floor2[33].link = [floor2[30]]
    floor2[34].link = [floor2[30]]
    floor2[35].link = [floor2[30], floor3[40]]

    # 3층 맵핑
    floor3[40].link = [floor3[35], floor3[41]]
    floor3[41].link = [floor3[40]]

    # 랜덤으로 찍어서 이동하기 위한 목록 준비
    mapList = {}
    mapList.update(floorE)
    mapList.update(floor0)
    mapList.update(floor1)
    mapList.update(floor2)
    mapList.update(floor3)
    return mapList


def getRoute(start_node: Node, goal_node: Node):
    queue = deque([[start_node]])  # 큐에 시작 노드 객체로 초기화
    visited = set()
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal_node:
            route = [n for n in path]  # 경로의 노드 이름을 리스트로 반환
            route.reverse()
            return route
        if node not in visited:
            visited.add(node)
            for linked_node in node.link:
                if linked_node not in visited:
                    new_path = list(path)
                    new_path.append(linked_node)
                    queue.append(new_path)
    return None  # 경로를 찾지 못했을 경우


def showMap(currentLocation: int):
    SYSTEM = SM.System()
    SYSTEM.delText(3)
    # 계단에서 이동할 때 현재 문제가 있는데, 해당 층에서 벗어날 방법이 없다는 것
    # - 별도의 변수로 층전환을 시도하거나, 이전에 있던 위치의 ID값을 활용하여 보여주는 방식을 전환하도록 설계하자
    if currentLocation // 10 == 0 or currentLocation // 10 == 2:
        mapData = """■───────────────────────────────■
│□□□□□□□□□□□□□□05□□□□□□□□□□□□□■■■│
│□□□□■■■■■■■■■■□■■■■■■■■■■■■□■04■│
│□□□□■□□□□□□□21□□■10□■□□□■□□□■□□■■│
│□□□□■□22□■□■■■■■■■□■□26□■□27□■□□□□│
│□□□□■□□□■□□□◀28▶□□□■□□□■□□□■□□□□│
│□□□□■■□■■□□□□□□□□□■■□■■■□■■□□□□│
│□□□□■□□□□□□□□□20□□□■□□□□□□□■□□□□│
│□□□□■□□□□□□□□□□□□□□□□□□□□□■□□□□│
│□□□□■□■□■■■■■■■□■■■■□□□25□□■□□□□│
│□□□□■24■□23□□■□□□□□□□■□□□□□□■□□□□│
│■■■□■□■□□□□■□□□01□□□■□□□□□□■□■■■│
│■02□□■■■■■■■■□□□□□□□■■■■■■■■□□03■│
│■■■□□□□□□□□□□□□□□□□□□□□□□□□□■■■│
■───────────────00───────────────■"""
    elif currentLocation // 10 == 3:
        mapData = """■───────────────────────────────■
│□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□│
│□□□□■■■■■■■■■■■■■■■■■■■■■■■□□□□│
│□□□□■□□□■□□□□□□□□□□□□□□□■□■□□□□│
│□□□□■□31□■□■■■■■■■□□□□□□□■33■□□□□│
│□□□□■□□□■□□□◀28▶□□□□□□□□□□□■□□□□│
│□□□□■■□■■□■■■■■■■□□□□□□■■■■□□□□│
│□□□□■□□□□□□□□30□□□□□□□□□◀35▶■□□□□│
│□□□□■■□■■□□□□□□□□□□■□■■■■■■□□□□│
│□□□□■□□□■□□■■■■■■■■■□□□□□□■□□□□│
│□□□□■□32□■□□■□□□□□□□■□□□34□□■□□□□│
│□□□□■□□□■□□■□□□□□□□■□□□□□□■□□□□│
│□□□□■■■■■■■■□□□□□□□■■■■■■■■□□□□│
│□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□│
■───────────────────────────────■"""
    elif currentLocation // 10 == 4:
        mapData = """■───────────────────────────────■
│□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□│
│□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□│
│□□□□□□□□□□□□□□□□■■■□□□□□□□□□□□□│
│□□□□□□□□□□□□□□□■□□□■□□□□□□□□□□□│
│□□□□□□□□□□□□□□■□□□□□■□□□□□□□□□□│
│□□□□□□□□□□□□□■□□□40□□□■■■■■■□□□□│
│□□□□□□□□□□□□□■□□□□□□□□□◀35▶■□□□□│
│□□□□□□□□□□□□□■□■■□■■□■■■■■■□□□□│
│□□□□□□□□□□□□□□■□□□□□■□□□□□□□□□□│
│□□□□□□□□□□□□□□□■□41□■□□□□□□□□□□□│
│□□□□□□□□□□□□□□□□■■■□□□□□□□□□□□□│
│□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□│
│□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□│
■───────────────────────────────■"""
    else:
        mapData = """■■■■■■■■■■
■□10▶■■□□□■
■□■■■■□15□■
■□□□11□□□□■
■■■□■■■■□■
■12□□■□□□□■
■□■□■□□□□■
■■■□■□□□□■
■13□□■□□□□■
■□■□■□16□□■
■■■□■□□□□■
■□□□■□□□□■
■□14□■□□□□■
■□□□■□□□□■
■■■■■■■■■■"""

    SYSTEM.setText(3, mapData)

    lines = mapData.split("\n")
    SYSTEM.DISPLAY.textArea[3].tag_config("gray", foreground="gray")
    for i, line in enumerate(lines):
        start = 0
        while start != -1:
            start = line.find("□", start)
            if start != -1:
                start_index = f"{i+1}.{start}"
                end_index = f"{i+1}.{start+1}"
                SYSTEM.DISPLAY.textArea[3].tag_add("gray", start_index, end_index)
                start += 1

    lines = mapData.split("\n")
    locations = {}
    pattern = re.compile(r"\d\d")
    for indeY, line in enumerate(lines):
        for match in re.finditer(pattern, line):
            locations[match.group()] = (indeY + 1, match.start())

    # 이 태그는 나중에 캐릭터 상태에 따라서 이동가능/불가능일 때 붙여주거나 붙지 않도록 설계하자
    # 그냥 쓸 경우, 예상치 못한 이동이 발생하게 됨
    for loc, (row, col) in locations.items():
        start_index = f"{row}.{col}"
        end_index = f"{row}.{col+2}"
        SYSTEM.DISPLAY.textArea[3].tag_add(loc, start_index, end_index)
        SYSTEM.DISPLAY.textArea[3].tag_bind(
            loc, "<Enter>", lambda e, tag=loc: SM.on_enter(e, tag)
        )
        SYSTEM.DISPLAY.textArea[3].tag_bind(
            loc, "<Leave>", lambda e, tag=loc: SM.on_leave(e, tag)
        )
        if int(loc) in SYSTEM.MAP:
            SYSTEM.DISPLAY.textArea[3].tag_bind(
                loc,
                "<Button-1>",
                lambda e, chara=0, dest=SYSTEM.MAP[int(loc)]: print(chara, dest.NAME),
            )
