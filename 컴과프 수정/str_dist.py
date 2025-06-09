from jamo import h2j

def str_dist(inp,ans):
    def is_hangeul(char): # 한글인지 판단하는 모듈
        return (
            ('가' <= char <= '힣') or  # 한글
            ('ㄱ' <= char <= 'ㅎ') or  # 자음
            ('ㅏ' <= char <= 'ㅣ')     # 모음
        )
    def conv_str(string): # 한글->자모 영어->소문자
        res=''
        for ch in string:
            if is_hangeul(ch): res+=h2j(ch)
            elif ch.isalpha(): res+=ch.lower()
            else: pass
        return res

    def find_closest(inp,ans,inp_idx,ans_idx):
        min_dist_list=[max((len(ans)-1-ans_idx),(len(inp)-1-inp_idx)),len(inp),len(ans)]
        for idx in range(inp_idx+1,len(inp)):
            if ans_idx<len(ans)-1 and inp[idx] in ans[ans_idx+1:]:
                next_find=ans[ans_idx+1:].find(inp[inp_idx])
            else:
                next_find=len(ans)
            dist=max(next_find-ans_idx, idx-inp_idx)
            if min_dist_list[0]>dist:
                min_dist_list=[dist,next_find,idx]
        return min_dist_list

    inp,ans = conv_str(inp),conv_str(ans) #변환 완료된 문자열 string

    dist=0
    inp_rd, ans_rd = 0,0 # 읽고 있는 인덱스 위치
    try:
        while inp_rd<=len(inp)-1 and ans_rd<=len(ans)-1:
            if inp[inp_rd]==ans[ans_rd]:
                inp_rd+=1
                ans_rd+=1
            else: 
                #오타 발생 !!
                distance_list=find_closest(inp,ans,inp_rd,ans_rd)
                dist+=distance_list[0]
                ans_rd,inp_rd= distance_list[1],distance_list[2]
    except Exception as e:
        print(e)
    return dist
