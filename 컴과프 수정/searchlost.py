from str_dist import str_dist
from abrev_check import is_abrev_both

def search(data, search_str): #data는 리스트형, 내부에 Lost클래스
    searched_li=[]
    for inst in data:
        for data_piece in inst.data:
            if isinstance(data_piece,str):
                if str_dist(inp=search_str,ans=data_piece)<=2 or is_abrev_both(data_piece,search_str):
                    searched_li.append(inst)
                    break
            if isinstance(data_piece,list):
                for val in data_piece:
                    if str_dist(inp=search_str,ans=data_piece)<=2 or is_abrev_both(data_piece,search_str):
                        searched_li.append(inst)
                        break
    return searched_li[:]
