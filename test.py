import subprocess
import yaml
import sys

# Запуск если значения переменных одинаковые 
SETTINGS_FILE = "settings.yaml"
YAML_KEY_MAIN = "ALL_ROUNDS_COUNTER"

CONFIG_FILE = "CORE/AA_RECONFIG_CLICKS.yaml"
YAML_KEY_CONFIG = "MAXIMUM_ROUND_COUNTER_CONFIG"

MAIN_SCRIPTS = [
    "CORE/A_PRE_RESET.py",
    "CORE/B_RELOAD_ORDER.py",
    "CORE/C_RELOAD_ALL.py",
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
        print(f"[{i}/{len(scripts)}] Выполнение шага...")
        run_script(script)


def main():
    """Одиночный запуск при совпадении значений"""
    settings = load_yaml(SETTINGS_FILE)
    config = load_yaml(CONFIG_FILE)

    val_main = settings.get(YAML_KEY_MAIN)
    val_conf = config.get(YAML_KEY_CONFIG)

    print(f"{YAML_KEY_MAIN} = {val_main}, {YAML_KEY_CONFIG} = {val_conf}")

    if val_main == val_conf:
        print("→ Значения совпадают, запускаем MAIN_SCRIPTS...")
        run_script_list(MAIN_SCRIPTS)
    else:
        print("→ Значения НЕ совпадают, запуск отменён.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Пользователь прервал выполнение (Ctrl+C).")
        sys.exit(0)
