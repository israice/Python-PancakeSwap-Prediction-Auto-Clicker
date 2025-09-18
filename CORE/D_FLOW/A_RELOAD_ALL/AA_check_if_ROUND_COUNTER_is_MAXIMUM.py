import subprocess
import yaml
import sys

# Запуск если значения переменных одинаковые 
SETTINGS_FILE = "settings.yaml"
YAML_KEY_MAIN = "MAXIMUM_ROUND_COUNTER_CONFIG"
# check if =
CONFIG_FILE = "settings_clicks.yaml"
YAML_KEY_CONFIG = "MAXIMUM_ROUND_COUNTER"

MAIN_SCRIPTS = [
    "CORE/D_FLOW/A_RELOAD_ALL/tools/enable_RESET.py",
    "CORE/B_RESET/A_run.py",
    # ##############################
    "CORE/D_FLOW/A_RELOAD_ALL/AAA_run_1_and_change_desktop_2.py",
    "CORE/D_FLOW/A_RELOAD_ALL/AAB_run_2_and_change_desktop_3.py",
    "CORE/D_FLOW/A_RELOAD_ALL/AAC_run_3_and_change_desktop_4.py",
    "CORE/D_FLOW/A_RELOAD_ALL/AAD_run_4_and_change_desktop_1.py",
]


def load_yaml(path: str) -> dict:
    """Читаем YAML файл"""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_script(script):
    """Запускает один шаг (print или python-скрипт)"""
    if isinstance(script, dict) and "print" in script:
        print(script["print"])
    elif isinstance(script, str):
        print(f"=== RUN {script} ===")
        subprocess.run(["python", script], check=False)
    else:
        print(f"[WARN] Неверный тип шага: {script}")


def run_script_list(scripts):
    """Выполняем список шагов по очереди"""
    for i, script in enumerate(scripts, start=1):
        run_script(script)


def main():
    """Одиночный запуск при совпадении значений"""
    settings = load_yaml(SETTINGS_FILE)
    config = load_yaml(CONFIG_FILE)

    val_main = settings.get(YAML_KEY_MAIN)
    val_conf = config.get(YAML_KEY_CONFIG)


    if val_main == val_conf:
        run_script_list(MAIN_SCRIPTS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
