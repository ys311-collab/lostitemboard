#누군가 잃어버린 것 같은 물건 관리
import tkinter as tk
from images import load_image

class LostCAG:
    def __init__(self, name, loc, char ,img_path, ml):
        #변수들 지정정
        self.name = name
        self.loc = loc
        self.char = char.split('#')[0].strip()
        self.tags = list(map(lambda x: x.strip(), char.split('#')[1:]))
        self.img = img_path
        self.ml = ml
        self.retrieved = False
        self.data = [self.name, self.loc, self.char, self.tags, self.img]
        self.trigger=tk.BooleanVar(value=False,master=self.ml)
        self.frm = tk.Frame(self.ml, width=70, height=110, padx=10, pady=10,
                            highlightbackground="green", highlightthickness=5)

    def showState(self,mother_frm):
        #UI 만들기
        self.frm.destroy()
        self.frm = tk.Frame(mother_frm, width=70, height=110, padx=10, pady=10,
                            highlightbackground="green", highlightthickness=5)
        tk.Label(self.frm, text=f"{self.name}").pack()
        tk.Label(self.frm, text=f"{['찾으러 오세요','되찾음'][int(self.retrieved)]}").pack(anchor=tk.E)
        tk.Label(self.frm, text=f"위치: {self.loc}").pack()
        tk.Label(self.frm, text=f"{self.char}\n{' '.join(map(lambda x: '#'+x, self.tags))}").pack()
        if self.img: #이미지 출력
            self.photo = load_image(self.img, self.frm)
            if self.photo:
                tk.Label(self.frm, image=self.photo).pack(anchor="w")
            else:
                tk.Label(self.frm, text="(이미지 없음)").pack()
        else:
            tk.Label(self.frm, text="(이미지 없음)").pack()
        
        #찾기 버튼
        def retrieval():
            self.retrieved=True
            self.trigger.set(True)
            retrieve_bt.pack_forget()

        if not self.retrieved:
            retrieve_bt=tk.Button(self.frm, text="찾음", command=lambda: retrieval())
            retrieve_bt.pack()
