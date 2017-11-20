import keras
from keras.utils import  to_categorical
from keras.models import Sequential
from keras.layers import  Dense,Activation,Dropout,Flatten
from keras import optimizers
import random
import numpy as np
model = Sequential()
#model.add(Dense(units=256, input_shape=(145+9+9+9,)))  #特征维度=145+9+9+9
model.add(Dense(units=256, input_shape=(8,)))  #特征维度=最大金额范围（8位onehot)
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

def load_data_cyh(filepath):
    #格式是id\t罚金范围(标签\t罪名\t金额最大值范围
    #样例：60	7	224,25,26,27,52,72	7
    fo = open(filepath,'r+',encoding='utf-8')
    list_lines = fo.readlines()
    random.shuffle(list_lines)  #乱序化
    list_train_data0 = []
    list_train_label0 = []
    for i in range(len(list_lines)):
        line = list_lines[i].rstrip()
        list_items = line.split('\t')
        list_train_data0.append(int(list_items[3])-1 ) #0-8
        list_train_label0.append(int(list_items[1]) - 1)

    list_train_data = keras.utils.to_categorical(list_train_data0, num_classes=8)  # 将0-8的整数
    list_train_label = keras.utils.to_categorical(list_train_label0, num_classes=8)

    fo.close()
    return list_train_label,list_train_data

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
#list_train_label_onehot,list_train_data_onehot = load_data('train_8.txt')
train_label,train_data = load_data_cyh('t_amount.txt')
model.fit(train_data,train_label,
           epochs=20,batch_size=2000,validation_split=0.2)


#装载训练数据前100个开始验证
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

fo2 = open('test_amount.txt','r+',encoding='utf-8')
fw2 = open('test_result.txt','w+',encoding='utf-8')
line = fo2.readline()
test_data = []
test_id = []
#生成one-hot格式的测试数据，并保持相同顺序的数据id
while line:
    list_items = line.rstrip().split('\t')
    test_data.append(int(list_items[1])-1)  #将1-8转成0-7，以方便转one-hot
    test_id.append(list_items[0])
    line = fo2.readline()
onehot_test_data = keras.utils.to_categorical(test_data,num_classes=8)
predicted_test_label = model.predict_classes(onehot_test_data,batch_size=100,verbose=1)
list_predicted_test_label = predicted_test_label.tolist()
#{“id”: “1”, “penalty”: 1，“laws”: [351,67,72,73]}
for i in range(len(test_id)):
    str_line = '{"id":'+test_id[i]+',"penalty":'+str(list_predicted_test_label[i]+1)+',"laws":[133]}'
    fw2.write(str_line+'\n')
fw2.close()
fo2.close()

