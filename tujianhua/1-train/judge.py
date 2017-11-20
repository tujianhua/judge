# -*- coding: UTF-8 -*-
import re
def gen_law_title_dict():
#if (1 == 2):#是否执行本段代码的开关
    #生成新文件law_2.txt，法律条文每行只显示标题
    print("22")
    fo2 = open("form-laws.txt","r+",encoding='utf-8')
    fw2 = open("law_2.txt","w+")
    line = fo2.readline()
    while line:
        list = line.split('\t')
        matchobj = re.search(r'【.*?】',list[1].decode('utf-8'))
        if(matchobj):
            string = matchobj.group().encode('utf-8')
            #string = list[0]+' '+string.encode('utf-8')
            fw2.write(string+'\n')
        line = fo2.readline()
    fo2.close()
    fw2.close()
def gen_crime_title_and_amount():
#生成新文件train_2.txt，按样例格式显示：犯合同诈骗罪,2000元,1000元 60 7 224,25,26,27,52,72
#if (1 == 2):#是否执行本段代码的开关
    fo = open("train.txt","r+",encoding='utf-8')
    fw = open("train_2.txt","w+",encoding='utf-8')
    pattern = re.compile( u'犯[^犯，。罪].{1,12}?罪')
    pattern_amount = re.compile(u'.{1,10}[0-9\.，]+[多余万千]*元[^0-9]{0,10}')

    str = fo.readline()
    while str:
       # print "str = ",str.decode('utf-8')[0:200].encode('utf-8')
        str = str.strip()
        list = str.split("\t")
      #  print  (list[0],list[2],list[3])
       # string = list[1].decode('utf-8')[0:200].encode('utf-8')+"\n"
       # stringmatch = re.search(pattern,list[1].decode('utf-8'))
        list_zuiming = re.findall(pattern,list[1]) #找出所有罪名字符串
        list_amount_string = re.findall(pattern_amount,list[1])
        if(list_zuiming):
            #去重
            list_zuiming2 = sorted(set(list_zuiming),key=list_zuiming.index)
            stringmatch = ",".join(list_zuiming2)
        else:
            stringmatch = u"犯罪"
        stringmatch = stringmatch+","+",".join(list_amount_string)
        fw.write(stringmatch+" ")
        string = list[0] +" "+ list[2] +" "+list[3]+"\n"
        fw.write(string)
        str = fo.readline()
    fo.close()
    fw.close()

def gen_law_title():
#if (1 == 2):#是否执行本段代码的开关
    #生成新文件train_3.txt，将train_2里的法律条文序号转义成法律条文的标题,格式：犯非法行医罪, 291 7 336:【非法行医罪;非法进行节育手术罪】,67:【自首】
    # law_2里的罪名标题转成列表存在list_law里
    fo3 = open("law_2.txt","r",encoding='utf-8')
    list_law = fo3.readlines()
    for i in range(len(list_law)):
        list_law[i]=list_law[i].strip()
    fo3.close()
    #train_2里的法律条文序号转义成法律条文的标题，放在train_3.txt
    fo4 = open("train_2.txt",encoding='utf-8')
    fw4 = open("train_3.txt","w+",encoding='utf-8')
    line = fo4.readline()
    while line:
        list = line.strip().split(" ")
        list_law_item = list[3].split(",")
        list[3]=""
        zu_zui_ming = "0:【无名罪】"  #如果没查到罪名，则以此为默认值
        for i in range(len(list_law_item)):
            i_list_law = int(list_law_item[i]) -1
            if(i_list_law < len(list_law)):
                list_law_item[i] = list_law_item[i]+":"+ list_law[i_list_law]
            list[3]=list[3]+list_law_item[i]+","
        for law_item in list_law_item:  #从法律条文里找到以罪结尾的作为罪名
            if(law_item.find('罪】')>-1):
                zu_zui_ming = law_item
                break
            else:
                pass



        list[3] = (list[3])[0:-1] #删除最后的,号
        fw4.write(zu_zui_ming+"\t"+"\t".join(list)+"\n")
        line = fo4.readline()
    fo4.close()
    fw4.close()
def order_by_amount():
#if(1==2):
    #生成train_4,把数据按金额范围值排序
    fo5 = open("train_3.txt","r+",encoding='utf-8')
    fw5 = open("train_4.txt","w+",encoding='utf-8')
    list_lines = fo5.readlines()

    list_lines2 = sorted(list_lines,key=lambda line:(line.split("\t"))[3])
    for line in list_lines2:
        fw5.write(line)
    fo5.close()
    fw5.close()
def gen_zishou_zhufan_leifan_ligong():
#if(1==1):
    #生成train_5,增加字段：有无自首,主从犯,有无一般累犯,有无立功
    fo6 = open("train_4.txt","r+",encoding='utf-8')
    fw6 = open("train_5.txt","w+",encoding='utf-8')
    line = fo6.readline()
    list_law_fixed_order = ['','','',''] #有无自首,主从犯,有无一般累犯,有无立功
    while line:
        list_line = line.split("\t")
        list_line[-1] = list_line[-1].strip()
        list_law_items = list_line[-1].split(",")
        if(u'67:【自首】' in list_law_items):
            list_law_fixed_order[0]=u'有自首'
        else:
            list_law_fixed_order[0] = u'无自首'

        if(u'26:【主犯】' in list_law_items):
            list_law_fixed_order[1]=u'主犯'
        elif (u'27:【从犯】' in list_law_items):
            list_law_fixed_order[1] = u'从犯'
        else:
            list_law_fixed_order[1] = u'无主从'

        if(u'65:【一般累犯】' in list_law_items):
            list_law_fixed_order[2]=u'有累犯'
        else:
            list_law_fixed_order[2] = u'无累犯'

        if(u'68:【立功】' in list_law_items):
            list_law_fixed_order[3]=u'有立功'
        else:
            list_law_fixed_order[3] = u'无立功'
        list_line.extend(list_law_fixed_order)
        fw6.write("\t".join(list_line)+"\n")
        line = fo6.readline()
    fo6.close()
    fw6.close()

def gen_amount():
    fo7 = open("train_5.txt", "r+",encoding='utf-8')
    fw7 = open("train_6.txt", "w+",encoding='utf-8')
    line = fo7.readline()
    while line:
        list_line = line.split("\t")  #样例：犯盗窃罪,1只，内有现金人民币5000余元。同月,1只，内有现金人民币900余元。同月
        list_line[1] = list_line[1].rstrip(',') #去除最右边的分隔符,以防分割出空列
        list_amount_with_context = (list_line[1].split(","))[1:]  #把第1列的罪名去除，剩下的部分是：1只，内有现金人民币5000余元。同月,1只，内有现金人民币900余元。同月

        #pattern_amount = re.compile(u'(.*?)([0-9]+[，\.]?[0-9]+[多余]?元)(.*)')
        pattern_amount1 = re.compile(u'(.*?)([0-9]+[，][0-9]+[\.][0-9]+万?[多余]?元)([^0-9]{0,10})')
        pattern_amount2 = re.compile(u'(.*?)([0-9]+[\.][0-9]+万?[多余]?元)([^0-9]{0,10})')
        pattern_amount3 = re.compile(u'(.*?)([0-9]+万?[多余]?元)([^0-9]{0,10})')
        pattern_amount4 = re.compile(u'(.*?)([0-9]+[，][0-9]+万?[多余]?元)([^0-9]{0,10})')

        list_str_amounts = []
        list_str_returned_amount = []
        is_total = 0
        for i in range( len(list_amount_with_context)): # item in list_amount_with_context:
            item = list_amount_with_context[i]
            matchobj = re.match(pattern_amount1,item)
            if(matchobj == None):
                matchobj = re.match(pattern_amount2, item)
            if(matchobj == None):
                matchobj = re.match(pattern_amount3, item)
            if(matchobj == None):
                matchobj = re.match(pattern_amount4, item)
            if(matchobj ):
                str_amount = str(matchobj.group(2)).replace('，','').replace('多','').replace('余','').replace('元','')
                match_number = re.search(u'[\d\.]+', str_amount)
                if match_number:
                    number = float(match_number.group())
                    if re.search(u'万', str_amount):
                        number = number * 10000
                    if re.search(u'千', str_amount):
                        number = number * 1000
                    if re.search(u'百', str_amount):
                        number = number * 100
                    if re.search(u'十', str_amount):
                        number = number * 10
                    str_amount = str(number)
                #退赔的
                if(matchobj.group(1).find(u'退') > -1 or matchobj.group(1).find(u'赔') > -1):
                    list_str_returned_amount.append(str_amount)
                #罚金不计入，总计则只计一次,有与前面相同金额的则本次不再计入
                elif( matchobj.group(1).find('罚金')==-1 and str_amount not in list_str_amounts and is_total == 0):
                    list_str_amounts.append(str_amount)
                    if(matchobj.group(1).find('共计')>-1 or matchobj.group(1).find('总计')>-1 or matchobj.group(1).find('合计')>-1 ):
                        is_total = 1
                        list_str_amounts.clear()
                        list_str_amounts.append(str_amount)
                list_amount_with_context[i] = matchobj.group(1) + str_amount +'元'+ matchobj.group(3)
                if(len(list_str_returned_amount)==0):
                    list_str_returned_amount.append('0')
            else:
                list_str_amounts.append('0')
                list_str_returned_amount.append('0')
        try:
            flt_totalamount = sum([float(x) for x in list_str_amounts])
            flt_returned_totalamount = sum([float(x) for x in list_str_returned_amount])
        except Exception:
            print(Exception)


        line = line.rstrip()+'\t'+','.join(list_str_amounts)+'\t'+','.join(list_str_returned_amount)+'\t'+str(flt_totalamount)+'\t'+str(flt_returned_totalamount)
        try:
            fw7.write(str((line+'\n')))
        except Exception:
            print(Exception)
        line = fo7.readline()
    fo7.close()
    fw7.close()
    return
'''
def gen_crime_from_casetxt():
    fo8 = open("train_6.txt", "r+", encoding='utf-8')
    fw8 = open("train_7.txt", "w+", encoding='utf-8')
    line = fo8.readline()
    while line:
        list_lines = line.split("\t")  # 样例：犯盗窃罪,1只，内有现金人民币5000余元。同月,1只，内有现金人民币900余元。同月
        list_lines[1] = list_lines[1].rstrip(',')  # 去除最右边的分隔符,以防分割出空列
        list_amount_with_context = (list_lines[1].split(","))[
                                   1:]  # 把第1列的罪名去除，剩下的部分是：1只，内有现金人民币5000余元。同月,1只，内有现金人民币900余元。同月
        line = fo8.readline()
    fo8.close()
    fw8.close()
'''
def gen_accusationdict_from_casetxt():
    fo8 = open("train_6.txt", "r+", encoding='utf-8')
    fw8 = open("train_7.txt", "w+", encoding='utf-8')
    line = fo8.readline()
    list_accusationdict = []
    while line:
        list_line = line.split("\t")
        list_line[0] = list_line[0].rstrip(',')
        list_accusationdict.append(list_line[0])
        line = fo8.readline()
    list_accusationdict_sorted = sorted(set(list_accusationdict),key=lambda item:item.split(':')[0])
    for item in list_accusationdict_sorted:
        fw8.write(item+'\n')
    fo8.close()
    fw8.close()
def transform_amount_to_scope(amount):
    if(amount==0):
        return 0
    if amount > 0 and amount <= 1000:
        return 1
    if amount > 1000 and amount <=2000:
        return 2
    if amount > 2000 and amount <=3000:
        return 3
    if amount > 3000 and amount <=4000:
        return 4
    if amount > 4000 and amount <=5000:
        return 5
    if amount > 5000 and amount <=10000:
        return 6
    if amount > 10000 and amount <=500000:
        return 7
    if amount > 500000:
        return 8

def normalizate(min,max,value):
    return (value - min)*1.0/(max - min)

def onehot_for_int_value(int_value, length): #int_value是1到length之间的整数
    list_onehot = [0] * length
    list_onehot[int_value-1] = 1
    return list_onehot
def gen_onehot_for_case_accusation():
    fo9 = open("train_6.txt", "r+", encoding='utf-8')
    fo9dict = open("accusation_dict.txt", "r+", encoding='utf-8')
    fw9 = open("train_8.txt", "w+", encoding='utf-8')
    list_accusation_dict = fo9dict.readlines()
    for i in range(len(list_accusation_dict)):#去除readlines后带来的换行符
        list_accusation_dict[i]=list_accusation_dict[i].rstrip('\n')

    #line的样例
    #264:【盗窃罪】	犯盗窃罪,携带的挎包内扒出现金815.5元、价值,62元的华为牌手机一部及小	974 1	264:【盗窃罪】,53:【罚金的缴纳、减免】	有自首	无主从	无累犯	无立功	815.5,62.0	0	877.5	0.0
    line = fo9.readline()

    while line:
        list_line = line.rstrip().split("\t")
        list_accusation_onehot = [0]*len(list_accusation_dict)  #145长度的list，值为0
        list_zisou_onehot = [0]*2 #自首，0：无自首，1：有自首
        list_zhucongfan_onehot = [0]*3 #0：无，1：从犯，2：主犯
        list_leifan_onehot = [0]*2 #0:无累犯，1:有累犯
        list_ligong_onehot = [0]*2 #0:无立功，1：有立功
        index = list_accusation_dict.index(list_line[0])
        list_accusation_onehot[index] = 1
        if(list_line[5] == '无自首'):
            list_zisou_onehot[0] = 1
        else:
            list_zisou_onehot[1] = 1

        if (list_line[6] == '无主从'):
            list_zhucongfan_onehot[0] = 1
        elif(list_line[6] == '从犯'):
            list_zhucongfan_onehot[1] = 1
        else:
            list_zhucongfan_onehot[2] = 1

        if (list_line[7] == '无累犯'):
            list_leifan_onehot[0] = 1
        else:
            list_leifan_onehot[1] = 1

        if (list_line[8] == '无立功'):
            list_ligong_onehot[0] = 1
        else:
            list_ligong_onehot[1] = 1
        total_amount_scope = transform_amount_to_scope(float(list_line[11]))
       # total_amount_normalized = normalizate(1,8,total_amount_scope)
        returned_amount_scope = transform_amount_to_scope(float(list_line[12]))
       # returned_amount_normalized = normalizate(1,8,returned_amount_scope)
     #   label_normalized = normalizate(1, 8, float(list_lines[3]))
        list_label_onehot = onehot_for_int_value( int(list_line[3]),8)
        line_onehot = list_line[2]+'\t'+ ','.join(str(item) for item in list_label_onehot) #编号 罚金范围（答案）
        line_onehot = line_onehot +'\t'+ ','.join(str(item) for item in list_accusation_onehot)  #数字型列表转成字符串，以逗号分隔index=0-144
        # line_onehot = line_onehot +','+str(total_amount_scope)
        # line_onehot = line_onehot + ','+str(returned_amount_scope)

        #index = 145-153 犯罪金额共8位
        if total_amount_scope==0:
            print('total_amount_scop is 0\n')
            pass
        list_amount_scope_onehot = onehot_for_int_value(total_amount_scope+1,9)   #total_amount_scop 是0-8的数，转成1-9的数
        line_onehot = line_onehot + ',' + ','.join(str(item) for item in list_amount_scope_onehot)

        # index = 154-162 退赔金额共8位
        list_returned_amount_scope_onehot = onehot_for_int_value(returned_amount_scope+1, 9)
        line_onehot = line_onehot + ',' + ','.join(str(item) for item in list_returned_amount_scope_onehot)

        line_onehot = line_onehot +','+','.join(str(item) for item in list_zisou_onehot)
        line_onehot = line_onehot +','+','.join(str(item) for item in list_zhucongfan_onehot)
        line_onehot = line_onehot +','+','.join(str(item) for item in list_leifan_onehot)
        line_onehot = line_onehot +','+','.join(str(item) for item in list_ligong_onehot)

#line_onehot格式：序号\t标签(8)\t罪名(145),犯罪金额(8),退赔金额(8),自首(2),主从犯(3),累犯(2),立功(2)
        fw9.write(line_onehot+'\n')
        line = fo9.readline()
    fo9.close()
    fo9dict.close()
    fw9.close()


if __name__ == '__main__':
   # gen_law_title_dict() #生成新文件law_2.txt，法律条文每行只显示标题
   # gen_crime_title_and_amount()  #生成新文件train_2.txt，按样例格式显示：犯合同诈骗罪,2000元,1000元 60 7 224,25,26,27,52,72
  #  gen_law_title() #生成新文件train_3.txt，将train_2里的法律条文序号转义成法律条文的标题,格式：犯非法行医罪, 291 7 336:【非法行医罪;非法进行节育手术罪】,67:【自首】
   # order_by_amount() #生成train_4,把数据按金额范围值排序
  #  gen_zishou_zhufan_leifan_ligong()  #生成train_5,增加字段：有无自首,主从犯,有无一般累犯,有无立功
  #  gen_amount()
  #  gen_accusationdict_from_casetxt()
    gen_onehot_for_case_accusation()
    print("aa")  #无意义，用于调试，执行完前面的代码不会直接退出.




