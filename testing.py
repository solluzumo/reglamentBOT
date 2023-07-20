import json
def format_text_from_json(json_data):
    formatted_text = ""

    for texts in json_data.values():
        for text in texts:
            if text.strip():
                formatted_text += f"⦁ {text.lstrip('-')}\n"

    return formatted_text

# Пример использования функции с вашим текстом
json_text  = open("text/fromprompt",encoding="utf-8").read()
print(json_text)