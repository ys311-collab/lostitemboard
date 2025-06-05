#게시판 생성 / 게시판의 전체적 ui를 여기서 다룸
import tkinter as tk

from fileio import load_data, save_data
from lost import Lost
from cag import LostCAG #Lost ComeAndGet, 잃어버린 것 같은 물건 관리
from sortlost import sort_seq
from searchlost import search
from images import select_image

def start():
    
    typ='lf'
    ## 새로고침침
    def reload_data(type='lf',*args):
        for w in board.winfo_children():
            w.pack_forget()
        for inst in lost_item_list[:]+found_item_list[:]:  # 복사본을 돌면서
            if inst.state == 1 and inst not in found_item_list:
                lost_item_list.remove(inst)
                found_item_list.append(inst)
            if inst.state == 0 and inst not in lost_item_list:
                found_item_list.remove(inst)
                lost_item_list.append(inst)
        if type=='lf':    
            for lost_inst in lost_item_list+found_item_list+cag_item_list:
                lost_inst.trigger.trace_add("write",reload_data_prime)

            for w in board_lost_ctxt.winfo_children(): w.destroy()
            for w in board_found_ctxt.winfo_children(): w.destroy()
            for w in board_cag_ctxt.winfo_children(): w.destroy()
            
            sorted_i_l=sort_seq(var_sort.get(),lost_item_list)[:]
            sorted_i_f=sort_seq(var_sort.get(),found_item_list)[:]
            sorted_i_cag=sort_seq('u',cag_item_list)

            for n, inst in enumerate(sorted_i_l):
                inst.showState(board_lost_ctxt)
                inst.frm.grid(row=n//4, column=n%4)
            for n, inst in enumerate(sorted_i_f):
                inst.showState(board_found_ctxt)
                inst.frm.grid(row=n//4, column=n%4)
            for n, inst in enumerate(sorted_i_cag):
                inst.showState(board_cag_ctxt)
                inst.frm.grid(row=n//4, column=n%4)
            board_lost.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            board_found.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            board_cag.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            
        elif type=='s':
            global searched_list
            sorted_i_s=sort_seq(var_sort.get(),searched_list)[:]
            for w in board_search_ctxt.winfo_children(): w.destroy()
            if not sorted_i_s:
                tk.Label(board_search_ctxt, text="검색 결과가 없습니다.").pack()
            for n, inst in enumerate(sorted_i_s):
                inst.showState(board_search_ctxt)
                inst.frm.grid(row=n//4, column=n%4)
            board_search_ctxt.pack()
            board_search.pack()

        elif type=='user':
            sorted_i_u=sort_seq(var_sort.get(),user_list)[:]
            for w in board_search_ctxt.winfo_children(): w.destroy()
            if not sorted_i_u:
                tk.Label(board_search_ctxt, text="아직 게시물이 없습니다.").pack()
            for n, inst in enumerate(sorted_i_u):
                inst.showState(board_mypage_ctxt)
                inst.frm.grid(row=n//4, column=n%4)
            board_mypage_ctxt.pack()
            board_mypage.pack()

    def reload_data_prime(*args): reload_data(typ)

    ##입력력
    def lost_input(ml): 
        window = tk.Toplevel(ml)
        window.title("분실물 입력하기")
        frm=tk.Frame(window)

        def inputLostAndFound(frm):
            def select_image_int():
                global img_path
                img_path=select_image()

            def assign():
                lost_item = Lost(name_et.get(), time_et.get(), loc_et.get(), img_path, ml)
                lost_item_list.append(lost_item)
                reload_data(type=typ)
                window.destroy()

            name_et, time_et, loc_et = tk.Entry(frm), tk.Entry(frm), tk.Entry(frm)
            tk.Label(frm, text="이름:").pack(); name_et.pack()
            tk.Label(frm, text="시간(월.일.시:분):").pack(); time_et.pack()
            tk.Label(frm, text="위치:").pack(); loc_et.pack()
            tk.Button(frm, text="사진 선택", command=select_image_int).pack()
            tk.Button(frm, text='등록', command=assign).pack()
    
        def inputComeAndFind(frm):
            def select_image_int():
                global img_path
                img_path=select_image()

            def assign():
                lost_item = LostCAG(name_et.get(), loc_et.get(), char_txt.get("1.0", "end-1c"), img_path, ml)
                cag_item_list.append(lost_item)
                reload_data(type=typ)
                window.destroy()

            name_et,loc_et,char_txt=tk.Entry(frm),tk.Entry(frm),tk.Text(frm, width=20, height=9)
            tk.Label(frm, text="이름:").pack(); name_et.pack()
            tk.Label(frm, text="위치:").pack(); loc_et.pack()
            tk.Label(frm, text="특징 (태그 포함):\n").pack(); char_txt.pack()
            tk.Button(frm, text="사진 선택", command=select_image_int).pack()
            tk.Button(frm, text='등록', command=assign).pack()

        def load(typ,frm):
            for w in frm.winfo_children():
                w.destroy()
            if typ=='laf': inputLostAndFound(frm)
            elif typ=='cag': inputComeAndFind(frm)
            frm.pack()

        button_bar=tk.Frame(window)
        tk.Button(button_bar,text='찾아주세요!!',width=10, height=4, bd=0,padx=0,pady=0, command=lambda: load('laf',frm)).pack(side=tk.LEFT)
        tk.Button(button_bar,text='찾아가세요!!',width=10, height=4, bd=0,padx=0,pady=0, command=lambda: load('cag',frm)).pack(side=tk.LEFT)
        button_bar.pack(padx=0,pady=0)

    ml = tk.Tk()
    ml.title("Lost and Found")
    lost_item_list=[]
    found_item_list=[]
    searched_list=[]
    user_list=[]
    cag_item_list=[]
    load_data()

    #등록하기 : datainput 과 연결
    add_bt = tk.Button(ml, text='등록하기', font=('Arial', 9, 'bold'), fg='#4CAF50', bg='white',
                       command=lambda: lost_input(ml)) 
                        #<- 여기서 datainput의 함수 lost_input 사용용
    add_bt.pack()

    #검색창 : searchlost 와 연결
    def search_int():
        global searched_list ###33
        global typ #######
        searched_list=search(lost_item_list+found_item_list+cag_item_list, search_et.get().strip())[:]
        typ='s'
        reload_data('s')

    search_frm = tk.Frame(ml)
    search_et = tk.Entry(search_frm)
    search_bt = tk.Button(search_frm,text='검색하기',command=search_int)
    
    search_et.pack(side='left')
    search_bt.pack(side='left')
    search_frm.pack()

    #정렬하기
    #정렬 프레임
    sort_frm = tk.Frame(ml)
    sort_lbl = tk.Label(sort_frm, text="정렬", font=("나눔고딕 Light", 10, "bold"))
    sort_lbl.pack(side=tk.LEFT)

    #정렬 옵션 선택: sortdata와 연결
    var_sort = tk.StringVar(value='u',master=ml)
    tk.Radiobutton(sort_frm,text='업로드 순',value='u',variable=var_sort).pack(side='left')
    tk.Radiobutton(sort_frm,text='잃어버린 날짜',value='t',variable=var_sort).pack(side='left')
    tk.Radiobutton(sort_frm,text='잃어버린 위치',value='l',variable=var_sort).pack(side='left')

    sort_bt = tk.Button(sort_frm, text="정렬", command=lambda: reload_data_sort())
    def reload_data_sort():
        reload_data(typ)

    sort_bt.pack(side=tk.LEFT, padx=10)
    sort_frm.pack()

    #전체 게시판 관리
    board=tk.Frame(ml)
    board_lost = tk.Frame(board)
    board_found = tk.Frame(board)
    board_cag = tk.Frame(board)
    board_search=tk.Frame(board)
    board_mypage=tk.Frame(board)
    tk.Label(board_lost, text='LOST', font=('Arial', 20, 'bold')).pack()
    tk.Label(board_found, text='FOUND', font=('Arial', 20, 'bold')).pack()
    tk.Label(board_cag, text='COME&GET', font=('Arial', 20, 'bold')).pack()
    tk.Label(board_search,text='SEARCHED', font=('Arial', 20, 'bold')).pack()
    tk.Label(board_mypage, text='MYPAGE', font=('Arial', 20, 'bold')).pack()

    board_lost_ctxt = tk.Frame(board_lost)
    board_found_ctxt = tk.Frame(board_found)
    board_cag_ctxt = tk.Frame(board_cag)
    board_search_ctxt=tk.Frame(board_search)
    board_mypage_ctxt=tk.Frame(board_mypage)
    board_lost.pack(side="left", padx=2, pady=2, fill="both", expand=True)
    board_found.pack(side="left", padx=2, pady=2, fill="both", expand=True)
    board_cag.pack(side="left", padx=2, pady=2, fill="both", expand=True)
    board_search.pack(side='left')
    board_mypage.pack(side='left')
    board_lost_ctxt.pack()
    board_found_ctxt.pack()
    board_cag_ctxt.pack()
    board_search_ctxt.pack()
    board_mypage_ctxt.pack()

    board.pack()

    def login():
        #login함수 세부 처리 넣기
        global user_list #######3
        global typ #######
        user=login_et.get()
        user_list=list(filter(lambda x: x.username==user,lost_item_list+found_item_list))
        typ=user
        reload_data(type='user')

    #로그인 버튼 (임시)
    login_et=tk.Entry(ml, text='user id')
    login_bt=tk.Button(ml,text='login',command=login)
    login_et.pack()
    login_bt.pack()

    def on_close():
        save_data()
        ml.destroy()
    ml.protocol("WM_DELETE_WINDOW", on_close)

    reload_data(typ) #데이터 재정렬

    ml.mainloop()
