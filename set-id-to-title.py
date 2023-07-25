import json
import os
def check_is(sub_el,result):
    for el in result:
        if sub_el in el:
            return True
    return False
def func(keys,data):
    result = [[str(i),keys[i]] for i in range(len(list(keys)))]
    for key in keys:
        if str(type(data[key]))=="<class 'dict'>":
            for item1, zna1 in data[key].items():
                if isinstance(zna1, (dict, list)) and not item1 in result:
                    sub_sub = []
                    sub_sub.append(item1)
                    i = len(result)
                    for sub_keys_element in sub_sub:
                        if not check_is(sub_keys_element, result):
                            result.append([str(i), sub_keys_element])
                            i += 1
                    for sub_key in data[key]:
                        if str(type(data[key][sub_key]))=="<class 'dict'>":
                            for item,zna in data[key][sub_key].items():
                                if isinstance(zna, (dict, list)) and not item in result:
                                    sub_sub = []
                                    sub_sub.append(item)
                                    i = len(result)
                                    for sub_keys_element in sub_sub:
                                        if not check_is(sub_keys_element,result):
                                            result.append([str(i), sub_keys_element])
                                            i += 1

    return result



file_names = os.listdir('text/reglaments')
for file_name in file_names:
    data = json.loads(open(f"text/reglaments/{file_name}", encoding="utf-8").read())

    keys = list(data.keys())
    final = func(keys,data)
    file = open("text/accordance",'w',encoding="utf-8")
    for i in final:
        file.write("/".join([el for el in i]))
        file.write("/photo1/table1/reg1\n")
    file.close()
