import os
class Reglament:
    def __init__(self, reg_name, glossary):
        self.reg_name = reg_name
        self.glossary = glossary

def parse_string_reglament(reglament_string:str)->Reglament:
    reglaments_list = os.listdir("text/reglaments-accordance")
    reglament_string = reglament_string.strip()
    for reglament_name in reglaments_list:
        if reglament_name == "glossary_"+reglament_string:
            reglament_file = open(f"text/reglaments-accordance/{reglament_name}", 'r', encoding='utf-8').read()
            reglament_glossary = reglament_file
            return Reglament(reglament_string, reglament_glossary)