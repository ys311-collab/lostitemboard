def is_abrev(full,short): #short가 full의 준말인지 확인하는 함수
    for ch in short:
        if ch not in full: return False
        full=full[full.find(ch)+1:]
    return True

def is_abrev_both(str1,str2): # 한쪽이 다른 쪽의 준말인지 확인하는 함수수
    return is_abrev(str1,str2) or is_abrev(str2,str1)
