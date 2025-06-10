#누군가 잃어버린 것 같은 물건 관리
#누군가 잃어버린 것 같은 물건 관리
import tkinter as tk
from images import load_image
from tkinter import ttk
from ttkthemes import ThemedTk

class LostCAG:
    def __init__(self, name, loc, char ,img_path, username, ml):
        #변수들 지정정
        self.name = name
        self.loc = loc
        self.char = char.split('#')[0].strip()
        self.tags = list(map(lambda x: x.strip(), char.split('#')[1:]))
        self.img = img_path
        self.ml = ml
        self.username=username
        self.retrieved = False
        self.data = [self.name, self.loc, self.char, self.tags]
        self.trigger=tk.BooleanVar(value=False,master=self.ml)
        self.delete_trigger=tk.BooleanVar(value=False,master=self.ml)
        self.del_trc_id=''
        self.trc_id=''
        self.frm = ttk.Frame(self.ml)

    def showState(self,mother_frm):
        #찾기 버튼
        with open('./login_state.txt', 'r') as f:
            login_user = f.readline().strip()

        def retrieval():
            self.retrieved = True
            self.trigger.set(True)

        #UI 만들기
        self.frm.destroy()
        
        self.frm = ttk.Frame(mother_frm)
        
        if login_user==self.username:
            ttk.Button(self.frm, text = "delete", command=lambda: delete()).pack()

        def delete():
            self.delete_trigger.set(True)
        
        ttk.Label(self.frm, text = f"User: {self.username}").pack()
        ttk.Label(self.frm, text=f"Lost: {self.name}").pack()
        ttk.Label(self.frm, text='Come And Get!' if not self.retrieved else f'{login_user} got it').pack(anchor=tk.E)
        ttk.Label(self.frm, text=f"Loc: {self.loc}").pack()
        ttk.Label(self.frm, text=f"{self.char}\n{' '.join(map(lambda x: '#'+x, self.tags))}").pack()
        try: #이미지 출력
            self.photo = load_image(self.img, self.frm)
            if self.photo:
                ttk.Label(self.frm, image=self.photo).pack(anchor="w")
            else:
                ttk.Label(self.frm, text="(No Image)").pack()
        except:
            ttk.Label(self.frm, text="(No Image)").pack()

        if not self.retrieved:
            retrieve_bt=ttk.Button(self.frm, text="I Got It!", command=lambda: retrieval())
            retrieve_bt.pack()
