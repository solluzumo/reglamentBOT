import reglaments
import search
import json

class Title:
    def __init__(self, title_id, title_name, photo, table, reglament,current_root,before_key):
        self.id = title_id
        self.title_name = title_name
        self.photo = photo
        self.table = table
        self.reglament = reglament  # Ссылка на объект Reglament
        self.current_root = current_root
        self.before_key = before_key

def pars_string_title(title_string:str, data)->Title:
    title_info = title_string.split('/')
    title_id = title_info[0]
    title_name = title_info[1]
    photo = title_info[2]
    table =title_info[3]
    reglament = reglaments.parse_string_reglament(title_info[4])
    current_root = search.find_value_by_key(data, title_name)
    before_key = search.get_key_by_key(data,title_name)
    return Title(title_id, title_name, photo, table, reglament, current_root,before_key)


