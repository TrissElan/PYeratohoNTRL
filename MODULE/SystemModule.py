from csv import reader as read
import MODULE.DisplayModule as DM
import tkinter as tk
import tkinter.font as font
import typing

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
        with open("./DATA/VARSIZE.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.VARSIZE = {row[0]:int(row[1]) for row in result if row != []}
        with open("./DATA/SETTING.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.SETTING = {}
            for row in result:
                if row[0] not in self.SETTING:
                    self.SETTING[row[0]] = row[1]
                else:
                    self.SETTING[row[0]] += "\n" + row[1]
        
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
        with open("./DATA/EXP.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.EXPNAME = {}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    self.EXPNAME[int(row[0])] = row[1]
        with open("./DATA/EQUIP.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.EQUIPNAME = {}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    self.EQUIPNAME[int(row[0])] = row[1]
        with open("./DATA/BASE.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.BASENAME = {}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    self.BASENAME[int(row[0])] = row[1]
        with open("./DATA/PARAM.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.PARAMNAME = {}
            for row in result:
                if row == [] or row[0] == "" or row[0].startswith(";"):
                    continue
                else:
                    self.PARAMNAME[int(row[0])] = row[1]
        with open("./DATA/LV.csv", "r", encoding="utf-8") as csvFile:
            result = read(csvFile)
            self.LV = {}
            for row in result:
                self.LV[row[0]] = [int(row[i]) for i in range(1, len(row))]

        self.CHARACTERS = None
        self.CLOTHLIST = None
        self.ITEMNAME = None
        self.MASTER = None
        self.TARGET = None
        self.MAP = None
        self.TIME = 0
        self.FLAG = [0 for i in range(self.VARSIZE["GFLAG"])]
        self.__format = "{}%s {}%s {}%s {}%s {}%s"%(self.SETTING['YEAR'], self.SETTING['MONTH'], self.SETTING['DAY'], self.SETTING['HOUR'], self.SETTING['MIN'])

        # 게임 시스템 관리를 위한 기믹 / 변수들
        self.DISPLAY = DM.Display(self.SETTING)
        self.DISPLAY.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.scheduled_tasks = [] 
        self.__RESULT = tk.IntVar()
        self.__RESULT.set(0)
    
    @property
    def timeInfo(self):
        return self.__format.format(self.TIME // 518400, self.TIME % 518400 // 43200 + 1, self.TIME % 43200 // 1440 + 1, self.TIME % 1440 // 60, self.TIME % 60)
    @property
    def RESULT(self)->int:
        return self.__RESULT.get()
    @RESULT.setter
    def RESULT(self, intValue:int):
        self.__RESULT.set(intValue)
    
    # 버튼 관리 및 텍스트 관리 메서드
    def setButton(self, func, msg, position = 'top', align = 'w', xyfill = 'y'):
        button = tk.Button(self.DISPLAY.bArea, command=func, text=msg, bg="black", fg="white", font=self.DISPLAY.font, borderwidth=0, highlightthickness=0)
        button.pack(side=position, fill=xyfill, anchor = align, padx = 1, pady = 0)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    def delButton(self):
        for instance in self.DISPLAY.bArea.winfo_children():
            instance.destroy()
    def drawLine(self, index, shape):
        fontWidth = font.nametofont(self.DISPLAY.textArea[index].cget("font")).measure("-")
        windowWidth = self.DISPLAY.textArea[index].winfo_width()
        self.setText(index, shape * (windowWidth // fontWidth - 1) + "\n")
    def setText(self, index, msg, align='left'):
        self.DISPLAY.textArea[index].insert("end", msg, align)
    def delText(self, index):
        self.DISPLAY.textArea[index].delete("1.0", tk.END)

    # 이벤트루트를 시작하는 메서드
    def mainloop(self):
        self.DISPLAY.root.mainloop()
    
    # UI요소 업데이트용
    def update(self):
        self.DISPLAY.root.update()
    
    # 이벤트함수 예약메서드
    def after(self, ms:int, func):
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
            self.RESULT = 0
            self.DISPLAY.root.quit()  # 이벤트 루프 중단
            self.DISPLAY.root.destroy()  # 창 닫기
        except Exception as e:
            print(f"Error while closing: {e}")
    
    # 입력을 대체하는 메서드
    def input(self, command:dict, positon = "top", align = "w", ):
        for key, msg in command.items():
            self.setButton(lambda value = key: self.__RESULT.set(value), msg, positon, align)
        self.DISPLAY.root.wait_variable(self.__RESULT)
        return self.RESULT
