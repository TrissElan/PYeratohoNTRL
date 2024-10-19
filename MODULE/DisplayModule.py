import tkinter as tk
import tkinter.font as font


class Display:
    def setup_text_area(
        self, row, column, rowspan, colspan, isImgArea=False
    ):
        area = tk.Text(
            self.root, height=1, width=1, bg="black", fg="white", font=self.font
        )
        area.tag_configure("center", justify="center")
        area.tag_configure("left", justify="left")
        area.tag_configure("right", justify="right")
        area.grid(
            row=row, column=column, rowspan=rowspan, columnspan=colspan, sticky="nsew"
        )

        area.bindtags((str(area), str(self.root), "all"))

        if isImgArea:
            self.imgArea.append(area)
        else:
            self.textArea.append(area)
    
    def create_font_size_buttons(self):
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.grid(row=0, column=0, sticky="nw")

        button_frame.rowconfigure(0, weight=1)
        button_frame.columnconfigure(0, weight=1, uniform="buttons")
        button_frame.columnconfigure(1, weight=1, uniform="buttons")

        increase_button = tk.Button(button_frame, text="+", command=self.increase_font_size, bg="black", fg="white", highlightbackground="white", highlightthickness=1)
        increase_button.grid(row=0, column=0, sticky="nsew")

        decrease_button = tk.Button(button_frame, text="-", command=self.decrease_font_size, bg="black", fg="white", highlightbackground="white", highlightthickness=1)
        decrease_button.grid(row=0, column=1, sticky="nsew")

    def increase_font_size(self):
        self.font_size += 1
        self.update_font_size()

    def decrease_font_size(self):
        if self.font_size > self.min_font_size:
            self.font_size -= 1
            self.update_font_size()

    def update_font_size(self):
        self.font.configure(size=self.font_size)
        for area in self.textArea + self.imgArea:
            area.configure(font=self.font)
        self.root.update_idletasks()  # 레이아웃 업데이트

    def __init__(self, setting):
        

        self.root = tk.Tk()
        self.root.configure(bg="black")
        self.root.title(f"{setting['title']} {setting['version']}")
        self.root.geometry(setting["screen_size"])

        # 메인 윈도우의 최소 크기 제한 : 600 x 570
        self.root.minsize(720, 650)
        self.root.resizable(True, True)

        # 폰트 설정 및 현재 크기와 최소 크기를 반영함
        self.font = font.Font(family=setting["font_name"], size=setting["font_size"])
        self.min_font_size = self.font.cget("size")
        self.font_size = self.min_font_size

        self.imgArea = []
        self.textArea: list[tk.Text] = []

        # 메인 그리드 레이아웃 설정(행/열)
        # ---- 행 설정 ----
        row_settings = [
            (0, 0, 30),   # 1행 : 전역 정보 영역 - 고정된 높이를 가짐
            (1, 1, 160),  # 2행 : 아나타 정보 영역 - 최소 높이를 가짐
            (2, 1, 160),  # 3행 : 환녀의 정보 영역 - 최소 높이를 가짐
            (3, 2, 100),  # 4행
            (4, 2, 100),  # 5행
        ]
        for row, weight, minsize in row_settings:
            self.root.rowconfigure(row, weight=weight, minsize=minsize)

        # ---- 열 설정 ----
        col_settings = [
            (0, 0, 30),   # 1열 : 버튼 영역 - 고정된 너비를 가짐
            (1, 1, 90),   # 2열 : 1열까지 합쳐서 사진 영역이 존재함
            (2, 1, 150),  # 3열
            (3, 1, 150),  # 4열
            (4, 2, 150),  # 5열
            (5, 2, 150),  # 6열
        ]
        for col, weight, minsize in col_settings:
            self.root.columnconfigure(col, weight=weight, minsize=minsize)
        
        # 폰트 크기 조절 버튼 추가 (첫 번째 열의 가장 좌측에 배치)
        self.create_font_size_buttons()

        # 1행 : 전역 정보 영역
        self.setup_text_area(
            row=0, column=1, rowspan=1, colspan=5
        )

        # 2행 : 아나타의 정보 영역
        self.setup_text_area(
            row=1,
            column=0,
            rowspan=1,
            colspan=2,
            isImgArea=True,
        )  # 이미지 영역
        self.setup_text_area(
            row=1, column=2, rowspan=1, colspan=2
        )  # 텍스트 영역

        # 3행 : 상대방의 정보 영역
        self.setup_text_area(
            row=2,
            column=0,
            rowspan=1,
            colspan=2,
            isImgArea=True,
        )  # 이미지 영역
        self.setup_text_area(
            row=2, column=2, rowspan=1, colspan=2
        )  # 텍스트 영역

        # 2행과 3행 통합 : 지도 영역
        self.setup_text_area(
            row=1, column=4, rowspan=2, colspan=2
        )

        # 대사 출력 텍스트 (3행 전체를 차지)
        self.setup_text_area(
            row=3, column=0, rowspan=1, colspan=6
        )

        # 마지막 행에 버튼을 출력하는 텍스트 위젯
        self.setup_text_area(
            row=4, column=0, rowspan=1, colspan=6
        )

        # 창 업데이트
        self.root.update()