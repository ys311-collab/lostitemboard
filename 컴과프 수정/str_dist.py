from jamo import h2j

def str_dist(inp,ans):
    def is_hangeul(char): # 한글인지 판단
        return (
            ('가' <= char <= '힣') or  
            ('ㄱ' <= char <= 'ㅎ') or  
            ('ㅏ' <= char <= 'ㅣ')     
        )
    def conv_str(string): # 한글->자모 / 영어->소문자
        res=''
        for ch in string:
            if is_hangeul(ch): res+=h2j(ch)
            elif ch.isalpha(): res+=ch.lower()
            elif ch.isdigit(): res+=ch
        return res

    def find_closest(inp,ans,inp_idx,ans_idx):
        min_dist_list=[max((len(ans)-ans_idx),(len(inp)-inp_idx)),len(inp),len(ans)]
        for idx in range(inp_idx,len(inp)): #inp의 idx>inp_idx 인덱스 값과 ans의 next_find>ans_idx 인덱시 값이 같은
            #것들 중에서 그 차이의 합이 최소가 되도록 함. 없다면 inp_idx, ans_idx 값을 가짐.
            if inp[idx] in ans[ans_idx:]:
                next_find=ans[ans_idx:].find(inp[idx])+ans_idx
            else:
                next_find=len(ans)
            dist=max(next_find-ans_idx, idx-inp_idx)
            if min_dist_list[0]>dist:
                min_dist_list=[dist,next_find,idx] #거리, answer의 리더 인덱스, input의 리더 인덱스. 둘의 리스트에서의 값은 같다.
        return min_dist_list

    inp,ans = conv_str(inp),conv_str(ans) #변환 완료된 문자열 string

    dist=0
    inp_rd, ans_rd = 0,0 # 읽고 있는 인덱스 위치
    try:
        while inp_rd<=len(inp)-1 and ans_rd<=len(ans)-1:
            if inp[inp_rd]==ans[ans_rd]: #같으면 다음 칸으로 이동해 읽기
                inp_rd+=1
                ans_rd+=1
            else: 
                #오타 발생 !! 두 값이 같은 최소 거리의 인덱스로 리더를 이동시킴
                distance_list=find_closest(inp,ans,inp_rd,ans_rd)
                dist+=distance_list[0]
                ans_rd,inp_rd= distance_list[1],distance_list[2]
    
    except Exception as e:
        pass
    return dist+max(len(ans)-ans_rd,len(inp)-inp_rd)
