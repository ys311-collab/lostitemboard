import tkinter as tk
import data
from lost import Lost
from sortdata import reload_data
from fileio import save_data

def select_image():
    from tkinter import filedialog
    global img_path
    img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])

def lost_input(board_lost_ctxt, board_found_ctxt, ml):
    window = tk.Toplevel(ml)
    window.title("분실물 입력하기")
    name_et, time_et, loc_et = tk.Entry(window), tk.Entry(window), tk.Entry(window)
    tk.Label(window, text="이름:").pack(); name_et.pack()
    tk.Label(window, text="시간(월.일.시:분):").pack(); time_et.pack()
    tk.Label(window, text="위치:").pack(); loc_et.pack()
    tk.Button(window, text="사진 선택", command=select_image).pack()

    def assign():
        lost_item = Lost(name_et.get(), time_et.get(), loc_et.get(), img_path, board_lost_ctxt, board_found_ctxt, ml)
        data.lost_item_list.append(lost_item)
        save_data()
        reload_data(board_lost_ctxt, board_found_ctxt)
        window.destroy()

    tk.Button(window, text='등록', command=assign).pack()
