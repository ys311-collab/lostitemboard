#정렬기능 +
#다시 불러오기 기능_f

#정렬 함수
def sort_seq(var_sort,item_list):
    typ = var_sort.get()
    if typ == 'u':
        sorted_i = item_list[::-1]
    elif typ == 't':
        sorted_i = sorted(item_list, key=lambda x: x.time, reverse=True)
    elif typ == 'l':
        sorted_i = sorted(item_list, key=lambda x: x.loc)
    return sorted_i
