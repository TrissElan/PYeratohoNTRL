import tkinter as tk
import tkinter.font as font
from json import load


class Display:
    def setup_text_area(
        self, root, row, column, rowspan, colspan, isImgArea=False
    ):
        area = tk.Text(
            root, height=1, width=1, bg="black", fg="white", font=self.font
        )
        area.tag_configure("center", justify="center")
        area.tag_configure("left", justify="left")
        area.tag_configure("right", justify="right")
        area.grid(
            row=row, column=column, rowspan=rowspan, columnspan=colspan, sticky="nsew"
        )
        if isImgArea:
            self.imgArea.append(area)
        else:
            self.textArea.append(area)

    def __init__(self, setting):
        

        self.root = tk.Tk()
        self.root.configure(bg="black")
        self.root.title(f"{setting['title']} {setting['version']}")
        self.root.geometry(setting["screen_size"])

        # 메인 윈도우의 최소 크기 제한 : 600 x 570
        self.root.minsize(720, 650)
        self.root.resizable(True, True)

        self.font = font.Font(family=setting["font_name"], size=setting["font_size"])

        self.imgArea = []
        self.textArea: list[tk.Text] = []

        # 메인 그리드 레이아웃 설정(행/열)
        # ---- 행 설정 ----
        row_settings = [
            (0, 0, 30),  # 1행 : 전역 정보 영역 - 고정된 높이를 가짐
            (1, 0, 160),  # 2행 : 아나타 정보 영역 - 최소 높이를 가짐
            (2, 0, 160),  # 3행 : 환녀의 정보 영역 - 최소 높이를 가짐
            (3, 1, 100),  # 4행
            (4, 1, 100),  # 5행
        ]
        for row, weight, minsize in row_settings:
            self.root.rowconfigure(row, weight=weight, minsize=minsize)

        # ---- 열 설정 ----
        col_settings = [
            (
                0,
                0,
                120,
            ),  # 1열 : 사진 영역이 존재함 - 고정된 너비를 가지며 변동이 되면 안됨
            (1, 1, 150),  # 2열
            (2, 1, 150),  # 3열
            (3, 0, 150),  # 4열
            (4, 0, 150),  # 5열
        ]
        for col, weight, minsize in col_settings:
            self.root.columnconfigure(col, weight=weight, minsize=minsize)

        # 1행 : 전역 정보 영역
        self.setup_text_area(
            self.root, row=0, column=0, rowspan=1, colspan=5
        )

        # 2행 : 아나타의 정보 영역
        self.setup_text_area(
            self.root,
            row=1,
            column=0,
            rowspan=1,
            colspan=1,
            isImgArea=True,
        )  # 이미지 영역
        self.setup_text_area(
            self.root, row=1, column=1, rowspan=1, colspan=2
        )  # 텍스트 영역

        # 3행 : 상대방의 정보 영역
        self.setup_text_area(
            self.root,
            row=2,
            column=0,
            rowspan=1,
            colspan=1,
            isImgArea=True,
        )  # 이미지 영역
        self.setup_text_area(
            self.root, row=2, column=1, rowspan=1, colspan=2
        )  # 텍스트 영역

        # 2행과 3행 통합 : 지도 영역
        self.setup_text_area(
            self.root, row=1, column=3, rowspan=2, colspan=2
        )

        # 대사 출력 텍스트 (3행 전체를 차지)
        self.setup_text_area(
            self.root, row=3, column=0, rowspan=1, colspan=5
        )

        # 마지막 행에 버튼을 출력하는 텍스트 위젯
        self.setup_text_area(
            self.root, row=4, column=0, rowspan=1, colspan=5
        )

        # 창 업데이트
        self.root.update()
