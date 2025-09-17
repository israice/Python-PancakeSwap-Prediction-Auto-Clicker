import re

# ###############################################
SOURCE_FILE = "CORE/Y_DATA/B_temp_data.yaml"
SOURCE_VAR = "PIXEL_CONFIG"
# ###############################################
TARGET_FILE = "CORE/Y_DATA/C_flow.yaml"
TARGET_VAR = "click_metamask_icon"
# ###############################################

# Чтение значения из исходного файла
with open(SOURCE_FILE, 'r', encoding='utf-8') as file:
    source_content = file.read()
    match = re.search(f"{SOURCE_VAR}:\\s*(\\S+)", source_content)
    if not match:
        raise ValueError(f"Переменная {SOURCE_VAR} не найдена в {SOURCE_FILE}")
    value = match.group(1)

# Обновление значения в целевом файле
with open(TARGET_FILE, 'r', encoding='utf-8') as file:
    target_content = file.read()

# Замена значения переменной
updated_content = re.sub(f"{TARGET_VAR}:\\s*\\S+", f"{TARGET_VAR}: {value}", target_content)

# Запись обновленного содержимого
with open(TARGET_FILE, 'w', encoding='utf-8') as file:
    file.write(updated_content)