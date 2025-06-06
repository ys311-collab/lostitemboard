#게시판 생성 / 게시판의 전체적 ui를 여기서 다룸
#module import
#region Method
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk

from fileio import load_data, save_data
from lost import Lost
from cag import LostCAG #Lost ComeAndGet, 잃어버린 것 같다고 생각되는는 물건 관리
from sortlost import sort_seq
from searchlost import search
from images import select_image, load_image
from login import load_user_data, save_user_data
#endregion Method

def start():

    with open('./login_state.txt','w') as f:
        f.write('')
    
    ## 새로고침
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
                inst.frm.grid(row=n//3, column=n%3)
            for n, inst in enumerate(sorted_i_f):
                inst.showState(board_found_ctxt)
                inst.frm.grid(row=n//3, column=n%3)
            for n, inst in enumerate(sorted_i_cag):
                inst.showState(board_cag_ctxt)
                inst.frm.grid(row=n//3, column=n%3)
            board_lost.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            board_found.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            board_cag.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            
        elif type=='s':
            global searched_list
            sorted_i_s=sort_seq(var_sort.get(),searched_list)[:]
            for w in board_search_ctxt.winfo_children(): w.destroy()
            if not sorted_i_s:
                tk.Label(board_search_ctxt, text="No result found.").pack()
            for n, inst in enumerate(sorted_i_s):
                inst.showState(board_search_ctxt)
                inst.frm.grid(row=n//4, column=n%4)
            board_search_ctxt.pack()
            board_search.pack()

        elif type=='user':
            user_lost_list=list(filter(lambda x: hasattr(x, 'username') and x.username==user,lost_item_list))
                                    #hasattr 추가한 이유: 기존 저장된 객체에 .username 속성이 없을 수 있음음
            user_found_list=list(filter(lambda x: hasattr(x, 'username') and x.username==user,found_item_list))

            for w in lostboard_mypage_ctxt.winfo_children(): w.destroy() 
            for w in foundboard_mypage_ctxt.winfo_children(): w.destroy()

            sorted_i_ul=sort_seq(var_sort.get(),user_lost_list)[:]
            if not sorted_i_ul:
                tk.Label(lostboard_mypage_ctxt, text="No Item Yet.").pack()
            for n, inst in enumerate(sorted_i_ul):
                inst.showState(lostboard_mypage_ctxt, mypage = True)
                inst.frm.grid(row=n//3, column=n%3)

            lostboard_mypage_ctxt.pack()

            sorted_i_uf=sort_seq(var_sort.get(),user_found_list)[:]
            if not sorted_i_uf:
                tk.Label(foundboard_mypage_ctxt, text="No Item Yet.").pack()
            for n, inst in enumerate(sorted_i_uf):
                inst.showState(foundboard_mypage_ctxt, mypage = True)
                inst.frm.grid(row=n//3, column=n%3)

            foundboard_mypage_ctxt.pack()
            board_mypage.pack()

    def reload_data_prime(*args): reload_data(typ)

    #변수 정의
    #region Method
    global typ
    global user
    typ='lf'
    user=''

    ml = tk.Tk()
    ml.title("Lost and Found")
    lost_item_list=[]
    found_item_list=[]
    searched_list=[]
    user_list=[]
    user_lost_list=[]
    user_found_list = []
    cag_item_list=[]
    load_data()
    #endregion Method

    #입력하기
    #region Method
    def lost_input(ml): 
        window = tk.Toplevel(ml)
        window.title("분실물 입력하기")
        frm=tk.Frame(window)

        def inputLostAndFound(frm):
            def select_image_int():
                global img_path
                img_path=select_image()

            def assign():
                lost_item = Lost(name_et.get(), time_et.get(), loc_et.get(), img_path, user, ml)
                lost_item_list.append(lost_item)
                reload_data(type=typ)
                window.destroy()

            name_et, time_et, loc_et = tk.Entry(frm),tk.Entry(frm), tk.Entry(frm)
            tk.Label(frm, text="Lost Name:",font=('Helvetica', 9, 'bold')).pack(); name_et.pack()
            tk.Label(frm, text="Lost Time:",font=('Helvetica', 9, 'bold')).pack(); time_et.pack()
            tk.Label(frm, text="Lost Location:",font=('Helvetica', 9, 'bold')).pack(); loc_et.pack()
            tk.Button(frm, text="Select Photo", command=select_image_int).pack()
            tk.Button(frm, text='submit', command=assign).pack()
    
        def inputComeAndFind(frm):
            def select_image_int():
                global img_path
                img_path=select_image()

            def assign():
                lost_item = LostCAG(name_et.get(), loc_et.get(), char_txt.get("1.0", "end-1c"), img_path, user,ml)
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
    
    top_frm = tk.Frame(ml)   #submit 버튼이 무조건 제일 위로 가게 함함
    top_frm.pack(side='top', fill='x')

    #submit 버튼
    #등록하기 : datainput 과 연결
    global submit_bt
    submit_bt = tk.Button(top_frm, text='submit', font=('Helvetica', 9, 'bold'),fg='#89B0AE', 
                          bg='#FAF9F9', command=lambda: lost_input(ml))  #<- 여기서 datainput의 함수 lost_input 사용
    submit_bt.pack()
    submit_bt.pack_forget()  # 처음에는 숨기기

    #endregion Method

    def to_home():
        global typ
        typ='lf'
        reload_data(typ)
    tk.Button(ml,text='HOME',command=to_home).pack()

    #검색하기 
    # region Method
    # searchlost 와 연결
    def search_int():
        global searched_list ###33
        global typ #######
        searched_list=search(lost_item_list+found_item_list+cag_item_list, search_et.get().strip())[:]
        typ='s'
        reload_data('s')

    search_frm = tk.Frame(ml)
    search_et = tk.Entry(search_frm)
    search_bt = tk.Button(search_frm,text='Search',command=search_int)
    
    search_et.pack(side='left')
    search_bt.pack(side='left')
    search_frm.pack()
    # endregion Method

    #정렬하기
    #region Method
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

    sort_bt.pack(side=tk.LEFT, padx=10)
    sort_frm.pack()
    #endregion Method

    #로그인 (메뉴바) 관리
    #region Method
    menubar = tk.Menu(ml)

    # 로그인 함수
    #menu reload 함수수
    def update_login_menu():
        # 기존 메뉴 항목 제거
        global user
        global submit_bt
        loginmenu.delete(0, 'end')
        if user:
            loginmenu.add_command(label="My Page", command=mypage)
            loginmenu.add_command(label="Logout", command=logout)
            submit_bt.pack()    #로그인하면 버튼 표시시
        else:
            loginmenu.add_command(label="Create ID", command= lambda : create_id(ml))
            loginmenu.add_command(label="Login", command= lambda: login(ml))
            submit_bt.pack_forget()   #로그아웃하면 버튼 숨김김

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
                with open ('./login_state.txt', 'w') as f:
                    f.write(user) 
                window.destroy()
                update_login_menu()
                reload_data(typ)
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

    def logout():
            global user
            user = ''
            with open ('./login_state.txt', 'w') as f:
                f.write('') 
            update_login_menu()
            messagebox.showinfo("Logout", "You are now logged out.")

    def mypage():
            global user
            messagebox.showinfo("My Page", f"Welcome to {user}'s page!")
            global typ
            typ= 'user'
            reload_data(typ)

    def exit(ml):
            ml.quit()
    
    # 로그인 메뉴 생성
    loginmenu = tk.Menu(menubar, tearoff=0)
    update_login_menu()
    menubar.add_cascade(label="Login", menu = loginmenu)

    # 테마 메뉴 생성
    # thememenu = tk.Menu(menubar, tearoff=0)
    # thememenu.add_command(label="Modern Basic", command = basic_theme)
    # thememenu.add_command(label="Cozy Cafe", command = cozy_theme)
    # thememenu.add_command(label="Aqua Blue", command = aqua_theme)
    # thememenu.add_command(label="Sunny Day", command = sunny_theme)
    # menubar.add_cascade(label="Theme", menu= thememenu)


    # 나가는 메뉴 생성
    exitmenu = tk.Menu(menubar, tearoff=0)
    exitmenu.add_command(label="Exit",command = lambda: exit(ml))
    menubar.add_cascade(label= "Exit", menu = exitmenu)

    ml.config(menu=menubar)
    #endregion Method

    #전체 게시판 관리
    #region Method
    board = tk.Frame(ml)
    board_lost = tk.Frame(board)
    board_lost.configure(bg='#FAF9F9')
    board_found = tk.Frame(board)
    board_found.configure(bg='#FAF9F9')
    board_cag = tk.Frame(board)
    board_search=tk.Frame(board)
    board_mypage=tk.Frame(board)
    board_mypage_ctxt=tk.Frame(board_mypage)
    lostboard_mypage=tk.Frame(board_mypage_ctxt)
    foundboard_mypage=tk.Frame(board_mypage_ctxt)
    
    tk.Label(board_lost, text='LOST', font=('Helvetica', 20, 'bold'),fg='#BEE3DB',bg = '#555B6E').pack()
    tk.Label(board_found, text='FOUND', font=('Helvetica', 20, 'bold'),fg='#FFD6BA',bg = '#555B6E').pack()
    tk.Label(board_cag, text='COME&GET', font=('Helvetica', 20, 'bold'),fg="#CAD7A4",bg = '#555B6E').pack()
    tk.Label(board_search, text='SEARCHED', font=('Helvetica', 20, 'bold'),fg='#BEE3DB',bg = '#555B6E').pack()
    tk.Label(board_mypage, text='MYPAGE', font=('Helvetica', 20, 'bold'),fg="#1BC8CB",bg = '#555B6E').pack()
    tk.Label(lostboard_mypage, text='LOST', font=('Helvetica', 20, 'bold'),fg='#FFD6BA',bg = '#555B6E').pack()
    tk.Label(foundboard_mypage, text='FOUND', font=('Helvetica', 20, 'bold'),fg='#FFD6BA',bg = '#555B6E').pack()

    board_lost_ctxt = tk.Frame(board_lost)
    board_found_ctxt = tk.Frame(board_found)
    board_cag_ctxt = tk.Frame(board_cag)
    board_search_ctxt=tk.Frame(board_search)
    lostboard_mypage_ctxt=tk.Frame(lostboard_mypage)
    foundboard_mypage_ctxt=tk.Frame(foundboard_mypage)

    board_lost.pack(side="left", padx=2, pady=2, fill="both", expand=True)
    board_found.pack(side="left", padx=2, pady=2, fill="both", expand=True)
    board_cag.pack(side="left", padx=2, pady=2, fill="both", expand=True)
    board_search.pack(side='left')
    board_mypage.pack(side='left')
    lostboard_mypage.pack(side=tk.LEFT, fill="both", expand=True)
    foundboard_mypage.pack(side=tk.RIGHT,fill="both", expand=True)
    
    board_mypage_ctxt.pack()
    board_cag_ctxt.pack(side='right', expand=True)
    board_search_ctxt.pack(fill="both", expand=True)
    lostboard_mypage_ctxt.pack(fill="both", expand=True)
    foundboard_mypage_ctxt.pack(fill="both", expand=True)

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

    board_lost_ctxt, lost_canvas, lost_scrollbar = create_scrollable_frame(board_lost)
    board_found_ctxt, found_canvas, found_scrollbar = create_scrollable_frame(board_found)
    board_cag_ctxt, cag_cv, cag_scbar = create_scrollable_frame(board_cag)
    lostboard_mypage_ctxt, lost_canvas, lost_scrollbar = create_scrollable_frame(lostboard_mypage)
    foundboard_mypage_ctxt, found_canvas, found_scrollbar = create_scrollable_frame(foundboard_mypage)

    board.pack()
    #endregion Method

    def on_close():
        save_data()
        ml.destroy()
    ml.protocol("WM_DELETE_WINDOW", on_close)

    reload_data(typ) #데이터 재정렬

    ml.mainloop()
