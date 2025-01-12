from json import load
from collections import defaultdict
import MODULE.DisplayModule as DM
import tkinter as tk
import tkinter.font as font
import random as rd
import unicodedata

def on_enter(e, tag=None):
    if tag == None:
        e.widget['foreground'] = 'yellow'  # 버튼에 대한 효과
    else:
        e.widget.tag_config(tag, foreground = 'yellow') # 태그에 대한 효과

def on_leave(e, tag=None):
    if tag == None:
        e.widget['foreground'] = 'white'
    else:
        e.widget.tag_config(tag, foreground = 'white')

# 싱글톤 패턴 클래스 : 클래스의 전역변수로 접근함
class System:
    __instance:"System" = None
    __initialized = False
    time_standard = [518400, 43200, 1440, 60]

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__class__.__initialized:
            return
        else:
            self.__class__.__initialized = True
            self.__initialize()

    def __initialize(self):
        with open("./DATA/setting1.json", "r", encoding="utf-8") as file:
            self.setting1 = load(file)
        with open("./DATA/setting2.json", "r", encoding="utf-8") as file:
            self.setting2 = load(file)

        # 사용할 커맨드 생성 - 객체가 생성된 후 진행함
        self.COMMAND = defaultdict(None)
        self.CHARACTERS:list = None
        self.CLOTHLIST:dict = None
        self.ITEMNAME:dict = None
        self.MASTER:int = None
        self.MAP:dict = None
        self.GFLAG = [0 for i in range(100)]

        # UI 셋업 - 구상출력영역은 실제 게임에 접속한 이후부터 우클릭을 통한 출력내용 제거가 가능함 / 그 외에는 불가능함
        self.DISPLAY = DM.Display(self.setting1)
        self.DISPLAY.textArea[4].bind("<Button-3>", lambda e: self.delText(4) if self.GFLAG[0] == 3 else None)
        self.DISPLAY.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.scheduled_tasks = []

        # 시간 변수 준비
        self.time = 0
        self.__format = "{}%s {}%s {}%s {}%s {}%s" % tuple(self.setting2["format"])

        # 선택값 저장 변수 준비
        self.__result = tk.IntVar()
        self.__result.set(0)
        self.__input_processed = False  # 입력 처리 여부를 추적하는 플래그
    
    @property
    def timeInfo(self):
        minute = self.time
        times = []
        for unit in self.time_standard:
            times.append(minute // unit)
            minute %= unit
        times.append(minute)
        return self.__format.format(*times)

    @property
    def result(self)->int:
        return self.__result.get()
    @result.setter
    def result(self, value):
        self.__result.set(value)
        
    # 출력과 관련된 메서드
    
    # 사진 영역
    # - 사진 출력
    def setImage(self, index, img):
        self.DISPLAY.imgArea[index - 1].image_create(tk.END, image = img)
    # - 텍스트 출력
    def addTextAfterImg(self, index, msg, align='left'):
        self.DISPLAY.imgArea[index - 1].insert("end", "\n" + msg, align)
    # - 사진 제거
    def delImageArea(self, index):
        self.DISPLAY.imgArea[index - 1].delete("1.0", tk.END)
    # - 사진 영역 클리어
    def clearImgArea(self):
        for imgArea in self.DISPLAY.imgArea:
            imgArea.delete("1.0", tk.END)

    # 텍스트 영역
    # - 줄 긋기
    def drawLine(self, shape, index = 4):
        fontWidth = font.nametofont(self.DISPLAY.textArea[index].cget("font")).measure("-")
        windowWidth = self.DISPLAY.textArea[index].winfo_width()
        self.setText(shape * (windowWidth // fontWidth - 1) + "\n", index)

    # - 텍스트 출력
    def setText(self, msg, align='left', index = 4):
        self.DISPLAY.textArea[index].insert("end", msg, align)
    # - 텍스트 삭제
    def delText(self, index):
        self.DISPLAY.textArea[index].delete("1.0", tk.END)   
    # - 텍스트 영역 클리어
    def clearTextArea(self):
        for textArea in self.DISPLAY.textArea:
            textArea.delete("1.0", tk.END)
    # - 텍스트 포맷팅
    def fstr(self, text, size):
        text = str(text)
        width = 0
        for char in text:
            if unicodedata.east_asian_width(char) in 'FWA':
                width += 2  # 전각 문자는 너비를 2로 계산
            else:
                width += 1  # 반각 문자는 너비를 1로 계산
        space = size - width
        return text + ' ' * space
    
    def __handle_click(self, value):
        """입력값을 한 번만 처리하는 핸들러"""
        if not self.__input_processed:
            self.__input_processed = True
            self.__result.set(value)
    
    # 클릭 가능한 텍스트를 출력하여 입력을 받는 함수
    def __format_command_text(self, commands: dict[int, str], width: int = 20, col: int = 4) -> str:
        """커맨드 텍스트를 포맷팅하는 내부 메서드"""
        formatted = {key: f"[{key:03d}] - {text}" for key, text in commands.items()}
        result = ""
        for i, text in enumerate(formatted.values()):
            result += self.fstr(text, width)
            if i % col == col - 1:
                result += "\n"
        if not result.endswith("\n"):
            result += "\n"
        return result

    def __add_command_tags(self, commands: dict[int, str]) -> None:
        """커맨드 텍스트에 태그를 추가하는 내부 메서드"""
        text_widget = self.DISPLAY.textArea[5]
        current_text = text_widget.get("1.0", "end-1c")
        lines = current_text.split("\n")
        
        for key, text in commands.items():
            formatted_text = f"[{key:03d}] - {text}"
            for line_num, line in enumerate(lines):
                if formatted_text in line:
                    start = f"{line_num + 1}.{line.find(formatted_text)}"
                    end = f"{line_num + 1}.{line.find(formatted_text) + len(formatted_text)}"
                    tag_name = f"COM{key:03d}"
                    
                    text_widget.tag_add(tag_name, start, end)
                    text_widget.tag_bind(tag_name, "<Enter>", lambda e, tag=tag_name: on_enter(e, tag))
                    text_widget.tag_bind(tag_name, "<Leave>", lambda e, tag=tag_name: on_leave(e, tag))
                    text_widget.tag_bind(tag_name, "<Button-1>", lambda e, value=key: self.__handle_click(value))

    def input(self, commands: dict[int, str], width: int = 20, col: int = 4, align: str = "center") -> None:
        """클릭 가능한 커맨드 메뉴를 표시하고 사용자 입력을 기다림"""
        self.__input_processed = False
        self.delText(5)
        
        # 커맨드 텍스트 포맷팅 및 출력
        formatted_text = self.__format_command_text(commands, width, col)
        self.setText(formatted_text, align, 5)
        
        # 태그 추가
        self.__add_command_tags(commands)
        
        # 입력 대기
        self.DISPLAY.root.wait_variable(self.__result)

    def inputr(self, commands: dict[int, str]) -> None:
        """임의의 커맨드를 선택"""
        self.__result.set(rd.choice(list(commands.keys())))

    # 이벤트루트를 시작하는 메서드
    def mainloop(self):
        self.DISPLAY.root.mainloop()
    
    # UI요소 업데이트용
    def update(self):
        self.DISPLAY.root.update()
    
    # 출력된 텍스트의 가장 최신으로 자동으로 스크롤
    def see_end(self):
        self.DISPLAY.textArea[4].see("end")
    
    # 이벤트함수 예약메서드
    def after(self, func, ms:int = 0):
        task_id = self.DISPLAY.root.after(ms, func)
        self.scheduled_tasks.append(task_id)
        return task_id
    
    # 종료시에 실행되는 자원정리 메서드들
    def cancel_all_tasks(self):
        for task_id in self.scheduled_tasks:
            self.DISPLAY.root.after_cancel(task_id)
        self.scheduled_tasks.clear()

    def on_closing(self):
        try:
            self.cancel_all_tasks()  # 추가: 모든 예약된 작업 취소
            self.__result.set(0)
            self.DISPLAY.root.quit()  # 이벤트 루프 중단
            self.DISPLAY.root.destroy()  # 창 닫기
        except Exception as e:
            print(f"Error while closing: {e}")
    
    # 임의난수 생성함수
    def random(self, count):
        return rd.randrange(0, count)
    
    # 리스트에서 임의의 하나를 뽑아냄
    def choice(Self, lst:list):
        return rd.choice(lst)

SYSTEM = System()
