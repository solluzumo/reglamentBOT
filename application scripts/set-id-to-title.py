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
                    if isinstance(zna1,list):
                        for el in zna1:
                            if isinstance(el,dict):
                                for iiz,z in el.items():
                                    sub_sub.append(iiz)
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
                                    if isinstance(zna, list):
                                        for el in zna:
                                            if isinstance(el, dict):
                                                for iiz, z in el.items():
                                                    sub_sub.append(iiz)
                                    for sub_keys_element in sub_sub:

                                        if not check_is(sub_keys_element,result):

                                            result.append([str(i), sub_keys_element])
                                            i += 1

    return result




file_name ="ПРИЛОЖЕНИЕ 7 К ПОЛОЖЕНИЮ КОМПАНИИ «ИССЛЕДОВАНИЕ КЕРНА» СПЕЦИАЛЬНЫЕ ИССЛЕДОВАНИЯ КЕРНА. АЛГОРИТМ НАПИСАНИЯ РАЗДЕЛА «ЛИТОЛОГО-ПЕТРОФИЗИЧЕСКАЯ ХАРАКТЕРИСТИКА ОБЪЕКТА» В ОТЧЕТ № П1-01.03 Р-0136"


data = json.loads(open(f"static/text/reglaments/{file_name[:183]}", encoding="utf-8").read())
keys = list(data.keys())
final = func(keys,data)

with open("../static/text/accordance", 'r', encoding="utf-8") as accordance_file:
    lines = accordance_file.readlines()
    if lines:
        last_line = lines[-1]
        last_id = int(last_line.split("~~")[0])
    else:
        last_id = 0

for entry in final:
    entry[0] = str(int(entry[0]) + last_id+1)

with open("../static/text/accordance", 'a', encoding="utf-8") as accordance_file:
    for entry in final:
        entry_line = "~~".join(entry)
        accordance_file.write(f"{entry_line}~~{file_name[:183]}\n")

print(final)