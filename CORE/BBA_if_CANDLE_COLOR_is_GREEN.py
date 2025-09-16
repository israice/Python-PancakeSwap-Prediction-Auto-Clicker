import subprocess
import yaml
import sys

# ================= НАСТРОЙКИ =================
SETTINGS_FILE = "CORE/B_RELOAD_ORDER.yaml"
YAML_KEY_RUNNER = "CANDLE_COLOR"
RUNNER_ON_VALUE = "GREEN"

MAIN_SCRIPTS = [
    {"print": "GREEN..."},
    "TOOLS/click_CLICK_ENTER_UP.py",
        "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",

    "TOOLS/click_CLICK_INSIDE_SET_POSITION.py",
        "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "TOOLS/click_CLICK_ON_CONFIRM_AMMOUNT.py",
        "TOOLS/SYSTEM_MEDIUM_DELAY_IN_SECONDS.py",
    "TOOLS/click_CLICK_ON_METAMASK_ORDER.py",
        "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "TOOLS/click_CLICK_ON_CLOSE_EXTENSION.py",
        "TOOLS/SYSTEM_MEDIUM_DELAY_IN_SECONDS.py",

    "TOOLS/add_plus_1_to_ROUND_COUNTER.py",
    "TOOLS/add_plus_1_to_ALL_ROUNDS_COUNTER.py",
    
    "TOOLS/click_REFRESH_BROWSER.py",
    "TOOLS/SYSTEM_XXL_DELAY_IN_SECONDS.py",
    
]
# ==============================================


def load_settings():
    """Читаем настройки из файла settings.yaml"""
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_runner_on(value) -> bool:
    """Проверка YAML_KEY_RUNNER (строка или bool)."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == RUNNER_ON_VALUE.lower()
    return False


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
    """Одиночный запуск"""
    settings = load_settings()
    if is_runner_on(settings.get(YAML_KEY_RUNNER, "")):
        run_script_list(MAIN_SCRIPTS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
