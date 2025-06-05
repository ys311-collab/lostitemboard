def is_abrev(full,short):
    for ch in short:
        if ch not in full: return False
        full=full[full.find(ch)+1:]
    return True

def is_abrev_both(str1,str2):
    return is_abrev(str1,str2) or is_abrev(str2,str1)
