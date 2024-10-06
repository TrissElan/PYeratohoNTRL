from csv import reader as read
from json import load
from collections import defaultdict
import MODULE.DisplayModule as DM
import MODULE.CharacterModule as CM
import tkinter as tk
import tkinter.font as font
import typing
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
    __instance:typing.Optional["System"] = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(System, cls).__new__(cls, *args, **kwargs)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.__initialize()

    def __initialize(self):
        with open("./DATA/setting1.json", "r", encoding="utf-8") as file:
            self.setting1 = load(file)
        with open("./DATA/setting2.json", "r", encoding="utf-8") as file:
            self.setting2 = load(file)

        with open("./DATA/VARSIZE.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.VARSIZE = {row[0]:int(row[1]) for row in result if row != []}

        # 경험치 명칭 DB 생성
        with open("./DATA/EXP.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.__EXPNAME1 = []
            self.__EXPNAME2 = {}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    self.__EXPNAME1.append(row[3])
                    if row[4] == "EOL":
                        self.__EXPNAME2[row[3]] = None
                    else:
                        self.__EXPNAME2[row[3]] = []
                        for i in range(4, len(row)):
                            self.__EXPNAME2[row[3]].append(row[i])

        # 파라미터 명칭 DB 생성
        with open("./DATA/PARAM.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.__PARAMNAME1 = []
            self.__PARAMNAME2 = {}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    self.__PARAMNAME1.append(row[3])
                    if row[4] == "EOL":
                        self.__PARAMNAME1[row[3]] = None
                    else:
                        self.__PARAMNAME2[row[3]] = []
                        for i in range(4, len(row)):
                            self.__PARAMNAME2[row[3]].append(row[i])

        # 사용할 커맨드 생성 - 객체가 생성된 후 진행함
        self.COM = defaultdict(None)

        with open("./DATA/TALENT.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.TALENTNAME = {}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    self.TALENTNAME[int(row[0])] = row[1]

        with open("./DATA/ABL.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.ABLNAME = {}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    self.ABLNAME[int(row[0])] = row[1]

        with open("./DATA/EQUIP.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.EQUIPNAME = {}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    self.EQUIPNAME[int(row[0])] = row[1]

        with open("./DATA/LV.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.LV = {}
            for row in result:
                self.LV[row[0]] = [int(row[i]) for i in range(1, len(row))]

        self.CHARACTERS:list = None
        self.CLOTHLIST:dict = None
        self.ITEMNAME:dict = None
        self.MASTER:int = None
        self.MAP:dict = None
        self.TIME = 0
        self.GFLAG = [0 for i in range(self.VARSIZE["GFLAG"])]
        self.__format = "{}%s {}%s {}%s {}%s {}%s"%(self.setting2["format"][0], self.setting2["format"][1], self.setting2["format"][2], self.setting2["format"][3], self.setting2["format"][4])

        # UI 셋업
        self.DISPLAY = DM.Display(self.setting1)

        # 구상출력영역은 실제 게임에 접속한 이후부터 우클릭을 통한 출력내용 제거가 가능함 / 그 외에는 불가능함
        self.DISPLAY.textArea[4].bind("<Button-3>", lambda e: self.delText(4) if self.GFLAG[0] == 3 else None)

        self.DISPLAY.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.scheduled_tasks = []
        self._RESULT = tk.IntVar()
        self._RESULT.set(0)
    
    @property
    def timeInfo(self):
        return self.__format.format(self.TIME // 518400, self.TIME % 518400 // 43200 + 1, self.TIME % 43200 // 1440 + 1, self.TIME % 1440 // 60, self.TIME % 60)  
    @property
    def RESULT(self)->int:
        return self._RESULT.get()
    @RESULT.setter
    def RESULT(self, value):
        self._RESULT.set(value)

    # EXPNAME을 조합하여 반환하는 함수 - 첫번째 매개변수는 카테고리, 두번째 매개변수는 부위
    def EXPNAME(self, index1:int, index2:int = None):
        if self.__EXPNAME2[self.__EXPNAME1[index1]] == None or index2 == None:
            return self.__EXPNAME1[index1]
        else:
            return f"{self.__EXPNAME1[index1]}({self.__EXPNAME2[self.__EXPNAME1[index1]][index2]})"
        
    # 출력과 관련된 메서드
    # 줄 긋기
    def drawLine(self, shape, index = 4):
        fontWidth = font.nametofont(self.DISPLAY.textArea[index].cget("font")).measure("-")
        windowWidth = self.DISPLAY.textArea[index].winfo_width()
        self.setText(shape * (windowWidth // fontWidth - 1) + "\n", index)
    
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
    
    # 클릭 가능한 텍스트를 출력하여 입력을 받는 함수
    def input(self, commands:dict, width, col = 4, align = "center")->None:
        # 커맨드 정리
        self.delText(5)

        # 커맨드 출력(태그 부여 전)
        comtext = {key:f"[{key:03d}] - {value[0]}" for key, value in commands.items()}
        current_text = ""
        for i, text in enumerate(comtext.values()):
            current_text += self.fstr(text, width)
            if i % col == col - 1:
                current_text += "\n"
        if current_text[-1] != "\n":
            current_text += "\n"
        
        self.setText(current_text, align, 5)
            
        
        # 출력된 커맨드에 대한 태그 부여 시작
        current_text = self.DISPLAY.textArea[5].get("1.0", "end-1c")
        lines = current_text.split("\n")
        for key, text in comtext.items():
            for line_num, line in enumerate(lines):
                if text in line:
                    start = f"{line_num + 1}.{line.find(text)}"
                    end = f"{line_num + 1}.{line.find(text) + len(text)}"
                    tagName = f"COM{key:03d}"
                    self.DISPLAY.textArea[5].tag_add(tagName, start, end)
                    self.DISPLAY.textArea[5].tag_bind(tagName, "<Enter>", lambda e, tag=tagName: on_enter(e, tag))
                    self.DISPLAY.textArea[5].tag_bind(tagName, "<Leave>", lambda e, tag=tagName: on_leave(e, tag))
                    self.DISPLAY.textArea[5].tag_bind(tagName, "<Button-1>", lambda e, value = key : self._RESULT.set(value))
        self.DISPLAY.root.wait_variable(self._RESULT)

    # 임의선택함수
    def inputr(self, commands:dict)->int:
        key = rd.choice(list(commands.keys()))
        self._RESULT.set(key)

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
            self._RESULT.set(0)
            self.DISPLAY.root.quit()  # 이벤트 루프 중단
            self.DISPLAY.root.destroy()  # 창 닫기
        except Exception as e:
            print(f"Error while closing: {e}")
    
    # 임의난수 생성함수
    def RANDOM(self, count):
        return rd.randrange(0, count)
    
    # 리스트에서 임의의 하나를 뽑아냄
    def CHOICE(Self, lst:list):
        return rd.choice(lst)
    
    # 커맨드 준비함수
    def prepareCommand(self):
        import inspect
        from COMMAND import Category100
        with open("./DATA/TRAIN.csv", "r", encoding="utf-8") as csvFile:    
            result = read(csvFile)
            commands = {int(name[3:]):func for name, func in inspect.getmembers(Category100) if inspect.isfunction(func)}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    cnum = int(row[0])
                    if cnum in commands:
                        self.COM[int(cnum)] = (row[1], commands[cnum])
                    else:
                        self.COM[int(cnum)] = None