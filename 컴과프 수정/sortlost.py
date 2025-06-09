#정렬기능 +
#다시 불러오기 기능_f

#정렬 함수
def sort_seq_l(typ,item_list):
    sorted_i=[]
    if typ == 'u': #업로드 날짜 순 (최근일 수록 앞)
        sorted_i = item_list[::-1]
    elif typ == 't': #잃어버렸다 생각되는 시간 순 (최근일 수록 앞)
        sorted_i = sorted(item_list, key=lambda x: x.time, reverse=True)
    elif typ == 'l': #위치의 ㄱㄴㄷ순
        sorted_i = sorted(item_list, key=lambda x: x.loc)
    return sorted_i

def sort_seq_f(typ,item_list):
    sorted_i=[]
    if typ == 'u': #업로드 날짜 순
        sorted_i = item_list[::-1]
    elif typ == 't': # 찾아준 날짜 순
        sorted_i = sorted(item_list, key=lambda x: x.find_time, reverse=True)
    elif typ == 'l': # 찾은 위치의 ㄱㄴㄷ순
        sorted_i = sorted(item_list, key=lambda x: x.find_loc)
    return sorted_i

def sort_seq_cag(typ,item_list):
    sorted_i=[]
    if typ == 'u' or typ=='t': #업로드 순
        sorted_i = item_list[::-1]
    elif typ == 'l': #장소 순순
        sorted_i = sorted(item_list, key=lambda x: x.loc)
    return sorted_i
