#누군가 잃어버린 것 같은 물건 관리
import tkinter as tk
from images import load_image
from tkinter import ttk
from ttkthemes import ThemedTk

#누군가 일허어버린 물건을 찾아준 물건에 대한 정보 저장 클래스
class LostCAG:
    def __init__(self, name, loc, char ,img_path, username, ml): #변수 지정
        self.name = name
        self.loc = loc
        self.char = char.split('#')[0].strip()
        self.tags = list(map(lambda x: x.strip(), char.split('#')[1:])) #태그 구현현
        self.img = img_path
        self.ml = ml
        self.username=username
        self.retrieved = False  #현재 찾아가지 않은 상태(초기 상태)
        self.data = [self.name, self.loc, self.char, self.tags, self.img]
        self.trigger=tk.BooleanVar(value=False,master=self.ml)
        self.delete_trigger=tk.BooleanVar(value=False,master=self.ml)
        self.del_trc_id=''
        self.trc_id=''
        self.frm = ttk.Frame(self.ml)

    def showState(self,mother_frm):
        with open('./login_state.txt', 'r') as f:
            login_user = f.readline().strip()  #현재 로그인되어 있는 유저 읽어오기

        def retrieval():       #찾아갔을 때 실행되는 함수
            self.retrieved = True
            self.trigger.set(True)


        self.frm.destroy()
        
        self.frm = ttk.Frame(mother_frm)
        
        if login_user==self.username:  #현재 로그인된 유저는 본인이 올린 게시물 삭제 가능한 버튼 보임
            ttk.Button(self.frm, text = "delete", command=lambda: delete()).pack()

        def delete():
            self.delete_trigger.set(True)
        
        #Come and Get 게시판에 보이는 레이블의 텍스트 지정
        ttk.Label(self.frm, text = f"User: {self.username}").pack()
        ttk.Label(self.frm, text=f"Lost: {self.name}").pack()
        ttk.Label(self.frm, text='Come And Get!' if not self.retrieved else f'{login_user} got it').pack(anchor=tk.E)
        ttk.Label(self.frm, text=f"Loc: {self.loc}").pack()
        ttk.Label(self.frm, text=f"{self.char}\n{' '.join(map(lambda x: '#'+x, self.tags))}").pack()

        try: #이미지 출력
            self.photo = load_image(self.img, self.frm)
            if self.photo:
                ttk.Label(self.frm, image=self.photo).pack(anchor="w")
            else: #이미지 없을 때 예외처리리
                ttk.Label(self.frm, text="(No Image)").pack()
        except:
            ttk.Label(self.frm, text="(No Image)").pack()

        #찾아가지 않았을 때
        if not self.retrieved:
            retrieve_bt=ttk.Button(self.frm, text="I Got It!", command=lambda: retrieval())
            retrieve_bt.pack()
