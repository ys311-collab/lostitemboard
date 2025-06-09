from str_dist import str_dist # 문자열 간 거리 계산 함수
from abrev_check import is_abrev_both

def search(datas, search_str): #data는 리스트형, 내부에 Lost클래스
    searched_li=[]
    for inst in datas:
        for data_piece in inst.data:
            if isinstance(data_piece,str):
                if str_dist(inp=search_str,ans=data_piece)<=2 or is_abrev_both(data_piece,search_str):
                    searched_li.append(inst)
                    break
            if isinstance(data_piece,list):
                for val in data_piece:
                    if isinstance(val,str):
                        if str_dist(inp=search_str,ans=val)<=2 or is_abrev_both(val,search_str):
                            searched_li.append(inst)
                            break
            if inst in searched_li: break
    return searched_li[:]
