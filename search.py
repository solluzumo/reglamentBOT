#Получение id заголовка по названию из accordance.txt
def find_index_by_line(search_string:str)->str:
    """
    Эта функция принимает на вход название заголовка и в файле accordance находит соответствующий индетификатор
    :param search_string: str
    :return: str
    """

    file_path = "static/text/accordance"
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            if search_string in line:
                return line.split('~~')[0]


#Получение строки по id из accorance.txt
def find_line_by_index(index:str)->str:
    """
    Эта функция зеркальна функции find_index_by_line, она принимает на вход индетификатор и в файле accordance
    находит соответствующую целую строку
    :param index: str
    :return: str
    """

    file_path = "static/text/accordance"
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            line_info = line.split('~~')
            if line_info[0] == index or line_info[1] == index:
                print(line_info, index)
                return line



def find_value_by_key(dictionary:dict, target_key:str)->dict|None:
    """
    Эта функция принимает представленный в виде словаря текст регламента и ключ и находит занчение, так как словарь
    имеет большую вложенность,используется рекурсивный метод.
    :param dictionary: dict
    :param target_key: str
    :return: dict or None
    """

    if target_key in dictionary:
        return dictionary[target_key]

    for key, value in dictionary.items():
        if isinstance(find_value_by_key(dictionary,key),list):
            for el in find_value_by_key(dictionary,key):
                if isinstance(el,dict):
                    for key,value in el.items():
                        if key == target_key:
                            return value
        if isinstance(value, dict):
            result = find_value_by_key(value, target_key)
            if result is not None:
                return result
    return None

#Получение ключа по его значению, используется рекурсивный метод, так как вложенность словарей достигает 3х уровней
def get_key_by_key(dictionary:dict, search_key:str)->dict|None|str:
    """
    Эта функция принимает представленный в виде словаря текст регламента и ключ и находит название ключа,
    в который входит указанный ключ, перебирая все уровни вложенности, так как словарь имеет большую вложенность,
    используется рекурсивный метод.
    :param dictionary: dict
    :param search_key: str
    :return: dict, если ключ найден
    :return: None, если указанный ключ не найден в словаре
    :return: str, если ключ найден, но не вложен(самые верхние уровни вложенности)
    """
    for key in dictionary.keys():
        if key == search_key:
            return "/start"
        if isinstance(dictionary[key],dict):
            for subkey in dictionary[key].keys():
                if isinstance(find_value_by_key(dictionary, subkey), list):
                    for el in find_value_by_key(dictionary, subkey):
                        if isinstance(el, dict):
                            for skey, value in el.items():
                                if skey == search_key:
                                    return subkey
                if search_key == subkey:
                    return key
                if isinstance(dictionary[key][subkey],dict):
                    for sub_sub in dictionary[key][subkey].keys():

                        if search_key == sub_sub:
                            return subkey
    return None