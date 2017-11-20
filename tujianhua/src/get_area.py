# -*- coding: UTF-8 -*-
import re

#生成province_ordered.txt，按行政编码从小到大排序
def gen_province_ordered():
    fo_province = open('province.csv', 'r+', encoding='utf-8')
    fw_province = open('province_ordered.txt', 'w+', encoding='utf-8')
    list_province = fo_province.readlines()
    list_province_ordered = sorted(list_province,key=lambda p:p.split()[0])  #p的格式：340000,安徽省，按第一列排序
    for line in list_province_ordered:
        fw_province.write(line)
    fw_province.close()
    fo_province.close()



#获取各省code列表，已排序
def get_list_province_code():
    fo_province_ordered = open('province_ordered.txt','r+',encoding='utf-8')
    list_province = fo_province_ordered.readlines()
    list_province_code = [p.split()[0] for p in list_province ]
    fo_province_ordered.close()
    return list_province_code

#从train.txt获取公诉机关名称，连同案例编号保存在case_area.txt，排序不变，没有获取到的以‘无名’标识，并保存在case_area_bad.txt，以便分析错误原因
def gen_case_area(rfilepath_orgdata='train.txt', wfilepath_case_area='train_case_area.txt',
                  wfilepath_case_area_bad='train_case_area_bad.txt'):
    fo_train = open(rfilepath_orgdata, 'r+', encoding='utf-8')
    fw = open(wfilepath_case_area, 'w+', encoding='utf-8')
    fw2 = open(wfilepath_case_area_bad, 'w+', encoding='utf-8')
    line = fo_train.readline()
    while line:
        list_line = line.rstrip().split('\t')
        case_txt = list_line[1]
        pattern = re.compile(u'.{5,20}(法院|检察院)')
        matchobj = re.search(pattern,case_txt)
        if(matchobj):
            fw.write(list_line[0] +'\t'+ matchobj.group()+'\n')
        else:
            fw.write(list_line[0] +'\t'+'无名'+'\n')
            fw2.write(line )
           # print(line)
        line = fo_train.readline()
    fo_train.close()
    fw.close()
    fw2.close()
#在case_area.txt基础上生成case_area_province.txt，添加省的行政编码和在字典中的位置序号
def gen_case_province(rfilepath_case_area='train_case_area.txt',
                      wfilepath_case_area_province ='train_case_area_province.txt'):
    fo_case_area = open(rfilepath_case_area, 'r+', encoding='utf-8')
    fo_province = open('province_ordered.txt','r+',encoding='utf-8')
    list_province_and_code = fo_province.readlines()
    try:
        list_province = [p.rstrip().split(',')[1] for p in list_province_and_code]
        list_provincecode = [p.rstrip().split(',')[0] for p in list_province_and_code]

        fo_city = open('city.csv','r+',encoding='utf-8')
        list_city_and_code = fo_city.readlines()
        list_city = [c.rstrip().split(',')[1] for c in list_city_and_code]
        list_citycode = [c.rstrip().split(',')[0] for c in list_city_and_code]
    except Exception:
        print('Exception1')
    fw = open(wfilepath_case_area_province,'w+',encoding='utf-8')
    try:
        line = fo_case_area.readline()
        while line:
            list_line = line.rstrip().split('\t') #line的样例：37178	公诉机关浙江省嘉善县人民检察院
            isfound = False
            line_with_province =  line.rstrip()
            for i in range(len(list_province)):
                if(list_line[1].find(list_province[i]) > -1):
                    isfound = True
                    line_with_province = line_with_province + '\t'+list_provincecode[i] +'\t'+str(i)
                    break
            if(isfound == False):
                for i in range(len(list_city)):
                    if(list_line[1].find(list_city[i]) > -1):
                        isfound = True
                        provincecode = (list_citycode[i])[:2]+'0000'  #地市代码后4位替换为4个0则变成省代码
                        index_of_province = list_provincecode.index(provincecode)
                        line_with_province = line_with_province + '\t' +  provincecode +'\t'+ str(index_of_province)
                        break
            if (isfound == False):
                print(line)
                line_with_province = line_with_province+'\t'+'999999'+'\t'+ str(list_provincecode.index('999999'))
            fw.write(line_with_province+'\n')
            line = fo_case_area.readline()
    except Exception:
        print('Excepton')
    fo_case_area.close()
    fw.close()
if __name__ == '__main__':
    # 调用函数生成province_ordered.txt
    #gen_province_ordered()
    gen_case_area(rfilepath_orgdata='train.txt',wfilepath_case_area='train_case_area.txt',
                  wfilepath_case_area_bad='train_caes_area_bad.txt')
    gen_case_province(rfilepath_case_area='train_case_area.txt',wfilepath_case_area_province='train_case_area_province.txt')
    gen_case_area(rfilepath_orgdata='test.txt', wfilepath_case_area='test_case_area.txt',
              wfilepath_case_area_bad='test_caes_area_bad.txt')
    gen_case_province(rfilepath_case_area='test_case_area.txt',
                  wfilepath_case_area_province='test_case_area_province.txt')


