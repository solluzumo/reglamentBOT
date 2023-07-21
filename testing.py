def flatten_dict_recursive(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict_recursive(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def process_nested_dict(data, parent_key='', result=None):
    if result is None:
        result = []

    for key, value in data.items():
        new_key = f"{parent_key}_{key}" if parent_key else key
        if isinstance(value, dict):
            process_nested_dict(value, new_key, result)
        else:
            if parent_key:
                last_key = parent_key.split('_')[-1]
                if not any(row[0] == last_key for row in result):
                    result.append([last_key])
                for row in result:
                    if row[0] == last_key:
                        row.append(value)
                        break
            else:
                result.append([key, value])

    return result

# Пример словаря
data = {
    "ключ1": {
        "значение1": 1,
        "значение2": {
            "значение2_1": "abc",
            "значение2_2": "def"
        },
        "значение3": 42
    },
    "ключ2": {
        "значение1": "hello",
        "значение2": {
            "значение2_1": "world",
            "значение2_2": "!"
        },
        "значение3": "foo"
    }
}

result = process_nested_dict(data)
print(result)
