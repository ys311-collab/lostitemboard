#분실물 하나하나를 객체로 하는 클래스. 개별 ui설정, 찾기 기능 여기서 다룸룸

import tkinter as tk
from images import load_image

from tkinter import ttk
from ttkthemes import ThemedTk

class Lost: #클래스명명
    def __init__(self, name, time, loc, img_path, username, ml):
        #변수들 지정정
        self.name = name
        self.time = time
        self.loc = loc
        self.img = img_path
        self.ml = ml
        self.state = 0
        self.username = username
        self.check_mine=True
        self.data = [self.name,self.time,self.loc,self.img,0]
        self.trigger=tk.BooleanVar(value=False,master=self.ml)
        self.frm = tk.Frame(self.ml, width=70, height=110, padx=10, pady=10,
                            highlightbackground=["yellow", "blue"][self.state], highlightthickness=5)

    def showState(self,mother_frm, mypage=False):
        #UI 만들기
        self.frm.destroy()
        self.frm = tk.Frame(mother_frm, width=70, height=110, padx=10, pady=10,
                            highlightbackground=["yellow", "blue"][self.state], highlightthickness=5)
        tk.Label(self.frm, text = f"User: {self.username}").pack()
        tk.Label(self.frm, text=f"Lost Name: {self.name}").pack()
        tk.Label(self.frm, text=f"Lost Time: {self.time}" if self.state==0 else f"Found Time: {getattr(self,'find_time','')}").pack()
        tk.Label(self.frm, text=f"Lost Loc: {self.loc}" if self.state==0 else f"Found Loc: {getattr(self,'find_loc','')}").pack()
        tk.Label(self.frm, text=f"State: {['Not Found','Found'][self.state]}").pack()
        if self.img: #이미지 출력
            self.photo = load_image(self.img, self.frm)
            if self.photo:
                tk.Label(self.frm, image=self.photo).pack(anchor="w")
            else:
                tk.Label(self.frm, text="(No Image)").pack()
        else:
            tk.Label(self.frm, text="(No Image)").pack()
        
        #찾기 버튼
        if not self.state:
            tk.Button(self.frm, text="Found", command=self.foundInput).pack()
        if self.check_mine and self.state:
            def checked():
                self.check_mine=False
                self.trigger.set(True)
            def send_back():
                self.state=0
                self.trigger.set(True)
            tk.Button(self.frm, text="It's Mine!", command=checked).pack()
            tk.Button(self.frm, text="Not Mine", command=send_back).pack(side=tk.LEFT)

    #찾기 버튼 눌렀을 때 발동 - 새로운 창과 UI 생성성
    def foundInput(self):
        window = tk.Toplevel(self.ml)
        window.title('Found Input')
        time_frm = tk.Frame(window)
        tk.Label(time_frm, text="Found Time:").pack(side=tk.LEFT)
        time_et = tk.Entry(time_frm)
        time_et.pack(side=tk.LEFT)
        time_frm.pack(anchor=tk.W)

        loc_frm = tk.Frame(window)
        tk.Label(loc_frm, text="Found Loc:").pack(side=tk.LEFT)
        loc_et = tk.Entry(loc_frm)
        loc_et.pack(side=tk.LEFT)
        loc_frm.pack(anchor=tk.W)

        #찾기 버튼튼
        find_bt=tk.Button(window, text='Found Submit', command=lambda: (self.setFound(time_et.get(), loc_et.get()), window.destroy()))
        find_bt.pack()

    def setFound(self, time, loc):
        self.state = 1
        self.find_time = time
        self.find_loc = loc
        self.trigger.set(True)
        self.data = [self.name,self.find_time,self.find_loc,self.img,1]
