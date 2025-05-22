import tkinter as tk
import pickle

ml=tk.Tk()
class LostAndFound:
    def __init__(self,ml):

        self.lost_item_list=[]
        self.found_item_list=[]
        self.sorted_i_l = [] ## 메인 화면 표시의 기준
        self.sorted_i_f = []
        self.ml=ml

        self.add_bt=tk.Button(ml,text='등록하기', font=('Arial', 9, 'bold'), fg='#4CAF50', bg='white',command=lambda: self.lostInput())
        self.add_bt.pack()
        self.board_lost = tk.Frame(self.ml)
        self.board_found = tk.Frame(self.ml)
        self.lost_tit = tk.Label(self.board_lost, text='LOST', font=('Arial', 20, 'bold'))
        self.found_tit = tk.Label(self.board_found, text='FOUND', font=('Arial', 20, 'bold'))
        self.lost_tit.pack()
        self.found_tit.pack()

        self.board_lost_ctxt = tk.Frame(self.board_lost)
        self.board_found_ctxt = tk.Frame(self.board_found)

        self.sortLost()
        self.reload()

        self.board_lost.pack(side="left", padx=2, pady=2, fill="both", expand=True)
        self.board_found.pack(side="left", padx=2, pady=2, fill="both", expand=True)

    def reload(self):
        for wdg in self.board_lost_ctxt.winfo_children():
            wdg.destroy()

        for wdg in self.board_found_ctxt.winfo_children():
            wdg.destroy()

        self.sort_seq()

        for n,inst in enumerate(self.sorted_i_l):
            inst.showState()
            inst.frm.grid(row=n//4, column=n%4)

        for n,inst in enumerate(self.sorted_i_f):
            inst.showState()
            inst.frm.grid(row=n//4, column=n%4)

        self.board_lost_ctxt.pack()
        self.board_found_ctxt.pack()

    def sort_seq(self): #sorted_i_l에 순서를 저장하는 함수
        for lost in self.lost_item_list:
            if lost.state==1:
                self.lost_item_list.remove(lost)
                self.found_item_list.append(lost)
            
        self.typ = self.var_sort.get()
        if self.typ == 'u':
            self.sorted_i_l = self.lost_item_list[::-1]
            self.sorted_i_f = self.found_item_list[::-1]
        if self.typ == 't':
            self.sorted_i_l = sorted(self.lost_item_list, key=lambda x: x.time, reverse=True)
            self.sorted_i_f = sorted(self.found_item_list, key=lambda x: x.time, reverse=True)
        if self.typ == 'l':
            self.sorted_i_l = sorted(self.lost_item_list, key=lambda x: x.loc)
            self.sorted_i_f = sorted(self.found_item_list, key=lambda x: x.loc)
        print([(inst.name,inst.time,inst.loc) for inst in self.sorted_i_l])

    def sortLost(self): ### sorted_i_l 작성성
        self.sort_frm = tk.Frame(self.ml) 
        self.sort_lbl = tk.Label(self.sort_frm, text = "정렬 ", font=("나눔고딕 Light", 10, "bold"))
        self.sort_lbl.pack(side=tk.LEFT)

        self.var_sort = tk.StringVar(value='u')  #정렬 기준 선택
        self.sort_upload_rd = tk.Radiobutton(self.sort_frm, text='업로드 날짜',value='u',variable=self.var_sort)
        self.sort_time_rd = tk.Radiobutton(self.sort_frm, text='잃어버린 날짜',value='t',variable=self.var_sort)
        self.sort_loc_rd = tk.Radiobutton(self.sort_frm, text='잃어버린 위치',value='l',variable=self.var_sort)

        self.sort_bt = tk.Button(self.sort_frm, text="정렬", command= self.reload) ## 정렬 버튼

        self.sort_upload_rd.pack(side=tk.LEFT, padx=5) #pack
        self.sort_time_rd.pack(side=tk.LEFT, padx=5)
        self.sort_loc_rd.pack(side=tk.LEFT, padx=5)
        self.sort_bt.pack(side=tk.LEFT, padx=10)

        self.sort_frm.pack()

    def lostInput(self): #lost_item_list는 분실물 클래스를 값으로 하는 리스트, main에서 관리

        self.window=tk.Toplevel(self.ml)

        def assign(): #제출 버튼을 누를 시 등록하는 함수
            self.lost_item=Lost(self.name_et.get(),self.time_et.get(),self.loc_et.get(),self.image_et.get(),self.board_lost_ctxt,self.board_found_ctxt,self.ml) #객체 생성
            self.lost_item_list.append(self.lost_item)
            self.sort_seq()
            
            # lost_item.showState()

            # with open('./lost_sv.dat','wb') as f:
            #     pickle.dump(lost_item_list,f)

        self.window.title("분실물 입력하기")

        self.name_frm = tk.Frame(self.window)
        self.name_prmpt = tk.Label(self.name_frm, text = "분실물 이름:",font=("HY궁서B", 12, "bold"))
        self.name_et = tk.Entry(self.name_frm)

        self.time_frm = tk.Frame(self.window)
        self.time_prmpt = tk.Label(self.time_frm, text = "잃어버린 시간(월.일.시:분):")
        self.time_et = tk.Entry(self.time_frm)

        self.loc_frm = tk.Frame(self.window)
        self.loc_prmpt = tk.Label(self.loc_frm, text = "잃어버린 위치:")
        self.loc_et = tk.Entry(self.loc_frm)

        self.image_prmpt = tk.Label(self.window, text = "분실물 사진(선택):")  #사진 없을 경우 기본값(기본사진; X표 있는 흰 배경 같은거) 있어야힘
        self.image_et = tk.Entry(self.window)

        self.submit_bt = tk.Button(self.window, text='등록하기',command=lambda:(assign(),self.reload()))

        self.name_frm.pack(anchor=tk.W)
        self.name_prmpt.pack(side = tk.LEFT)
        self.name_et.pack(side = tk.LEFT)

        self.time_frm.pack(anchor=tk.W)
        self.time_prmpt.pack(side = tk.LEFT)
        self.time_et.pack(side = tk.LEFT)

        self.loc_frm.pack(anchor=tk.W)
        self.loc_prmpt.pack(side = tk.LEFT)
        self.loc_et.pack(side = tk.LEFT)

        self.image_prmpt.pack(anchor=tk.W)
        self.image_et.pack(anchor=tk.W)

        self.submit_bt.pack()
    
class Lost: #각 분실물을 객체로 하는 클래스스

    def __init__(self, name, time, loc, img, board_l, board_f, ml):
        self.name=name #변수 저장
        self.time=tuple(time.split('.'))
        self.loc=loc
        self.img=img
        self.board=[board_l,board_f]
        self.ml=ml
        self.state = 0 #'못 찾음'
        self.frm=tk.Frame(self.board[self.state],width=70, height=110, padx=10,pady=10, highlightbackground=["yellow","blue"][self.state], highlightthickness=5)

    def showState(self):
        self.frm.destroy()
        self.frm=tk.Frame(self.board[self.state],width=70, height=110, padx=10,pady=10, highlightbackground=["yellow","blue"][self.state], highlightthickness=5)

        self.statename = tk.Label(self.frm, text = f"분실물 이름: {self.name}")
        self.statetime = tk.Label(self.frm, text = f"예상 분실 시간: {self.time[0]}:{self.time[1]}" if self.state==0 else f"찾은 시간간: {self.find_time}")
        self.stateloc = tk.Label(self.frm, text = f"예상 분실 위치: {self.loc}" if self.state==0 else f"찾은 위치: {self.find_loc}")
        self.stateimg = tk.Label(self.frm, text = f"이미지: {self.img}")
        self.statestate = tk.Label(self.frm, text = f"현재 상태: {['못 찾음','찾음'][self.state]}")
        self.statesubmit = tk.Button(self.frm, text="분실물 찾음",command=self.foundInput)
        self.statename.pack()
        self.statetime.pack()
        self.stateloc.pack()
        self.stateimg.pack()
        self.statestate.pack()
        self.statesubmit.pack()

    def foundInput(self):
            
        self.window =tk.Toplevel(self.ml)
        self.window.title('분실물 찾아주기')

        def foundassign(): #제출 버튼을 누를 시 등록하는 함수
            self.state=1 #찾음
            self.find_time=self.time_et.get().split('.')
            self.find_loc=self.loc_et.get()
            self.showState()
            losts.reload()

        self.window.title("")

        self.time_frm = tk.Frame(self.window)
        self.time_prmpt = tk.Label(self.time_frm, text = "찾은 시간(월.일.시:분):")
        self.time_et = tk.Entry(self.time_frm)

        self.loc_frm = tk.Frame(self.window)
        self.loc_prmpt = tk.Label(self.loc_frm, text = "찾은 위치:")
        self.loc_et = tk.Entry(self.loc_frm)

        self.submit_bt = tk.Button(self.window, text='찾아주기',command=foundassign)

        self.time_frm.pack(anchor=tk.W)
        self.time_prmpt.pack(side = tk.LEFT)
        self.time_et.pack(side = tk.LEFT)

        self.loc_frm.pack(anchor=tk.W)
        self.loc_prmpt.pack(side = tk.LEFT)
        self.loc_et.pack(side = tk.LEFT)

        self.submit_bt.pack()

losts=LostAndFound(ml)
ml.mainloop()
