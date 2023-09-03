import re
import json
def get_id(regulations,title):
    for key in regulations.keys():
        for subkey in regulations[key]:
            if title in regulations[key][subkey]:
                return regulations[key][subkey].index(title),subkey,key

def parse_regulations(file_path):
    regulations = {}
    current_section = None
    current_subsection = None
    diction = {}
    dicts = []
    jacor = False
    jacor_string = ""
    jacor_array = []
    with open(file_path, 'r', encoding='utf-8') as file:

        lines = file.readlines()


        for line in range(len(lines)-1):
            lines[line] = lines[line].strip()
            lines[line] = lines[line].replace("	","")
        for line in lines:
            line = line.strip()
            if line:
                # print(line)
                print(json.dumps(regulations, indent=4, ensure_ascii=False))

                # Проверка, является ли строка пунктом или подпунктом
                if re.match(r'^\d+\.\s', line):
                    # print(line.split()[-1])
                    # print(line.split()[-1].lower())
                    # Извлечение номера пункта
                    if line.split()[-1] == line.split()[-1].lower():
                        print(line)
                        current_subsection = line.replace("\n", "").replace("\t", "")

                        regulations[current_section][current_subsection] = {}
                        index = lines.index(line) + 1
                        if index != len(lines):
                            if not lines[index].startswith("•") and not lines[index].startswith("– ") and not lines[
                                index].startswith("") and not lines[index].startswith(""):
                                regulations[current_section][current_subsection] = current_subsection
                        else:
                            regulations[current_section][current_subsection] = current_subsection
                    else:
                        current_section = line.replace("\n", "").replace("\t", "")
                        regulations[current_section] = {}

                elif re.match(r'^\d+\.\d+\.\d+\.\d+\.\s', line):
                    element = regulations[current_section][current_subsection]
                    jacor = True

                    for index in range(len(element) - 1, -1, -1):
                        if not isinstance(element[index],dict):

                            if "".join(element[index].split(".")[:3])=="".join(line.split(".")[:3]):

                                if not diction:
                                    diction[element[index]] = []
                                    if jacor_array:
                                        for jacor_line in jacor_array:
                                            diction[element[index]].append(jacor_line.replace("\n", "").replace("\t", ""))
                                        jacor_array = []

                                    diction[element[index]].append(line.replace("\n", "").replace("\t", ""))
                                else:
                                    if element[index] in diction.keys():
                                        if jacor_array:
                                            for jacor_line in jacor_array:
                                                diction[element[index]].append(
                                                    jacor_line.replace("\n", "").replace("\t", ""))
                                            jacor_array = []

                                        diction[element[index]].append(line)
                                        index = lines.index(line) + 1
                                        if index != len(lines):
                                            if not "".join(lines[index].split(".")[:3]) == "".join(line.split(".")[:3]):
                                                diction_key = list(diction.keys())[0]
                                                id, subkey, key = get_id(regulations, diction_key)
                                                regulations[key][subkey][id] = diction
                                                jacor = False
                                    else:
                                        diction = {}
                                        diction[element[index]] = []
                                        if jacor_array:
                                            for jacor_line in jacor_array:
                                                diction[element[index]].append(
                                                    jacor_line.replace("\n", "").replace("\t", ""))
                                            jacor_array = []
                                        diction[element[index]].append(line.replace("\n", "").replace("\t", ""))
                                break

                elif re.match(r'^\d+\.\d+\.\s', line):
                    # print(line)
                    # Извлечение номера подпункта
                    current_subsection = line.replace("\n", "").replace("\t", "")

                    regulations[current_section][current_subsection] = {}
                    index = lines.index(line) + 1
                    if index != len(lines):
                        if not lines[index].startswith("•") and not lines[index].startswith("– ") and not lines[index].startswith("") and not lines[index].startswith(""):
                            regulations[current_section][current_subsection] = current_subsection
                    else:
                        regulations[current_section][current_subsection] = current_subsection


                else:
                    # for ida in range(lines.index(line),0,-1):
                    #     if re.match(r'^\d+\.\s', lines[ida]):
                    #         current_subsection = lines[ida].replace("\n", "").replace("\t", "")
                    #         regulations[current_section][current_subsection] = {}
                    #         break
                    # Добавление текста в текущий подпункт
                    if current_subsection:
                        if line.startswith("•") or line.startswith("") or line.startswith("– ") or line.startswith("") or line.startswith("- "):
                            element = regulations[current_section][current_subsection]
                            # print(json.dumps(diction, indent=4, ensure_ascii=False))
                            if not element:
                                element = []
                                element.append(line)
                            else:
                                if not isinstance(element,list):
                                    previous = element
                                    element = []
                                    element.append(previous)
                                if isinstance(element,list):
                                    for index in range(len(element)-1,-1,-1):

                                        if not element[index].startswith("•") and not element[index].startswith("") and not element[index].startswith("– ") and not element[index].startswith("")\
                                                and not element[index].startswith("- "):
                                            if not diction:
                                                diction[element[index]] = []
                                                diction[element[index]].append(line.replace("\n", "").replace("\t", ""))

                                            else:

                                                if element[index] in diction.keys():
                                                    diction[element[index]].append(line)
                                                    index = lines.index(line)+1
                                                    if index != len(lines):
                                                        if not lines[index].startswith("•") and not lines[index].startswith("") and not lines[index].startswith("– ") and not lines[index].startswith("")\
                                                                and not lines[index].startswith("- "):
                                                            diction_key = list(diction.keys())[0]
                                                            id,subkey,key = get_id(regulations,diction_key)
                                                            if isinstance(regulations[key][subkey],str):
                                                                regulations[key][subkey] = diction
                                                            else:
                                                                # print(json.dumps(regulations[key], indent=4, ensure_ascii=False))
                                                                regulations[key][subkey][id] = diction
                                                            dicts.append(diction)
                                                else:
                                                    diction = {}
                                                    diction[element[index]] = []
                                                    diction[element[index]].append(line.replace("\n", "").replace("\t", ""))
                                            break
                        elif not current_subsection in regulations[current_section].keys():
                            current_subsection = line
                            regulations[current_section][current_subsection] = line
                        elif regulations[current_section][current_subsection]:
                            if not isinstance(regulations[current_section][current_subsection], list):
                                previous = regulations[current_section][current_subsection]
                                regulations[current_section][current_subsection] = []
                                regulations[current_section][current_subsection].append(line.replace("\n", "").replace("\t", ""))

                            regulations[current_section][current_subsection].append(line.replace("\n", "").replace("\t", ""))
                            if jacor:
                                jacor_array.append(line)

                        else:
                            regulations[current_section][current_subsection] = line.replace("\n", "").replace("\t", "")

                    # Иначе, добавление текста в текущий пункт



        return regulations,dicts


regulations_data,dicts = parse_regulations('example')
print(json.dumps(regulations_data, indent=4, ensure_ascii=False))

# for diction in dicts:
#     for key,titles in diction.items():
#         for title in titles:
#             print(json.dumps(regulations_data, indent=4, ensure_ascii=False))
#             print(title,key)
#             id, subkey, key = get_id(regulations_data, title)
#             regulations_data[key][subkey].pop(id)

#reglament-abbreviation

#заменить массивы на словари
file_name ="ПРИЛОЖЕНИЕ 7 К ПОЛОЖЕНИЮ КОМПАНИИ «ИССЛЕДОВАНИЕ КЕРНА» СПЕЦИАЛЬНЫЕ ИССЛЕДОВАНИЯ КЕРНА. АЛГОРИТМ НАПИСАНИЯ РАЗДЕЛА «ЛИТОЛОГО-ПЕТРОФИЗИЧЕСКАЯ ХАРАКТЕРИСТИКА ОБЪЕКТА» В ОТЧЕТ № П1-01.03 Р-0136"

# file = open(f"static/text/reglaments/{file_name[:183]}", 'w+', encoding="utf-8")
# file.write(json.dumps(regulations_data, indent=4, ensure_ascii=False))
#
# accordance = open(f"static/text/reglament-abbreviation", 'a', encoding="utf-8")
# accordance.write(f"{file_name[:183]}~~{file_name}\n")
# if len(file_name)>183:
#     glossary = open(f"static/text/reglaments-accordance/glossary_{file_name[:183]}","w+")
#     glossary.close()
# else:
#     glossary = open(f"static/text/reglaments-accordance/glossary_{file_name}","w+")
#     glossary.close()