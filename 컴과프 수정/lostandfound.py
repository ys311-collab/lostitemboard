
#게시판 생성 / 게시판의 전체적 ui를 여기서 다룸
#module import
#region Method
try:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk
    from ttkthemes import ThemedTk

    # from fileio import load_data, 
    # data
    from lost import Lost           #분실물 하나하나를 객체로 클래스
    from cag import LostCAG         #Lost ComeAndGet, 잃어버린 것 같다고 생각되는 물건을 객체로 가지는 클래스
    from sortlost import sort_seq   #정렬 함수
    from searchlost import search   #검색 함수
    from images import select_image #이미지 입력 함수
    from login import load_user_data, save_user_data    #로그인 관련 함수
    import os
    import pygame
    pygame.mixer.init()
except ModuleNotFoundError:
    print('필요 모듈과 파일을 먼저 다운로드 받으세요 !!')
#endregion Method

def start():
    
    with open('./login_state.txt','w') as f: #login 한 사람 저장 -> 다른 파일에서 사용됨
        f.write('')

    def play_theme_music(theme_name):
        #저장되어있는 음악의 경로로
        theme_music = {
        'Basic': './bgm_basic.mp3',
        'Cozy': './bgm_cozy.mp3',
        'Aqua': './bgm_aqua.mp3',
        'Sunny': './bgm_sunny.mp3'
    }
        #pygame 모듈을 이용한 음악 재생, 무한 반복
        pygame.mixer.music.stop()
        path = theme_music.get(theme_name)
        if path and os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)  # 무한 반복


    #테마별 음악 재생 함수, Menubar의 Music Theme에 연결되어 있음
    def basic_theme():
        play_theme_music("Basic")

    def cozy_theme():
        play_theme_music("Cozy")

    def aqua_theme():
        play_theme_music("Aqua")

    def sunny_theme():
        play_theme_music("Sunny")


    ## 새로고침
    def reload_data(type='lf',*args): #게시판 새로고침 함수 : 배열 및 게시판 형식 새로고침침
        for w in board.winfo_children(): #기존의 모든 판 제거
            w.pack_forget()
        for inst in lost_item_list[:]+found_item_list[:]:  # 잃어버린 물건과 찾은 물건 재정렬
            if inst.state == 1 and inst not in found_item_list:
                lost_item_list.remove(inst)
                found_item_list.append(inst)
            if inst.state == 0 and inst not in lost_item_list:
                found_item_list.remove(inst)
                lost_item_list.append(inst)

        for lost_inst in lost_item_list+found_item_list+cag_item_list:
            if lost_inst.del_trc_id: lost_inst.delete_trigger.trace_remove("write",lost_inst.del_trc_id)
            lost_inst.del_trc_id=lost_inst.delete_trigger.trace_add("write",delete_reload)

        for lost_inst in lost_item_list+found_item_list+cag_item_list:
            if lost_inst.trc_id: lost_inst.trigger.trace_remove("write",lost_inst.trc_id)
            lost_inst.trc_id=lost_inst.trigger.trace_add("write",delete_reload)
            #객체 내에서 변화한 상태를 감지 후 새로고침
            #reload_data_prime은 trace_add 함수의 변수를 가변 매개변수 처리로 매개

        if type=='lf':    # 기본 홈 게시판 - 잃어버린 물건 lost_item_list, 찾은 물건 found_item_list, 
            #누군가 잃어버린 물건 cag_item_list. 세 리스트가 개별 보드에서 관리

            #보드 내부 초기화
            for w in board_lost_ctxt.winfo_children(): w.destroy()
            for w in board_found_ctxt.winfo_children(): w.destroy()
            for w in board_cag_ctxt.winfo_children(): w.destroy()
        
            #게시물을 정렬한 리스트 sortlost의 sort_seq 사용
            sorted_i_l=sort_seq(var_sort.get(),lost_item_list)[:]
            sorted_i_f=sort_seq(var_sort.get(),found_item_list)[:]
            sorted_i_cag=sort_seq('u',cag_item_list)
            
            #게시물 배치 - 정렬된 것을 바탕으로 함. 한 줄에 3개씩 배치
            for n, inst in enumerate(sorted_i_l):
                inst.showState(board_lost_ctxt)
                inst.frm.grid(row=n//3, column=n%3)
            for n, inst in enumerate(sorted_i_f):
                inst.showState(board_found_ctxt)
                inst.frm.grid(row=n//3, column=n%3)
            for n, inst in enumerate(sorted_i_cag):
                inst.showState(board_cag_ctxt)
                inst.frm.grid(row=n//3, column=n%3)

            #각각 게시판 업로드
            board_lost.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            board_found.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            board_cag.pack(side="left", padx=2, pady=2, fill="both", expand=True)
            
        elif type=='s': #검색 게시판: 검색 버튼을 눌렀을 때 작동
            global searched_list # 검색 리스트 불러오기
            sorted_i_s=sort_seq(var_sort.get(),searched_list)[:] #검색 리스트 정렬하기
            for w in board_search_ctxt.winfo_children(): w.destroy() # 검색 게시판 초기화
            if not sorted_i_s: # 검색 결과가 없다면 안내 메세지 출력하기기
                ttk.Label(board_search_ctxt, text="No result found.").pack()
            for n, inst in enumerate(sorted_i_s): #게시물 배치 - 한 줄에 4개씩
                inst.showState(board_search_ctxt)
                inst.frm.grid(row=n//4, column=n%4)
            board_search_ctxt.pack() # 검색 게시판 불러오기
            board_search.pack()

        elif type=='user': #마이페이지 출력하기 - 마이페이지 이동 버튼을 눌렀을 때
            # 자신이 잃어버린 물건과 찾아진 물건들이 검색됨
            user_lost_list=list(filter(lambda x: hasattr(x, 'username') and x.username==user,lost_item_list))
            #hasattr 추가한 이유: 기존 저장된 객체에 .username 속성이 없을 수 있음
            user_found_list=list(filter(lambda x: hasattr(x, 'username') and x.username==user,found_item_list))

            #게시판 초기화
            for w in lostboard_mypage_ctxt.winfo_children(): w.destroy() 
            for w in foundboard_mypage_ctxt.winfo_children(): w.destroy()

            #사용자가 잃어버린 물건 정렬, 아이템이 있으면 출력
            sorted_i_ul=sort_seq(var_sort.get(),user_lost_list)[:]
            if not sorted_i_ul:
                ttk.Label(lostboard_mypage_ctxt, text="No Item Yet.").pack()
            for n, inst in enumerate(sorted_i_ul):
                inst.showState(lostboard_mypage_ctxt, mypage = True)
                inst.frm.grid(row=n//3, column=n%3)

            lostboard_mypage_ctxt.pack()

            #사용자가 잃어버렸다가 찾은 물건 정렬, 아이템이 있으면 출력
            sorted_i_uf=sort_seq(var_sort.get(),user_found_list)[:]
            if not sorted_i_uf:
                ttk.Label(foundboard_mypage_ctxt, text="No Item Yet.").pack()
            for n, inst in enumerate(sorted_i_uf):
                inst.showState(foundboard_mypage_ctxt, mypage = True)
                inst.frm.grid(row=n//3, column=n%3)

            foundboard_mypage_ctxt.pack()
            board_mypage.pack()

        else: # 예외처리
            print('Error: To Home')
            global typ
            typ='lf'
            reload_data(typ)

    def reload_data_prime(*args): 
        reload_data(typ) # trigger.trace_add 매개
        for lost_inst in lost_item_list+found_item_list+cag_item_list:
            lost_inst.trigger.set(False)

    def delete_reload(*args):
        for lost_inst in lost_item_list+found_item_list+cag_item_list:
            print(1)
            if lost_inst.delete_trigger.get()==True:
                lost_inst.delete_trigger.set(False)
                if lost_inst in lost_item_list: lost_item_list.remove(lost_inst)
                elif lost_inst in found_item_list: found_item_list.remove(lost_inst)
                elif lost_inst in cag_item_list: cag_item_list.remove(lost_inst)
                print(2)
        reload_data(typ)
        for lost_inst in lost_item_list+found_item_list+cag_item_list:
            lost_inst.delete_trigger.set(False)

    #변수 정의
    #region Method
    global typ
    global user
    typ='lf' # 게시판 타입
    user='' #유저 이름 저장

    ml = ThemedTk(theme = 'arc')
    ml.title("Lost and Found")
    lost_item_list=[] #잃어버린 물건의 객체의 리스트
    found_item_list=[] #찾은 물건의 객체의 리스트
    searched_list=[] # 검색된 물건의 객체의 리스트
    user_lost_list=[] # 분실물 게시판의 잃어버린 물건 리스트
    user_found_list = [] # 분실물 게시판의 찾은 물건 리스트
    cag_item_list=[] # 누군가 잃어버린 것 같은 물건 리스트트
    #endregion Method

    #입력하기
    #region Method
    def lost_input(ml): #등록하기 버튼 (Submit) 을 누르면 실행되는 함수
        window = tk.Toplevel(ml) #등록하기 창: 새 창이 실행됨
        window.title("분실물 입력하기")
        frm=ttk.Frame(window) 
        #창에서 상단의 버튼으로 이루어진 선택창에서 잃어버린 물건 입력 모드와
        # 잃어버린 것 같은 물건 등록 모드를 선택 가능능 

        def inputLostAndFound(frm): #잃어버린 물건 입력 UI+작동 함수
            def select_image_int(): #이미지 선택을 매개하는 함수
                global img_path
                img_path=select_image()

            def assign(): # 사용자 입력 값을 바탕으로 분실물 객체를 생성
                lost_item = Lost(name_et.get(), time_et.get(), loc_et.get(), img_path, user, ml)
                lost_item_list.append(lost_item)
                reload_data(type=typ)
                window.destroy()

            #사용자 입력 창
            name_et, time_et, loc_et = tk.Entry(frm),tk.Entry(frm), tk.Entry(frm)
            ttk.Label(frm, text="Lost Name:").pack(); name_et.pack()
            ttk.Label(frm, text="Lost Time:").pack(); time_et.pack()
            ttk.Label(frm, text="Lost Loc:").pack(); loc_et.pack()
            ttk.Button(frm, text="Select Photo", command=select_image_int).pack()
            ttk.Button(frm, text='submit', command=assign).pack()
    
        def inputComeAndFind(frm): #잃어버린 것 같은 물건 등록 모드
            def select_image_int(): #이미지 선택을 매개하는 함수
                global img_path
                img_path=select_image()

            def assign(): # 사용자 입력 값을 바탕으로 분실물 객체를 생성
                lost_item = LostCAG(name_et.get(), loc_et.get(), char_txt.get("1.0", "end-1c"), img_path, user, ml)
                cag_item_list.append(lost_item)
                reload_data(type=typ)
                window.destroy()

            # 사용자 입력 창
            name_et,loc_et,char_txt=tk.Entry(frm),tk.Entry(frm),tk.Text(frm, width=20, height=9)
            ttk.Label(frm, text="Lost Name:").pack(); name_et.pack()
            ttk.Label(frm, text="Lost Loc:").pack(); loc_et.pack()
            ttk.Label(frm, text="Tags:\n").pack(); char_txt.pack()
            ttk.Button(frm, text="Select Photo", command=select_image_int).pack()
            ttk.Button(frm, text='Submit', command=assign).pack()

        # 버튼 선택을 바탕으로 사용자가 지정한 입력 창이 표시됨
        def load(typ,frm):
            for w in frm.winfo_children(): #새로고침
                w.destroy()
            if typ=='laf': inputLostAndFound(frm)
            elif typ=='cag': inputComeAndFind(frm)
            frm.pack()

        button_bar=ttk.Frame(window) # 버튼 두 개를 자연스럽게 이어지도록 프레임에 정렬
        ttk.Button(button_bar,text='Take this!!',command=lambda: load('laf',frm)).pack(side=tk.LEFT)
        ttk.Button(button_bar,text='Find this!!',command=lambda: load('cag',frm)).pack(side=tk.LEFT)
        button_bar.pack()
    
    ##입력하기 버튼, 로그인이 되어 있을 때에만 작동함
    top_frm = ttk.Frame(ml)   #submit 버튼이 무조건 제일 위로 가게 함함
    top_frm.pack(side='top', fill='x')

    #submit 버튼: 로그인 된 상태에서만 표시
    global submit_bt
    submit_bt = ttk.Button(top_frm, text='submit', command=lambda: lost_input(ml))  #<- 여기서 datainput의 함수 lost_input 사용
    submit_bt.pack()
    submit_bt.pack_forget()  # 처음에는 숨기기

    #endregion Method

    #유틸창
    # region Method
    util_frm=tk.Frame(ml)
    #홈매뉴
    def to_home():
        global typ
        typ='lf'
        reload_data(typ)
    ttk.Button(util_frm,text='HOME',command=to_home).pack(side='left',anchor='center')

    #검색하기 
    # searchlost 와 연결
    def search_int(): # 매개 함수: typ와 검색 리스트의 변화
        global searched_list 
        global typ 
        searched_list=search(lost_item_list+found_item_list+cag_item_list, search_et.get().strip())[:] # searchlost.py와 연결
        typ='s'
        reload_data('s') # 새로고침

    search_et = ttk.Entry(util_frm) #검색창
    search_bt = ttk.Button(util_frm,text='Search',command=search_int, style = "FIRST.TButton") # 검색 버튼
    
    search_et.pack(side='left')
    search_bt.pack(side='left')

    util_frm.pack()
    # endregion Method

    #정렬하기
    #region Method
    #정렬 프레임
    sort_frm = ttk.Frame(ml)
    sort_lbl = ttk.Label(sort_frm, text="Reload")
    sort_lbl.pack(side = tk.LEFT)

    #정렬 옵션 선택: sortdata와 연결
    var_sort = tk.StringVar(value='u',master = ml)
    ttk.Radiobutton(sort_frm, text='Upload Date', value='u', variable=var_sort).pack(side='left')
    ttk.Radiobutton(sort_frm, text='Lost Date',value='t', variable=var_sort).pack(side='left')
    ttk.Radiobutton(sort_frm, text='Lost Location',value='l', variable=var_sort).pack(side='left')
    sort_bt = ttk.Button(sort_frm, text="Reload", command=lambda: reload_data(typ))

    sort_bt.pack(side= 'left', padx=10)
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
            loginmenu.add_command(label="Logout", command=logout) #로그인하면 my page, logout 보임임
            submit_bt.pack()    #로그인하면 버튼 표시
        else:
            loginmenu.add_command(label="Create ID", command= lambda : create_id(ml))
            loginmenu.add_command(label="Login", command= lambda: login(ml)) #로그아웃하면 create ID, Login 보임
            submit_bt.pack_forget()   #로그아웃하면 버튼 숨김

    def login(ml):

        #아이디, 비밀번호 입력하는 창
        window = tk.Toplevel(ml)

        ttk.Label(window, text="ID").pack()
        entry_id = ttk.Entry(window)
        entry_id.pack()

        ttk.Label(window, text="Password").pack()
        entry_pw = ttk.Entry(window, show="*")
        entry_pw.pack()    
        
        def check_login():
            username = entry_id.get()
            password = entry_pw.get()

            users = load_user_data()
            if username in users and users[username] == password:
                messagebox.showinfo("Login Sucessful!", f"Welcome {username}")
                global user
                user = username

                #현재 로그인되어있는 유저 저장
                with open ('./login_state.txt', 'w') as f:
                    f.write(user) 
                window.destroy()
                update_login_menu()
                reload_data(typ)


            else:
                messagebox.showerror("Failed to Login", "Id or password is wrong.")

            
        ttk.Button(window, text="Login", command=check_login).pack()

    # 회원가입 함수
    def create_id(ml):

        window = tk.Toplevel(ml)

        ttk.Label(window, text="Id").pack()
        entry_id = ttk.Entry(window)
        entry_id.pack()

        ttk.Label(window, text="Password").pack()
        entry_pw = ttk.Entry(window, show="*")
        entry_pw.pack()

        def register():
            username = entry_id.get()
            password = entry_pw.get()

            #예외 처리리
            if not username or not password:
                messagebox.showwarning("입력 오류", "아이디와 비밀번호를 모두 입력하세요.")
                return

            users = load_user_data()
            if username in users:
                messagebox.showerror("회원가입 실패", "이미 존재하는 아이디입니다.")
            else:
                users[username] = password
                save_user_data(users) #유저 정보 저장
                messagebox.showinfo("회원가입 성공", f"{username}님 회원가입 완료!")
                window.destroy()
                update_login_menu()
        ttk.Button(window, text="Create ID", command= register).pack()

    def logout(): #로그아웃했을 때 게시판을 reload, 로그아웃 상태로 변경경
            global user
            global typ
            user = ''
            with open ('./login_state.txt', 'w') as f:
                f.write('')   #로그아웃 상태 저장장
            update_login_menu()
            reload_data(typ)
            messagebox.showinfo("Logout", "You are now logged out.")


    def mypage(): #mypage로 들어갔을때로 상태 변경경
            global user
            messagebox.showinfo("My Page", f"Welcome to {user}'s page!")
            global typ
            typ= 'user'
            reload_data(typ)

    def exit(ml):  #나가기 함수수
            ml.quit()
    
    # 로그인 메뉴 생성
    loginmenu = tk.Menu(menubar, tearoff=0)
    update_login_menu()
    menubar.add_cascade(label="Login", menu = loginmenu)

    # 배경음악 메뉴 생성
    thememenu = tk.Menu(menubar, tearoff=0)
    thememenu.add_command(label="Modern Basic", command = basic_theme) #누르면 테마별 배경음악이 나옴
    thememenu.add_command(label="Cozy Cafe", command = cozy_theme)
    thememenu.add_command(label="Aqua Blue", command = aqua_theme)
    thememenu.add_command(label="Sunny Day", command = sunny_theme)
    menubar.add_cascade(label="Music Theme", menu= thememenu)


    # 나가는 메뉴 생성
    exitmenu = tk.Menu(menubar, tearoff=0)
    exitmenu.add_command(label="Exit",command = lambda: exit(ml))
    menubar.add_cascade(label= "Exit", menu = exitmenu)

    ml.config(menu=menubar)
    #endregion Method

    #전체 게시판 관리
    #region Method
    board = ttk.Frame(ml)
    board_lost = ttk.Frame(board)
    #board 배경색 지정
    board_found = ttk.Frame(board)

    #보드, 보드_ctxt 생성성
    board_cag = ttk.Frame(board)
    board_search=ttk.Frame(board)
    board_mypage=ttk.Frame(board)
    board_mypage_ctxt=ttk.Frame(board_mypage)
    lostboard_mypage=ttk.Frame(board_mypage_ctxt)
    foundboard_mypage=ttk.Frame(board_mypage_ctxt)
    
    #섹션별 보드 만들기기
    ttk.Label(board_lost, text='LOST').pack()
    ttk.Label(board_found, text='FOUND').pack()
    ttk.Label(board_cag, text='COME&GET').pack()
    ttk.Label(board_search, text='SEARCHED').pack()
    ttk.Label(board_mypage, text='MYPAGE').pack()
    ttk.Label(lostboard_mypage, text='LOST').pack()
    ttk.Label(foundboard_mypage, text='FOUND').pack()

    #보드, 보드_ctxt 생성성
    board_lost_ctxt = ttk.Frame(board_lost)
    board_found_ctxt = ttk.Frame(board_found)
    board_cag_ctxt = ttk.Frame(board_cag)
    board_search_ctxt=ttk.Frame(board_search)
    lostboard_mypage_ctxt=ttk.Frame(lostboard_mypage)
    foundboard_mypage_ctxt=ttk.Frame(foundboard_mypage)

    #보드별 패킹
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

    #스크롤 가능한 보드 만들기 함수
    def create_scrollable_frame(parent):
        canvas = tk.Canvas(parent, borderwidth=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style = "FIRST.TFrame")

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

    #스크롤 가능한 보드 만들기
    board_lost_ctxt, lost_canvas, lost_scrollbar = create_scrollable_frame(board_lost)
    board_found_ctxt, found_canvas, found_scrollbar = create_scrollable_frame(board_found)
    board_cag_ctxt, cag_cv, cag_scbar = create_scrollable_frame(board_cag)
    lostboard_mypage_ctxt, lost_canvas, lost_scrollbar = create_scrollable_frame(lostboard_mypage)
    foundboard_mypage_ctxt, found_canvas, found_scrollbar = create_scrollable_frame(foundboard_mypage)

    board.pack()
    #endregion Method

    #끝내기 함수
    def on_close():
        ml.destroy()
    ml.protocol("WM_DELETE_WINDOW", on_close)

    reload_data(typ) #데이터 재정렬

    ml.mainloop()
