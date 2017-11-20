# -*- coding:utf-8 -*-
import re


def sub1(matchobj):
    return matchobj.group(1)
def gen_accusation_dict():
    fo_accusation_with_duplicated = open('accusation_with_duplicated.txt','r+',encoding='utf-8')
    fw_accusation_dict = open('accusation_dict2.txt','w+',encoding='utf-8')
    list_lines = fo_accusation_with_duplicated.readlines() #每行样例：60	3	因涉嫌犯合同诈骗罪\n
    list_accusations = []
    pattern = re.compile(u'^[因涉嫌犯]+(.*)')
    for i in range(len(list_lines)):
        list_lines[i] = list_lines[i].rstrip()
        accusation = re.sub(pattern,sub1,list_lines[i].split()[2])
        if(accusation not in list_accusations):
            list_accusations.append(accusation)

    sorted(list_accusations)
    for accusation in list_accusations:
        fw_accusation_dict.write(accusation+'\n')
    fo_accusation_with_duplicated.close()
    fw_accusation_dict.close()

def gen_accusation_dict_step2():
    fw_accusation_dict = open('accusation_dict2.txt', 'r+', encoding='utf-8')

if __name__ == '__main__':
    gen_accusation_dict()
