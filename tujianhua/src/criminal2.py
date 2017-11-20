# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:56:44 2017

@author: Helen
"""

from amount_feature import get_amount_feature
from accusation_feature import get_accusation_feature


""" 主parser程序，数据预处理与特征提取"""
def parser(txti, txto):
    fo = open(txti,"r+",encoding='utf-8')
    fw = open(txto,"w+",encoding='utf-8')
    fw_bad = open('accusation_bad.txt','w+',encoding='utf-8')
    count_related = 0
    count_irrelated = 0
    count_nonumber = 0
    count_accusationcorrect = 0
    count_accusationwrong = 0
    
    case = fo.readline()
    while case:
        case = case.strip()
        list_case = case.split("\t")
        casetext = list_case[1]
        caseid = list_case[0]
        
        """获得金额特征"""
 #       amount_range = get_amount_feature(casetext, caseid)
        amount_range = 0
        """获得罪名特征: 第一罪名"""
 #       list_law = import_law_list("lawlist.txt")
        accusationname = get_accusation_feature(casetext, caseid)
  #       accusationid_answer = re.sub(u'[^0-9]',",",list_case[3]).split(",")[0]
        
  
        """统计、默认修正和打印"""    
        if amount_range == 0:
            count_nonumber += 1         #无金额的案例数
            amount_range = 3    #修改为默认值3
        
        if accusationname:
            count_accusationcorrect += 1
        else:
            accusationname = '无名罪'
            fw_bad.write(case+'\n')
            count_accusationwrong += 1
  #      if int(list_case[2]) == amount_range:
  #          count_related += 1          #金额范围=罚金范围的案例数
   #     else:
    #        count_irrelated += 1        #金额范围<>罚金范围的案例数
     #   if accusationid == accusationid_answer:
      #      count_accusationcorrect += 1  #罪名正确的案例数
       # else:
        #    count_accusationwrong += 1  #罪名错误的案例数  
        
        """输出结果"""
        fw.write(caseid + "\t" + str(amount_range) + "\t"  + accusationname + "\n")
        
 #      fw.write(caseid + "\t" + list_case[2] + "\t" + str(amount_range) + "\t" + str(accusationid_answer) + "\t" + str(accusationid) + "\n")
        case = fo.readline()
        
    print ("相关数%d:"%(count_related))
    print ("不相关数%d"%(count_irrelated))
    print ("无数据案例数%d"%(count_nonumber))
    print ("罪名正确案例数%d"%(count_accusationcorrect))
    print ("罪名错误案例数%d"%(count_accusationwrong))
    
    fo.close()
    fw.close()
    fw_bad.close()

def test_run():
    txti = "train.txt"
    txto = "accusation_with_duplicated.txt"
    parser(txti,txto)

if __name__ == "__main__":
    test_run()
