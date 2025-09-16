import subprocess
import yaml
import sys

# ================= НАСТРОЙКИ =================
SETTINGS_FILE = "CORE/B_RELOAD_ORDER.yaml"
YAML_KEY_RUNNER = "CHECK_IF_CANDLE_TIME_IS_3"
RUNNER_ON_VALUE = "true"

MAIN_SCRIPTS = [
    {"print": "CHECK_CANDLE_COLOR..."},
    "CORE/CAA_CHECK_IF_NEED_TO_CLOSE_PROMO_POPUP.py",
    "CORE/CAB_if_true.py",

    "TOOLS/click_CHECK_CANDLE_COLOR.py",

    "CORE/BBA_if_CANDLE_COLOR_is_GREEN.py",
    "CORE/BBB_if_CANDLE_COLOR_is_RED.py",
    "CORE/BBC_if_CANDLE_COLOR_is_ZERO.py",
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
