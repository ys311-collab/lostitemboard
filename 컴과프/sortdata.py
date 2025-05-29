#정렬기능 +
#다시 불러오기 기능

from data import lost_item_list, found_item_list, sorted_i_l, sorted_i_f
from tkinter import StringVar

#정렬 함수
def sort_seq(var_sort):
    for lost in lost_item_list[:]:
        if lost.state == 1:
            lost_item_list.remove(lost)
            found_item_list.append(lost)
    typ = var_sort.get()
    if typ == 'u':
        sorted_i_l[:] = lost_item_list[::-1]
        sorted_i_f[:] = found_item_list[::-1]
    elif typ == 't':
        sorted_i_l[:] = sorted(lost_item_list, key=lambda x: x.time, reverse=True)
        sorted_i_f[:] = sorted(found_item_list, key=lambda x: x.time, reverse=True)
    elif typ == 'l':
        sorted_i_l[:] = sorted(lost_item_list, key=lambda x: x.loc)
        sorted_i_f[:] = sorted(found_item_list, key=lambda x: x.loc)

#다시 불러오기 함수 #####중요 !!!!!!
def reload_data(board_lost_ctxt, board_found_ctxt, var_sort=None):

    if var_sort is None:
        var_sort = StringVar(value='u')

    for w in board_lost_ctxt.winfo_children(): w.destroy()
    for w in board_found_ctxt.winfo_children(): w.destroy()
    sort_seq(var_sort)

    for n, inst in enumerate(sorted_i_l):
        inst.showState()
        inst.frm.grid(row=n//4, column=n%4)
    for n, inst in enumerate(sorted_i_f):
        inst.showState()
        inst.frm.grid(row=n//4, column=n%4)
