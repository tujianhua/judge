# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 15:16:46 2017

@author: Helen
"""
import re
#import amount_feature
#from amount_feature import clean

def import_law_list(txti="lawlist.txt"):
    fo = open(txti, "r+")
    list_law = []
    law = fo.readline()
    while law:
        law = law.strip()
        lawname = law.split("\t")[1]
        list_law.append(lawname.decode('utf-8'))
        law = fo.readline()
    fo.close()
    return list_law

def get_law_list():
    
    txti = "law.txt"
    txto = "lawlist.txt"
    
    fo = open(txti,"r+")
    fw = open(txto,"w+")
    law = fo.readline()
    while law:
        law = law.strip()
        list_law = law.split("\t")
        
        lawid = list_law[0]
        lawtext = list_law[1]
        lawname = lawtext.split('】')[0].split('【')[1]
        fw.write(lawid + "\t" + lawname + "\n")
        law = fo.readline()
    
    fo.close()
    fw.close()
    
def get_accusation_feature(casetext, caseid, list_law = []):
#    cleantext = clean(casetext, caseid)
    first_accusation = ""
#    list_accusations = re.findall(u'([因以犯涉嫌][^《》，。,]+[于被对罪,，])', casetext)  #提取罪名
    #list_accusation = re.findall('(犯|涉嫌|因|因涉嫌|因涉嫌犯|涉嫌犯)[^因涉嫌《》;；，。,]{2,30}?罪', casetext)  #提取罪名
    list_accusation = re.findall('[因犯涉嫌][^因涉嫌犯《》;；，。,]{2,30}?罪', casetext)  # 提取罪名
#   list_accusation2 = sorted(set(list_accusations),key=list_accusations.index) #去重
    
    if len(list_accusation) > 0:
   #     first_accusation = re.sub(u'[因以犯涉嫌罪于被对,]', '', list_accusations[0])
        
   #     for lawi in list_law:
  #          if re.search(first_accusation, lawi):
  #              return list_law.index(lawi) + 1
        return list_accusation[0]

    return None

def test_run():
    case = "犯盗窃罪"
    caseid = "17"
    get_accusation_feature(case, caseid)

if __name__ == "__main__":
    test_run()