
def tranxiaox(upnum):
    s = "零壹贰叁肆伍陆柒捌玖"
    for c in "0123456789": 
        upnum = upnum.replace(s[eval(c)], c)
    return upnum
