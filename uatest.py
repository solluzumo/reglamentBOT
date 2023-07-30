import docx
import json
def extract_headers_and_contents(doc_path):
    doc = docx.Document(doc_path)
    result = {}
    current_header = None

    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith("Heading"):
            current_header = paragraph.text.strip()
            result[current_header] = ""
        elif current_header:
            result[current_header] += paragraph.text.strip() + " "

    return result

def save_as_json(output_path, data):
    with open(output_path, "w+", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    doc_file_path = "static/Инструкция.DOCX"
    txt_output_path = "static/output"

    extracted_data = extract_headers_and_contents(doc_file_path)
    save_as_json(txt_output_path, extracted_data)  # Вызываем функцию сохранения в JSON формате

print("Преобразование завершено.")
