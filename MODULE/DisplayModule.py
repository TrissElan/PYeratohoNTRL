import tkinter as tk
import tkinter.font as font

class Display:
    def setup_text_area(self, root, height, width, defaultFont):
        textArea = tk.Text(root, height=height, width=width, bg="black", fg="white", font=defaultFont)
        textArea.tag_configure("center", justify='center')
        textArea.tag_configure("left", justify='left')
        textArea.tag_configure("right", justify='right')
        self.textArea.append(textArea)

    def __init__(self, setting):
        self.root = tk.Tk()
        self.root.configure(bg="black")
        self.root.title(f"{setting['TITLE']} {setting['VERSION']}")
        self.root.geometry(setting['SIZE'])
        self.root.resizable(bool(int(setting["RESIZEW"])), bool(int(setting["RESIZEH"])))
        self.font = font.Font(family=setting["FONTNAME"], size=setting["FONTSIZE"], weight=setting["FONTWEIGHT"])
        
        self.textArea:list[tk.Text] = []
        
        # root를 2개로 나눔 : frame1(top)과 frame2(bottom)
        frame1 = tk.Frame(self.root, height = 1, bg="black")
        frame1.pack(side='top', fill='both')
        frame2 = tk.Frame(self.root, bg="black")
        frame2.pack(side='top', fill='both')

        # frame1에 전역정보를 위한 텍스트위젯 추가
        self.setup_text_area(frame1, 1, 100, self.font)
        self.textArea[0].pack(side='top', fill='x', padx=0, pady=0, expand=True)
    
        # frame2를 다시 나눔 : frame21(top)과 frame22(bottom)
        frame21 = tk.Frame(frame2, bg="black")
        frame21.pack(side='top', fill='both', expand=True)
        frame22 = tk.Frame(frame2, bg="black")
        frame22.pack(side='bottom', fill='both', expand=True)

        # frame21를 다시 나눔 : frame211(left)와frame212(right)
        frame211 = tk.Frame(frame21, bg="black")
        frame211.pack(side='left', fill='both', expand=True)
        frame212 = tk.Frame(frame21, bg="black")
        frame212.pack(side='right', fill='both', expand=True)
    
        # frame211의 상단에는 아나타의 정보 출력 텍스트위젯
        self.setup_text_area(frame211, 9, 64, self.font)
        self.textArea[1].pack(side='top', fill='both', padx=0, pady=0, expand=True)
        # frame211의 하단에는 선택한 캐틱터의 정보 출력 텍스트위젯
        self.setup_text_area(frame211, 9, 64, self.font)
        self.textArea[2].pack(side='bottom', fill='both', padx=0, pady=0, expand=True)
        # frame212 전체에는 맵 정보 출력 텍스트 위젯
        self.setup_text_area(frame212, 18, 36, self.font)
        self.textArea[3].pack(side='top', fill='both', padx=0, pady=0, expand=True)

        # frame22를 다시 나눔 : frame221(top)과 frame222(bottom) 
        frame221 = tk.Frame(frame22, bg="black")
        frame221.pack(side='top', fill='x', expand=True)
        frame222 = tk.Frame(frame22, bg="black")
        frame222.pack(side='top', fill='both', expand=True)
    
        # frame221은 대사 출력을 위한 텍스트위젯
        self.setup_text_area(frame221, 21, 100, self.font)
        self.textArea[4].pack(side='top', fill='both', padx=0, pady=0)
        
        # frame222는 클릭할 버튼을 출력하기 위한 텍스트위젯
        self.setup_text_area(frame222, 60, 100, self.font)
        self.textArea[5].pack(side='top', fill='both', padx=0, pady=0)

        self.root.update()