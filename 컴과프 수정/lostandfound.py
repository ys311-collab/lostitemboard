#게시판 생성 / 게시판의 전체적 ui를 여기서 다룸
import tkinter as tk

from fileio import load_data, save_data
import lost
from sortlost import sort_seq
# from searchlost import search_lost

def start():
    
    def reload_data(*args):
        for lost_inst in lost_item_list+found_item_list:
            lost_inst.trigger.trace_add("write",reload_data)

        for w in board_lost_ctxt.winfo_children(): w.destroy()
        for w in board_found_ctxt.winfo_children(): w.destroy()
        
        sorted_i_l, sorted_i_f = sort_seq(var_sort, lost_item_list, found_item_list)

        for n, inst in enumerate(sorted_i_l):
            inst.showState()
            inst.frm.grid(row=n//4, column=n%4)
        for n, inst in enumerate(sorted_i_f):
            inst.showState()
            inst.frm.grid(row=n//4, column=n%4)

    def lost_input(board_lost_ctxt, board_found_ctxt, ml):
        def select_image():
            from tkinter import filedialog
            global img_path
            img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        window = tk.Toplevel(ml)
        window.title("분실물 입력하기")
        name_et, time_et, loc_et = tk.Entry(window), tk.Entry(window), tk.Entry(window)
        tk.Label(window, text="이름:").pack(); name_et.pack()
        tk.Label(window, text="시간(월.일.시:분):").pack(); time_et.pack()
        tk.Label(window, text="위치:").pack(); loc_et.pack()
        tk.Button(window, text="사진 선택", command=select_image).pack()

        def assign():
            lost_item = lost.Lost(name_et.get(), time_et.get(), loc_et.get(), img_path, board_lost_ctxt, board_found_ctxt, ml)
            lost_item_list.append(lost_item)
            save_data()
            reload_data()
            window.destroy()

        tk.Button(window, text='등록', command=assign).pack()
    ml = tk.Tk()
    ml.title("Lost and Found")
    lost_item_list=[]
    found_item_list=[]
    load_data()

    #등록하기 : datainput 과 연결
    add_bt = tk.Button(ml, text='등록하기', font=('Arial', 9, 'bold'), fg='#4CAF50', bg='white',
                       command=lambda: lost_input(board_lost_ctxt, board_found_ctxt, ml)) 
                        #<- 여기서 datainput의 함수 lost_input 사용용
    add_bt.pack()

    #검색창 : sear
    search_frm = tk.Frame(ml)
    search_et = tk.Entry(search_frm)
    search_bt = tk.Button(search_frm,text='검색하기')#,command=search)
    # def search():
    #     searched_list=serach_lost(search_et.get())
    search_et.pack(side='left')
    search_bt.pack(side='left')
    search_frm.pack()

    #정렬하기
    #정렬 프레임
    sort_frm = tk.Frame(ml)
    sort_lbl = tk.Label(sort_frm, text="정렬", font=("나눔고딕 Light", 10, "bold"))
    sort_lbl.pack(side=tk.LEFT)

    #정렬 옵션 선택: sortdata와 연결
    var_sort = tk.StringVar(value='u')
    sort_upload_rd = tk.Radiobutton(sort_frm, text='업로드 날짜', value='u', variable=var_sort)
    sort_time_rd = tk.Radiobutton(sort_frm, text='잃어버린 날짜', value='t', variable=var_sort)
    sort_loc_rd = tk.Radiobutton(sort_frm, text='잃어버린 위치', value='l', variable=var_sort)
    sort_bt = tk.Button(sort_frm, text="정렬", command=lambda: reload_data())
    
    #sortdata의 함수 reload_data 사용용
    sort_upload_rd.pack(side=tk.LEFT, padx=5)
    sort_time_rd.pack(side=tk.LEFT, padx=5)
    sort_loc_rd.pack(side=tk.LEFT, padx=5)
    sort_bt.pack(side=tk.LEFT, padx=10)
    sort_frm.pack()

    #전체 게시판 관리
    board_lost = tk.Frame(ml)
    board_found = tk.Frame(ml)
    tk.Label(board_lost, text='LOST', font=('Arial', 20, 'bold')).pack()
    tk.Label(board_found, text='FOUND', font=('Arial', 20, 'bold')).pack()

    global board_lost_ctxt, board_found_ctxt
    board_lost_ctxt = tk.Frame(board_lost)
    board_found_ctxt = tk.Frame(board_found)
    board_lost.pack(side="left", padx=2, pady=2, fill="both", expand=True)
    board_found.pack(side="left", padx=2, pady=2, fill="both", expand=True)
    board_lost_ctxt.pack()
    board_found_ctxt.pack()

    def on_close():
        save_data()
        ml.destroy()
    ml.protocol("WM_DELETE_WINDOW", on_close)

    reload_data() #데이터 재정렬

    ml.mainloop()
