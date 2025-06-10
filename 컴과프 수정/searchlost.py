from str_dist import str_dist # 문자열 간 거리 계산 함수
from abrev_check import is_abrev_both # 문자열 간 준말 관계 확인

def search(datas, search_str): #datas는 리스트형, 내부에 Lost클래스
    print(search_str)
    searched_li=[] #검색 결과
    for inst in datas: 
        for data_piece in inst.data:
            if isinstance(data_piece,str): #str형 데이터에서 비교
                if data_piece and (str_dist(inp=search_str,ans=data_piece)<=2 or str_dist(ans=search_str,inp=data_piece)<=2 or is_abrev_both(data_piece,search_str)): #오차거리 2 허용
                    searched_li.append(inst)
                    print(data_piece)
                    break
            elif isinstance(data_piece,list): #list형 데이터에서
                for val in data_piece:
                    if isinstance(val,str): #str형 내부 객체를 비교
                        if val and (str_dist(inp=search_str,ans=val)<=2 or str_dist(ans=search_str,inp=val)<=2 or is_abrev_both(val,search_str)):
                            searched_li.append(inst)
                            print(val)
                            break
            if inst in searched_li: break #중복 검색 안 되도록 탈출
    return searched_li[:]
