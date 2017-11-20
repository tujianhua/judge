# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:56:44 2017

@author: Helen
"""
import re

"""清洗数据:  1. 多个小数点; 2. 小数点结尾; 3.xxx.xx元 4. 90O0元 5. l00元 """
def clean(casetext, caseid):
    pattern = re.compile(u'(\d+\.)(\d+\.)+\d+[万余多]?元')
    str1 = re.sub(pattern, func_correction1, casetext) 
    pattern = re.compile(u'\.元')
    str2 = re.sub(pattern, u'元', str1)
    pattern = re.compile(u'[(币)(计)(额)][Xx]+[Xx.\d]*元')
    # pattern_xxx = re.compile('[Xx]+\.0')
    # matchobj = re.match(pattern_xxx,str2)
    # if(matchobj):
    #     print(matchobj.group())
    str3 = re.sub(pattern, func_correction3, str2)
    pattern = re.compile(u'\d+O[O\d]+元')
    str4 = re.sub(pattern, func_correction4, str3)
    pattern = re.compile(u'\d*l[\dl]+元')
    str5 = re.sub(pattern, func_correction5, str4)
    return str5

    """辅助函数 纠错1：多个小数点"""
def func_correction1(m):
    s = m.group()
    i = s.rfind('.') 
    s1 = s[0:i].replace('.','')
    s2 = s[i:] 
#    print ("clean() func_correction1() corrected data from %s to %s" %(s, s1+s2))
    str1 = (s1+s2)
    return str1

    """辅助函数 纠错3: xxx.xx元 -> 111.11元"""
def func_correction3(m):
    s = m.group()
    str1 = re.sub(u'[Xx]','1', s)
#    print ("clean() func_correction3() corrected data from %s to %s" %(s, str1))
    return str1

def func_correction4(m):
    s = m.group()
    str1 = re.sub(u'[Oo]','0', s)
#    print ("clean() func_correction4() corrected data from %s to %s" %(s, str1))
    return str1

def func_correction5(m):
    s = m.group()
    str1 = re.sub(u'[l]','1', s)
#    print ("clean() func_correction5() corrected data from %s to %s" %(s, str1))
    return str1

   
"""金额文本 -> 浮点数"""
def trans_amount_text(casetext, caseid):
    if(caseid == 528420):
        print(caseid)
    cleantext = clean(casetext, caseid)
    pattern = re.compile(u'(\d[\d\.,，]+[十百佰千万多余]*元)')
    str1 = re.sub(pattern, func_trans_amount, cleantext)
    return str1

    """辅助函数 金额数值转为浮点数"""
def func_trans_amount(nstr):
    str1 = re.sub(u'[,，]', '', nstr.group())    #去除逗号    
    m = re.search(u'[\d\.]+', str1)             #找到纯数值    
    n = float(m.group())
    if re.search(u'万',str1):
        n = n * 10000
    if re.search(u'千',str1):  
        n = n * 1000
    if re.search(u'百',str1):
        n = n * 100
    if re.search(u'十',str1):
        n = n * 10 
    str1 = str(n) + "元"
    #str1 = str1.decode('utf-8')
    return str1


"""把文本中金额提取出来，返回一个列表"""
def get_amount_list(casetext, caseid):   
    if(caseid=='528420'):
       print(caseid)
    cleantext = trans_amount_text(casetext, caseid)
    pattern = re.compile(u'[\d\.]+元')
    list_nstr = re.findall(pattern, cleantext)
    if list_nstr:
        list_nstr1 = [s.replace(u'元','') for s in list_nstr]
        list_amounts = []
        try:
            list_amounts = [float(_s) for _s in list_nstr1]
            return list_amounts
        except Exception:
            print(Exception)

    return []


"""取得犯罪金额特征值"""
def get_amount_feature(casetext, caseid):
    list_amounts = get_amount_list(casetext, caseid)
    if len(list_amounts) > 0:
        maxn =  max(list_amounts)
    else:
        maxn = 0
    return get_range(maxn)


"""判断数值范围"""
def get_range(n):
    if n > 0 and n <= 1000:
        return 1
    if n > 1000 and n <=2000:
        return 2
    if n > 2000 and n <=3000:
        return 3
    if n > 3000 and n <=4000:
        return 4
    if n > 4000 and n <=5000:
        return 5
    if n > 5000 and n <=10000:
        return 6
    if n > 10000 and n <=500000:
        return 7
    if n > 500000:
        return 8
    return 3


""" 主parser程序，数据预处理与特征提取"""
def parser(txti, txto,is_test=False):
    fo = open(txti,"r+",encoding='utf-8')
    fw = open(txto,"w+",encoding='utf-8')
    
    count_related = 0
    count_irrelated = 0
    count_nonumber = 0
    
    case = fo.readline()
    if(is_test):
        length = 2
    else:
        length = 4
    while case:
        list_case = case.strip().split("\t")

        #length
        if len(list_case) == length:
            casetext = list_case[1]
            caseid = list_case[0]
            amount_range = get_amount_feature(casetext, caseid)
            
            # if amount_range == 0:
            #     count_nonumber += 1
            # if int(list_case[2]) == amount_range:
            #     count_related += 1
            # else:
            #     count_irrelated += 1
            if (is_test==False):
                fw.write(list_case[0] + "\t" + list_case[2] + "\t" + list_case[3] + "\t" + str(amount_range) + "\n")
            else:
                fw.write(list_case[0]+ "\t" + str(amount_range) +"\n")
        case = fo.readline()
        
    # print ("相关数")
    # print (count_related)
    # print ("不相关数" )
    # print (count_irrelated)
    # print ("无数据案例数")
    # print (count_nonumber)
    
    fo.close()
    fw.close()

def test_run():
    txti = "test.txt"
    txto = "test_amount.txt"
    parser(txti,txto,is_test=True)

    parser('train.txt','t_amount.txt',is_test=False)

if __name__ == "__main__":
    test_run()
