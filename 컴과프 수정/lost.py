#분실물 하나하나를 객체로 하는 클래스. 개별 ui설정, 찾기 기능 여기서 다룸룸

import tkinter as tk
from images import load_image, select_image

from tkinter import messagebox as msg
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
        self.delete_trigger=tk.BooleanVar(value=False,master=self.ml)
        self.frm = ttk.Frame(self.ml)

    def showState(self,mother_frm, mypage=False):
        with open('./login_state.txt','r') as f:
            login_user=f.readline().strip()
        #UI 만들기
        self.frm.destroy()
        style = ttk.Style()
        style.configure( "selfst.TFrame", width=70, height=110, padx=10, pady=10,
                            highlightbackground=["yellow", "blue"][self.state], highlightthickness=5)
        self.frm = ttk.Frame(mother_frm, style = "selfst.TFrame")

        if login_user==self.username:
            ttk.Button(self.frm, text = "delete", command=lambda: delete()).pack()

        def delete():
            self.delete_trigger.set(True)

        ttk.Label(self.frm, text = f"User: {self.username}").pack()
        ttk.Label(self.frm, text=f"Lost Name: {self.name}").pack()
        ttk.Label(self.frm, text=f"Lost Time: {self.time}" if self.state==0 else f"Found Time: {getattr(self,'find_time','')}").pack()
        ttk.Label(self.frm, text=f"Lost Loc: {self.loc}" if self.state==0 else f"Found Loc: {getattr(self,'find_loc','')}").pack()
        ttk.Label(self.frm, text=f"State: {['Not Found','Found'][self.state]}").pack()
        if self.state==0: #Lost상태
            try:
                self.photo = load_image(self.img, self.frm)
                if self.photo:
                    ttk.Label(self.frm, image=self.photo).pack(anchor="w")
                else:
                    ttk.Label(self.frm, text="(No Image)").pack()
            else:
                ttk.Label(self.frm, text="(No Image)").pack()
        else: #Found상태
            if self.found_img_path: #이미지 출력
                self.found_photo = load_image(self.found_img_path, self.frm)
                if self.found_photo:
                    ttk.Label(self.frm, image=self.found_photo).pack(anchor="w")
                else:
                    ttk.Label(self.frm, text="(No Image)").pack()       
            else:
                ttk.Label(self.frm, text="(No Image)").pack()

        
        #찾기 버튼
        if not self.state:
            ttk.Button(self.frm, text="Found", command=self.foundInput).pack()
        if self.check_mine and self.state and login_user==self.username:
            def checked():
                self.check_mine=False
                self.trigger.set(True)
            def send_back():
                self.state=0
                self.trigger.set(True)
            check_button_frm=ttk.Frame(self.frm)
            ttk.Button(check_button_frm, text="It's Mine!", command=checked).grid(row=0,column=0)
            ttk.Button(check_button_frm, text="Not Mine",command=send_back).grid(row=0,column=1)
            check_button_frm.pack()

    #찾기 버튼 눌렀을 때 발동 - 새로운 창과 UI 생성성
    def foundInput(self):
        window = tk.Toplevel(self.ml)
        window.title('Found Input')
        time_frm = ttk.Frame(window)
        ttk.Label(time_frm, text="Found Time:").pack(side=tk.LEFT)
        time_et = tk.Entry(time_frm)
        time_et.pack(side=tk.LEFT)
        time_frm.pack(anchor=tk.W)

        loc_frm = ttk.Frame(window)
        ttk.Label(loc_frm, text="Found Loc:").pack(side=tk.LEFT)
        loc_et = tk.Entry(loc_frm)
        loc_et.pack(side=tk.LEFT)
        loc_frm.pack(anchor=tk.W)

        global found_img_path
        found_img_path=None

        def select_image_int():
            global found_img_path
            found_img_path=select_image()
        ttk.Button(window, text="Select Photo", command=select_image_int).pack()
       
        #찾기 버튼튼
        find_bt=ttk.Button(window, text='Found Submit', command=lambda: (self.setFound(time_et.get(), loc_et.get(), found_img_path), window.destroy()) if found_img_path else warn_no_image())
        find_bt.pack()

        def warn_no_image():
            msg.showwarning('Error','No Image Uploaded! Please upload Image')

    def setFound(self, time, loc, found_img_path):
        self.state = 1
        self.find_time = time
        self.find_loc = loc
        self.found_img_path=found_img_path
        self.trigger.set(True)
        self.data = [self.name,self.find_time,self.find_loc,self.found_img_path,1]
