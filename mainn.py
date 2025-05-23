import tkinter as tk
import pickle

ml=tk.Tk()
class LostAndFound:
    def __init__(self,ml):

        self.lost_item_list=[]
        self.sorted_i_l = [] ## 메인 화면 표시의 기준
        self.ml=ml
        self.board = tk.Frame(self.ml)
        self.add_bt=tk.Button(ml,text='등록하기', font=('Arial', 9, 'bold'), fg='#4CAF50', bg='white',command=lambda: self.lostInput())
        self.add_bt.pack()

        self.sortLost()
        self.reload()
        self.board.pack()

    def reload(self):
        for wdg in self.board.winfo_children():
            wdg.destroy()

        for n,inst in enumerate(self.sorted_i_l):
            inst.showState()
            inst.frm.grid(row=n//4, column=(n+1)%4)
        self.board.pack()

        #     # 상태 변경 버튼
        #     self.status_button = tk.Button(self.frm, text="분실물 찾음", command=self.mark_found)
        #     self.status_button.pack()
        #     self.frm.pack()

    def sortLost(self): ############################################################ sorted_i_l 작성성
        self.sort_frm = tk.Frame(self.ml)
        self.sort_lbl = tk.Label(self.sort_frm, text = "정렬 ", font=("나눔고딕 Light", 10, "bold"))
        self.sort_lbl.pack(side=tk.LEFT)

        self.var_sort = tk.StringVar(value='u')  #정렬 기준 선택
        self.sort_upload_rd = tk.Radiobutton(self.sort_frm, text='업로드 날짜',value='u',variable=self.var_sort)
        self.sort_time_rd = tk.Radiobutton(self.sort_frm, text='잃어버린 날짜',value='t',variable=self.var_sort)
        self.sort_loc_rd = tk.Radiobutton(self.sort_frm, text='잃어버린 위치',value='l',variable=self.var_sort)

        def sort_seq(): #sorted_i_l에 순서를 저장하는 함수
            self.typ = self.var_sort.get()
            if self.typ == 'u':
                self.sorted_i_l = self.lost_item_list[::-1]
            if self.typ == 't':
                self.sorted_i_l = sorted(self.lost_item_list, key=lambda x: x.time, reverse=True)
            if self.typ == 'l':
                self.sorted_i_l = sorted(self.lost_item_list, key=lambda x: x.loc)
            print([(inst.name,inst.time,inst.loc) for inst in self.sorted_i_l])
            self.reload()

        self.sort_bt = tk.Button(self.sort_frm, text="정렬", command= sort_seq) ## 정렬 버튼

        self.sort_upload_rd.pack(side=tk.LEFT, padx=5) #pack
        self.sort_time_rd.pack(side=tk.LEFT, padx=5)
        self.sort_loc_rd.pack(side=tk.LEFT, padx=5)
        self.sort_bt.pack(side=tk.LEFT, padx=10)

        self.sort_frm.pack()

    def lostInput(self): #lost_item_list는 분실물 클래스를 값으로 하는 리스트, main에서 관리

        self.window=tk.Toplevel(self.ml)

        def assign(): #제출 버튼을 누를 시 등록하는 함수
            self.lost_item=Lost(self.name_et.get(),self.time_et.get(),self.loc_et.get(),self.image_et.get(),self.board) #객체 생성
            self.lost_item_list.append(self.lost_item)
            self.reload()
            self.sort_frm.pack_forget()
            self.sortLost()

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

        self.submit_bt = tk.Button(self.window, text='등록하기',command=assign)

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

    def foundInput(fl, window, lost_item_list,self):

        window =tk.Toplevel(fl)

        def foundassign(self): #제출 버튼을 누를 시 등록하는 함수

            window.title("분실물 정보")
            self.state = '찾음'

        name_frm = tk.Frame(window)
        name_prmpt = tk.Label(name_frm, text = "분실물 이름:")
        name_et = tk.Entry(name_frm)

        time_frm = tk.Frame(window)
        time_prmpt = tk.Label(time_frm, text = "찾은 시간(월.일.시:분):")
        time_et = tk.Entry(time_frm)

        loc_frm = tk.Frame(window)
        loc_prmpt = tk.Label(loc_frm, text = "찾은 위치:")
        loc_et = tk.Entry(loc_frm)

        call_frm = tk.Frame(window)
        call_prmpt = tk.Label(window, text = "분실물 사진(선택):")
        call_et = tk.Entry(window)

        submit_bt = tk.Button(window, text='찾아주기',command=foundassign)

        name_frm.pack(anchor=tk.W)
        name_prmpt.pack(side = tk.LEFT)
        name_et.pack(side = tk.LEFT)

        time_frm.pack(anchor=tk.W)
        time_prmpt.pack(side = tk.LEFT)
        time_et.pack(side = tk.LEFT)

        loc_frm.pack(anchor=tk.W)
        loc_prmpt.pack(side = tk.LEFT)
        loc_et.pack(side = tk.LEFT)

        call_frm.pack(anchor=tk.W)
        call_prmpt.pack(side = tk.LEFT)
        call_et.pack(side = tk.LEFT)

        submit_bt.pack()

class Lost(LostAndFound): #각 분실물을 객체로 하는 상속 클래스

    def __init__(self, name, time, loc, img, board):
        self.name=name #변수 저장
        self.time=tuple(time.split('.'))
        self.loc=loc
        self.img=img
        self.board=board
        self.frm=tk.Frame(self.board,padx=10,pady=10)
        self.state = '못 찾음'

    def showState(self):
        statename = tk.Label(self.frm, text = f"분실물 이름: {self.name}")
        statetime = tk.Label(self.frm, text = f"시간: {self.time[0]}:{self.time[1]}")
        stateloc = tk.Label(self.frm, text = f"위치: {self.loc}")
        stateimg = tk.Label(self.frm, text = f"이미지: {self.img}")
        statestate = tk.Label(self.frm, text = f"현재 상태: {self.state}")
        statesubmit = tk.Button(self.frm, text="분실물 찾음", command = )
        statename.pack()
        statetime.pack()
        stateloc.pack()
        stateimg.pack()
        statestate.pack()
        statesubmit.pack()

losts=LostAndFound(ml)
ml.mainloop()
