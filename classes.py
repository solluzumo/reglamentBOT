import search
import os

class Reglament:
    """
    Этот объект представляет регламент для найденоого по запросу пользователя заголовка.
    """

    def __init__(self, reg_name:str, glossary:str, full_reg_name:str):
        self.reg_name = reg_name
        self.glossary = glossary
        self.full_reg_name = full_reg_name
class Title:
    """
    Этот объект представляет найденный по запросу пользователя заголовок.
    """

    def __init__(self, title_id:str, title_name:str, photo:list[str]|None, table:list[str]|None,
                                    reglament:Reglament ,current_root:dict|None ,before_key:str):
        self.id = title_id
        self.title_name = title_name
        self.photo = photo
        self.table = table
        self.reglament = reglament
        self.current_root = current_root
        self.before_key = before_key

def get_image_filenames(folder_path):
    image_filenames = []
    for filename in os.listdir(folder_path):
        # Проверяем, что файл является изображением по расширению
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_filenames.append(filename)
    return image_filenames


def parse_string_reglament(reglament_string:str)->Reglament:
    """
    Эта функция принимает на вход название регламента из функции titles.parse_string_title(), находит соответствующий
    регламенту глоссарий и создает на основе этой информации объект reglaments.Reglament.
    :param reglament_string: str
    :return: reglaments.Reglament
    """
    reglaments_list = os.listdir("static/text/reglaments-accordance")
    reglament_string = reglament_string.strip()
    full_reg_name_list = open("static/text/reglament-abbreviation","r",encoding="utf-8").read().split("\n")
    full_reg_name = ""

    for string in full_reg_name_list:
        abbreviation = string.split("~~")[0]
        if abbreviation == reglament_string:
            full_reg_name = string.split("~~")[1]
    if len(full_reg_name)<1:
        if len(reglament_string)>183:
            full_reg_name = reglament_string[:183]
        else:
            full_reg_name = reglament_string
    for reglament_name in reglaments_list:
        if reglament_name == "glossary_"+reglament_string:
            reglament_file = open(f"static/text/reglaments-accordance/{reglament_name}", 'r', encoding='utf-8').read()
            reglament_glossary = reglament_file
    return Reglament(reglament_string, reglament_glossary,full_reg_name)


def pars_string_title(title_string:str, data:dict)->Title:
    """
    Эта функция принимает строку из accordance.txt и превращает ее в объект titles.Title
    :param title_string: str
    :param data: dict
    :return: titles.Title
    """

    title_info = title_string.split('~~')
    title_id = title_info[0]
    title_name = title_info[1]

    images_list = os.listdir('static/images')
    images_title_list = None

    for image_id in images_list:
        if image_id == title_id:
            images_title_list = get_image_filenames(f'static/images/{image_id}')
    photo = images_title_list

    tables_list = os.listdir('static/tables')
    tables_title_list = None
    for table_id in tables_list:
        if table_id == title_id:
            tables_title_list = os.listdir(f'static/tables/{table_id}')
    table = tables_title_list

    reglament = parse_string_reglament(title_info[2])
    current_root = search.find_value_by_key(data, title_name)
    before_key = search.get_key_by_key(data,title_name)

    return Title(title_id, title_name, photo, table, reglament, current_root,before_key)




