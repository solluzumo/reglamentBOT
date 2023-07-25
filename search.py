#Получение id заголовка по названию из accordance.txt
def find_index_by_line(search_string):
    file_path = "text/accordance"
    with open(file_path, 'r') as file:
        for line in file:
            if search_string in line:
                return line.split('/')[0]


#Получение строки по id из accorance.txt
def find_line_by_index(index):
    file_path = "text/accordance"
    with open(file_path, 'r') as file:
        for line in file:
            line_info = line.split('/')
            if line_info[0] == index or line_info[1] == index:
                return line



#Получение значения ключа из словаря, используется рекурсивный метод, так как вложенность словарей достигает 3х уровней
def find_value_by_key(dictionary, target_key):
    if target_key in dictionary:
        return dictionary[target_key]

    for key, value in dictionary.items():
        if isinstance(value, dict):
            result = find_value_by_key(value, target_key)
            if result is not None:
                return result
    return None


#Получение ключа по его значению, используется рекурсивный метод, так как вложенность словарей достигает 3х уровней

def get_key_by_key(d, search_key):
    for key in d.keys():
        if key == search_key:
            return "/start"
        if isinstance(d[key],dict):
            for subkey in d[key].keys():
                if search_key == subkey:
                    return key
                if isinstance(d[key][subkey],dict):
                    for sub_sub in d[key][subkey].keys():
                        if search_key == sub_sub:
                            return subkey
    return None
def get_key_by_value_recursive(d, value):
    for key, val in d.items():
        if val == value:
            return key
        elif isinstance(val, dict):
            nested_key = get_key_by_value_recursive(val, value)
            if nested_key is not None:
                return nested_key
    return None