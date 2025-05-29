#정렬기능 +
#다시 불러오기 기능

from data import lost_item_list, found_item_list, sorted_i_l, sorted_i_f

#정렬 함수
def sort_seq(var_sort,lost_item_list,found_item_list):
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
    return sorted_i_l, sorted_i_f
