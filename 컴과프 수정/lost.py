#분실물 하나하나를 객체로 하는 클래스. 개별 ui설정, 찾기 기능 여기서 다룸룸

import tkinter as tk
from images import load_image

class Lost: #클래스명명
    def __init__(self, name, time, loc, img, board_l, board_f, ml):
        #변수들 지정정
        self.name = name
        self.time = tuple(time.split('.'))
        self.loc = loc
        self.img = img
        self.board = [board_l, board_f]
        self.ml = ml
        self.state = 0
        self.trigger=tk.BooleanVar(value=False,master=self.ml)
        self.frm = tk.Frame(self.board[self.state], width=70, height=110, padx=10, pady=10,
                            highlightbackground=["yellow", "blue"][self.state], highlightthickness=5)

    def showState(self):
        #UI 만들기
        self.frm.destroy()
        self.frm = tk.Frame(self.board[self.state], width=70, height=110, padx=10, pady=10,
                            highlightbackground=["yellow", "blue"][self.state], highlightthickness=5)
        tk.Label(self.frm, text=f"분실물 이름: {self.name}").pack()
        tk.Label(self.frm, text=f"시간: {self.time[0]}:{self.time[1]}" if self.state==0 else f"찾은 시간: {getattr(self,'find_time','')}").pack()
        tk.Label(self.frm, text=f"위치: {self.loc}" if self.state==0 else f"찾은 위치: {getattr(self,'find_loc','')}").pack()
        tk.Label(self.frm, text=f"상태: {['못 찾음','찾음'][self.state]}").pack()
        if self.img: #이미지 출력
            photo = load_image(self.img)
            if photo:
                tk.Label(self.frm, image=photo).pack(anchor="w")
                self.photo = photo
            else:
                tk.Label(self.frm, text="(이미지 없음)").pack()
        else:
            tk.Label(self.frm, text="(이미지 없음)").pack()
        
        #찾기 버튼
        tk.Button(self.frm, text="찾음", command=self.foundInput).pack()

    #찾기 버튼 눌렀을 때 발동 - 새로운 창과 UI 생성성
    def foundInput(self):
        window = tk.Toplevel(self.ml)
        window.title('찾음 입력')
        time_frm = tk.Frame(window)
        tk.Label(time_frm, text="찾은 시간:").pack(side=tk.LEFT)
        time_et = tk.Entry(time_frm)
        time_et.pack(side=tk.LEFT)
        time_frm.pack(anchor=tk.W)

        loc_frm = tk.Frame(window)
        tk.Label(loc_frm, text="찾은 위치:").pack(side=tk.LEFT)
        loc_et = tk.Entry(loc_frm)
        loc_et.pack(side=tk.LEFT)
        loc_frm.pack(anchor=tk.W)

        #찾기 버튼튼
        find_bt=tk.Button(window, text='찾음 등록', command=lambda: (self.setFound(time_et.get(), loc_et.get()), window.destroy()))
        find_bt.pack()

    def setFound(self, time, loc):
        self.state = 1
        self.find_time = time
        self.find_loc = loc
        self.trigger.set(True)
