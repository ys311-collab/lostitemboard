#게시판 생성 / 게시판의 전체적 ui를 여기서 다룸
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

from fileio import load_data, save_data
import lost
from sortlost import sort_seq
# from searchlost import search_lost
from searchlost import search

from login import *
from theme import *
from data import *

user = ''
def start():
    global user
    typ='lf'
    ## 새로고침침
    def reload_data(type='lf',*args):
        for w in board.winfo_children():
            w.pack_forget()

        #리스트에서 반복할때 수정되지 않도록 분리리
        moved_to_found = [inst for inst in lost_item_list if inst.state == 1]
        moved_to_lost = [inst for inst in found_item_list if inst.state == 0]
    
        for inst in moved_to_found:
            lost_item_list.remove(inst)
            found_item_list.append(inst)
        for inst in moved_to_lost:
            found_item_list.remove(inst)
            lost_item_list.append(inst)


        if type=='lf':    
            for lost_inst in lost_item_list+found_item_list:
                lost_inst.trigger.trace_add("write",reload_data_prime)

            for w in board_lost_ctxt.winfo_children(): w.destroy()
            for w in board_found_ctxt.winfo_children(): w.destroy()
            
            sorted_i_l=sort_seq(var_sort.get(),lost_item_list)[:]
            sorted_i_f=sort_seq(var_sort.get(),found_item_list)[:]

            for n, inst in enumerate(sorted_i_l):
                inst.showState(board_lost_ctxt)
                inst.frm.grid(row=n//4, column=n%4)
            for n, inst in enumerate(sorted_i_f):
                inst.showState(board_found_ctxt)
                inst.frm.grid(row=n//3, column=n%3)
            board_lost.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            board_found.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            board.pack(fill='both', expand=True)


        elif type=='s':
            global searched_list #######
            sorted_i_s=sort_seq(var_sort.get(),searched_list)[:]
            for w in board_search_ctxt.winfo_children(): w.destroy()
            if not sorted_i_s:
                tk.Label(board_search_ctxt, text="No result found.").pack()
            for n, inst in enumerate(sorted_i_s):
                inst.showState(board_search_ctxt)
                inst.frm.grid(row=n//3, column=n%3)
            board_search_ctxt.pack()
            board_search.pack()
            board.pack(fill='both', expand=True)


        elif type=='user':
            board_lost.pack_forget()
            board_found.pack_forget()
            board_search.pack_forget()
            sorted_i_u=sort_seq(var_sort.get(),user_lost_list)[:]
            for w in board_search_ctxt.winfo_children(): w.destroy()
            for w in lostboard_mypage_ctxt.winfo_children(): w.destroy() 
            for w in foundboard_mypage_ctxt.winfo_children(): w.destroy()
            if not sorted_i_u:
                tk.Label(board_search_ctxt, text="No Item Yet.").pack()
            for n, inst in enumerate(sorted_i_u):
                inst.showState(lostboard_mypage_ctxt, mypage = True)
                inst.frm.grid(row=n//3, column=n%3)

            lostboard_mypage_ctxt.pack()
            lostboard_mypage.pack(side = "left")

            sorted_i_u1=sort_seq(var_sort.get(),user_found_list)[:]
            if not sorted_i_u1:
                tk.Label(board_search_ctxt, text="No Item Yet.").pack()
            for n, inst in enumerate(sorted_i_u1):
                inst.showState(foundboard_mypage_ctxt, mypage = True)
                inst.frm.grid(row=n//4, column=n%4)

            foundboard_mypage_ctxt.pack()
            foundboard_mypage.pack(side = "right")
            board.pack(fill='both', expand=True)
    def reload_data_prime(*args): reload_data(typ)

    ##입력력
    def lost_input(board_lost_ctxt, board_found_ctxt, ml):
        def select_image():
            from tkinter import filedialog
            global img_path ##########3
            img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        window = tk.Toplevel(ml)
        window.title("Submit")
        name_et, time_et, loc_et = tk.Entry(window), tk.Entry(window), tk.Entry(window)
        tk.Label(window, text="Lost Name:",font=('Helvetica', 9, 'bold')).pack(); name_et.pack()
        tk.Label(window, text="Lost Time(MonthDayHour060714):",font=('Helvetica', 9, 'bold')).pack(); time_et.pack()
        tk.Label(window, text="Lost Location:",font=('Helvetica', 9, 'bold')).pack(); loc_et.pack()
        tk.Button(window, text="Select Photo", command=select_image).pack()

        def assign():
            global user
            lost_item = lost.Lost(name_et.get(), time_et.get(), loc_et.get(), img_path, user, ml)
            lost_item_list.append(lost_item)
            save_data()
            global typ
            typ = 'lf'
            reload_data(typ)
            window.destroy()



        tk.Button(window, text='submit', command=assign).pack()
    ml = tk.Tk()
    ml.title("Lost and Found")
    ml.configure(bg = '#FAF9F9')
    ######################################################################

    top_frm = tk.Frame(ml)   #submit 버튼이 무조건 제일 위로 가게 함함
    top_frm.pack(side='top', fill='x')

    #submit 버튼, 초기에 숨기는 역할
    global submit_bt
    #등록하기 : datainput 과 연결
    submit_bt = tk.Button(top_frm, text='submit', font=('Helvetica', 9, 'bold'),
                              fg='#89B0AE', bg='#FAF9F9', command=lambda: lost_input(board_lost_ctxt, board_found_ctxt, ml))
                        #<- 여기서 datainput의 함수 lost_input 사용
    submit_bt.pack()
    submit_bt.pack_forget()  # 처음에는 숨기기


    ###
    lost_item_list=[]
    found_item_list=[]
    searched_list=[]
    user_lost_list=[]
    user_found_list = []
    load_data()


     #검색창 : searchlost 와 연결
    def search_int():
        global searched_list ###33
        global typ #######
        searched_list=search(lost_item_list+found_item_list, search_et.get().strip())[:]
        typ='s'
        reload_data('s')


    #검색창 : search
    search_frm = tk.Frame(ml)
    search_et = tk.Entry(search_frm)
    search_bt = tk.Button(search_frm,text='Search' ,command=search_int)
    # def search():
    #     searched_list=serach_lost(search_et.get())
    search_et.pack(side='left')
    search_bt.pack(side='left')
    search_frm.pack()

    #정렬하기
    #정렬 프레임
    sort_frm = tk.Frame(ml)
    sort_lbl = tk.Label(sort_frm, text="Reload", font=("Helvetica", 10, "bold"))
    sort_lbl.pack(side=tk.LEFT)

    #정렬 옵션 선택: sortdata와 연결
    var_sort = tk.StringVar(value='u',master = ml)
    tk.Radiobutton(sort_frm, text='Upload Date', font=('Helvetica', 10, 'bold'),fg='#555B6E', value='u', variable=var_sort).pack(side='left')
    tk.Radiobutton(sort_frm, text='Lost Date', font=('Helvetica',10, 'bold'), fg='#555B6E', value='t', variable=var_sort).pack(side='left')
    tk.Radiobutton(sort_frm, text='Lost Location', font=('Helvetica',10, 'bold'),fg='#555B6E', value='l', variable=var_sort).pack(side='left')
    sort_bt = tk.Button(sort_frm, text="Reload", command=lambda: reload_data_sort())
    def reload_data_sort():
        reload_data(typ)

    #sortdata의 함수 reload_data 사용
    sort_bt.pack(side=tk.LEFT, padx=10)
    sort_frm.pack()

    #전체 게시판 관리


    menubar = tk.Menu(ml)


    # 로그인 함수
    def login(ml):

        window = tk.Toplevel(ml)

        tk.Label(window, text="ID").pack()
        entry_id = tk.Entry(window)
        entry_id.pack()

        tk.Label(window, text="Password").pack()
        entry_pw = tk.Entry(window, show="*")
        entry_pw.pack()
        
        def check_login():
            username = entry_id.get()
            password = entry_pw.get()

            users = load_user_data()
            if username in users and users[username] == password:
                messagebox.showinfo("Login Sucessful!", f"Welcome {username}")
                global user
                user = username
                window.destroy()
                update_login_menu()
                #login함수 세부 처리 넣기

            else:
                messagebox.showerror("Failed to Login", "Id or password is wrong.")

            
        tk.Button(window, text="Login", command=check_login).pack(pady=5)

    # 회원가입 함수
    def create_id(ml):

        window = tk.Toplevel(ml)

        tk.Label(window, text="Id").pack()
        entry_id = tk.Entry(window)
        entry_id.pack()

        tk.Label(window, text="Password").pack()
        entry_pw = tk.Entry(window, show="*")
        entry_pw.pack()

        def register():
            username = entry_id.get()
            password = entry_pw.get()

            if not username or not password:
                messagebox.showwarning("입력 오류", "아이디와 비밀번호를 모두 입력하세요.")
                return

            users = load_user_data()
            if username in users:
                messagebox.showerror("회원가입 실패", "이미 존재하는 아이디입니다.")
            else:
                users[username] = password
                save_user_data(users)
                messagebox.showinfo("회원가입 성공", f"{username}님 회원가입 완료!")
                window.destroy()
                update_login_menu()
        tk.Button(window, text="Create ID", command= register).pack(pady=5)
    global user
    #menu reload 함수수
    def update_login_menu():
            # 기존 메뉴 항목 제거
            loginmenu.delete(0, 'end')
            if user:
                loginmenu.add_command(label="My Page", command=mypage)
                loginmenu.add_command(label="Logout", command=logout)
                submit_bt.pack()    #로그인하면 버튼 표시시
            else:
                loginmenu.add_command(label="Create ID", command= lambda : create_id(ml))
                loginmenu.add_command(label="Login", command= lambda: login(ml))
                submit_bt.pack_forget()   #로그아웃하면 버튼 숨김김

    def logout():
            global user
            user = ''
            update_login_menu()
            messagebox.showinfo("Logout", "You are now logged out.")

    def mypage():
            global user
            messagebox.showinfo("My Page", "Welcome to {}'s page!".format(user))
            global user_lost_list #######
            global user_found_list #######
            global typ #######
            user_lost_list=list(filter(lambda x: hasattr(x, 'username') and x.username.strip() == user.strip(),lost_item_list))
                                    #hasattr 추가한 이유: 기존 저장된 객체에 .username 속성이 없을 수 있음음
            user_found_list=list(filter(lambda x: hasattr(x, 'username') and x.username.strip() == user.strip(),found_item_list))
            typ= 'user'
            reload_data(typ)


    def exit(ml):
            ml.quit()


        
    # 로그인 메뉴 생성
    loginmenu = tk.Menu(menubar, tearoff=0)

    update_login_menu()

    menubar.add_cascade(label="Login", menu = loginmenu)

    # 테마 메뉴 생성
    thememenu = tk.Menu(menubar, tearoff=0)
    thememenu.add_command(label="Modern Basic", command = basic_theme)
    thememenu.add_command(label="Cozy Cafe", command = cozy_theme)
    thememenu.add_command(label="Aqua Blue", command = aqua_theme)
    thememenu.add_command(label="Sunny Day", command = sunny_theme)
    menubar.add_cascade(label="Theme", menu= thememenu)


    # 나가는 메뉴 생성
    exitmenu = tk.Menu(menubar, tearoff=0)
    exitmenu.add_command(label="Exit",command = lambda: exit(ml))
    menubar.add_cascade(label= "Exit", menu = exitmenu)

    ml.config(menu=menubar)


    # 스크롤 가능한 게시판을 위한 헬퍼 함수
    def create_scrollable_frame(parent):
        canvas = tk.Canvas(parent, borderwidth=0, background="#FAF9F9")
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, background="#FAF9F9")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame, canvas, scrollbar


    board = tk.Frame(ml)
    board_lost = tk.Frame(board)
    board_lost.configure(bg='#FAF9F9')
    board_found = tk.Frame(board)
    board_found.configure(bg='#FAF9F9')
    board_search=tk.Frame(board)
    lostboard_mypage=tk.Frame(board)
    foundboard_mypage=tk.Frame(board)

    
    tk.Label(board_lost, text='LOST', font=('Helvetica', 20, 'bold'),fg='#BEE3DB',bg = '#555B6E').pack()
    tk.Label(board_found, text='FOUND', font=('Helvetica', 20, 'bold'),fg='#FFD6BA',bg = '#555B6E').pack()
    tk.Label(board_search, text='SEARCHED', font=('Helvetica', 20, 'bold'),fg='#BEE3DB',bg = '#555B6E').pack()
    tk.Label(lostboard_mypage, text='LOST', font=('Helvetica', 20, 'bold'),fg='#FFD6BA',bg = '#555B6E').pack()
    tk.Label(foundboard_mypage, text='FOUND', font=('Helvetica', 20, 'bold'),fg='#BEE3DB',bg = '#555B6E').pack()


    board_search_ctxt=tk.Frame(board_search)
    lostboard_mypage_ctxt=tk.Frame(lostboard_mypage)
    foundboard_mypage_ctxt=tk.Frame(foundboard_mypage)
    board_lost.pack(side="left", padx=2, pady=2, fill="both", expand=True)
    board_found.pack(side="right", padx=2, pady=2, fill="both", expand=True)
    board_search.pack(side='left')
    lostboard_mypage.pack(side='left')
    foundboard_mypage.pack(side='right')
    board_search_ctxt.pack(fill="both", expand=True)
    lostboard_mypage_ctxt.pack(fill="both", expand=True)
    foundboard_mypage_ctxt.pack(fill="both", expand=True)


    #Scrollable 게시판 구현현

    board_lost_ctxt, lost_canvas, lost_scrollbar = create_scrollable_frame(board_lost)
    board_found_ctxt, found_canvas, found_scrollbar = create_scrollable_frame(board_found)
    lostboard_mypage_ctxt, lost_canvas, lost_scrollbar = create_scrollable_frame(lostboard_mypage)
    foundboard_mypage_ctxt, found_canvas, found_scrollbar = create_scrollable_frame(foundboard_mypage)

    board.pack()

    def on_close():
        save_data()
        ml.destroy()
    ml.protocol("WM_DELETE_WINDOW", on_close)

    reload_data(typ) #데이터 재정렬

    ml.mainloop()
