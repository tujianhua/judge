import json
fo = open('test_result.txt','r',encoding='utf-8')
line = fo.readline()
list_json = []
while line:
    data = json.loads(line.rstrip())
    list_json.append(data)
    line = fo.readline()

fo.close()

for i in range(len(list_json)):
    if i >100:
        break
    str = json.dumps(list_json[i])
    print(str)
