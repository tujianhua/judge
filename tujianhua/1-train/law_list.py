# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 18:42:15 2017

@author: Helen
"""

import re

def import_law_list(txti):
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
    
    
if __name__ == "__main__":
    get_law_list()
    import_law_list("lawlist.txt")