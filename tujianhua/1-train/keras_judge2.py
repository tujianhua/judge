import keras
from keras.utils import  to_categorical
from keras.models import Sequential
from keras.layers import  Dense,Activation,Dropout,Flatten
from keras import optimizers
import random
import numpy as np
model = Sequential()
#model.add(Dense(units=256, input_shape=(145+9+9+9,)))  #特征维度=145+9+9+9
model.add(Dense(units=256, input_shape=(8+35,)))  #特征维度=最大金额范围（8位onehot)省编码（35位）
model.add(Dropout(0.5))
model.add(Activation("relu"))
model.add(Dense(units=256))
model.add(Dropout(0.5))
model.add(Activation("relu"))
model.add(Dense(units=128))
model.add(Dropout(0.5))
model.add(Activation("relu"))
model.add(Dense(units=8))
model.add(Activation("softmax"))

#model.add(Dense(units=1))
#model.add(Activation("relu"))
model.compile(optimizer='rmsprop',loss='mse',metrics=['accuracy'])
#sgd = optimizers.SGD(lr=0.01,decay=1e-6,momentum=0.9,nesterov=True)
#model.compile(loss='mean_squared_error',optimizer='sgd',metrics=['accuracy'])

def load_train_data_cyh(rfilepath_amount='t_amount.txt', wfilepath_province='train_case_area_province.txt'):
    #格式是id\t罚金范围(标签\t罪名\t金额最大值范围
    #样例：60	7	224,25,26,27,52,72	7
    fo = open(rfilepath_amount, 'r+', encoding='utf-8')
    fo_province = open(wfilepath_province, 'r+', encoding='utf-8')
    list_province = fo_province.readlines() #60	原公诉机关榆阳区人民检察院	610000	26
    list_lines = fo.readlines()   #样例：60	7	224,25,26,27,52,72	7
    for i in range(len(list_lines)):
        province_code = list_province[i].rstrip().split('\t')[3]
        list_lines[i] = list_lines[i].rstrip()+'\t'+province_code
    random.shuffle(list_lines)  #乱序化
    list_train_data0 = []
    list_train_data1 = []
    list_train_label0 = []
    for i in range(len(list_lines)): #60	7	224,25,26,27,52,72  7   26
        line = list_lines[i].rstrip()
        list_items = line.split('\t')
        list_train_data0.append(int(list_items[3])-1 ) #0-8
        list_train_data1.append(int(list_items[4]))
        list_train_label0.append(int(list_items[1]) - 1)

    list_train_data_onehot = keras.utils.to_categorical(list_train_data0, num_classes=8)  # 将0-8的整数
    list_train_data1_onehot = keras.utils.to_categorical(list_train_data1,num_classes=35)
    list_train_data_onehot = np.append(list_train_data_onehot,list_train_data1_onehot,axis=1)

    list_train_label_onehot = keras.utils.to_categorical(list_train_label0, num_classes=8)

    fo.close()
    return list_train_label_onehot,list_train_data_onehot

def load_data(filepath):
    fo = open(filepath, 'r+', encoding='utf-8')
    list_train_data = []
    list_train_label = []
    list_lines = fo.readlines()
    random.shuffle(list_lines) #乱序化
    #格式：序号\t标签(8)\t罪名(145),犯罪金额(9),退赔金额(9),自首(2),主从犯(3),累犯(2),立功(2)
    for i in range(len(list_lines)):
        line = list_lines[i].rstrip()
        list_items = line.split('\t')
        list_num = list_items[2].split(',')
        list_num = [float(x) for x in list_num]
        list_train_data.append(list_num[:145+9+9+9])
        list_num2 = list_items[1].split(',')
        list_num2 = [float(x) for x in list_num2]
        list_train_label.append(list_num2)
    fo.close()
    return list_train_label,list_train_data

#装载训练数据开始训练
def train(train_label,train_data):
#list_train_label_onehot,list_train_data_onehot = load_data('train_8.txt')
    model.fit(train_data,train_label,
               epochs=40,batch_size=4000,validation_split=0.2)
    #装载训练数据前100个样本进行预测以便人工验证
    validation_data = train_data[:100,:]  #onehot格式
    validation_label = train_label[:100,:] #onehot格式
    predicted_validateion_label = model.predict_classes(validation_data, batch_size=100, verbose=1)  #预测结果，整数0-7
    print('predicted result:\n')
    print(', '.join(str(l) for l in predicted_validateion_label))

    #验证数据的标签，把one-hot转成0-7的整数
    none_onehot_validation_label = []
    for item in validation_label:
        none_onehot_validation_label.append(np.argmax(item))
    print('label:\n')
    print(none_onehot_validation_label)

def load_test_data(rfilepath_amount='test_amount.txt', wfilepath_province='test_case_area_province.txt'):
    fo_amount = open(rfilepath_amount, 'r+', encoding='utf-8')
    fo_province = open(wfilepath_province, 'r+', encoding='utf-8')
    list_province = fo_province.readlines() #32	公诉机关海口市龙华区人民检察院	460000	20
    list_lines = fo_amount.readlines()   #格式：编号\t犯罪金额范围  样例：32 1
    for i in range(len(list_lines)):
        province_code = list_province[i].rstrip().split('\t')[3]
        list_lines[i] = list_lines[i].rstrip()+'\t'+province_code  #加上省份序号后格式：编号\t犯罪金额范围\t省份序号   样例： 32  1   20

    test_data = []
    test_data1 = []
    test_id = []
    for i in range(len(list_lines)):  #格式：编号\t犯罪金额范围\t省份序号   样例： 32  1   20
        line = list_lines[i].rstrip()
        list_items = line.split('\t')
        test_id.append(list_items[0])
        test_data.append(int(list_items[1]) - 1)  # 金额范围1-8转0-7
        test_data1.append(int(list_items[2]))

    list_test_data_onehot = keras.utils.to_categorical(test_data, num_classes=8)  # 将0-8的整数
    test_data1_onehot = keras.utils.to_categorical(test_data1, num_classes=35)
    list_test_data_onehot = np.append(list_test_data_onehot, test_data1_onehot, axis=1)
    fo_amount.close()
    fo_province.close()
    return list_test_data_onehot,test_id


#用测试数据进行测试，最终生成可提交的测试结果test_result.txt
def gen_test_result(list_test_data_onehot, test_id):
    fw2 = open('test_result.txt','w+',encoding='utf-8')
    predicted_test_label = model.predict_classes(list_test_data_onehot, batch_size=100, verbose=1)
    list_predicted_test_label = predicted_test_label.tolist()
    #{"id":32,"penalty":1,"laws":[133]}
    for i in range(len(test_id)):
        str_line = '{"id":'+test_id[i]+',"penalty":'+str(list_predicted_test_label[i]+1)+',"laws":[133]}' #predicted_test_label加1，把0-7转回1-8
        fw2.write(str_line+'\n')
    fw2.close()

if __name__ == '__main__':

    list_train_label_onehot, list_train_data_onehot = load_train_data_cyh('t_amount.txt', wfilepath_province='train_case_area_province.txt')
    train(list_train_label_onehot, list_train_data_onehot)
    list_test_data_onehot, test_id = load_test_data()  #加载测试数据特征值和数据id
    gen_test_result(list_test_data_onehot, test_id)




