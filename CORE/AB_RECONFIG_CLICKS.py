import subprocess
import yaml
import sys

# ================= НАСТРОЙКИ =================
SETTINGS_FILE = "CORE/AB_RECONFIG_CLICKS.yaml"
YAML_KEY_RUNNER = "AB_RECONFIG_CLICKS"
RUNNER_ON_VALUE = "on"

MAIN_SCRIPTS = [
    {"print": "RECONFIG CLICKS..."},
    # {"print": "Choose pixel for CHECK_CANDLE_COLOR..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CHECK_CANDLE_COLOR.py",
    # {"print": "Choose pixel for CLICK_ENTER_UP..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_ENTER_UP.py",
    # {"print": "Choose pixel for CLICK_ENTER_DOWN..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_ENTER_DOWN.py",
    # {"print": "Choose pixel for CLICK_INSIDE_SET_POSITION..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_INSIDE_SET_POSITION.py",
    # {"print": "Choose pixel for CLICK_ON_CONFIRM_AMMOUNT..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_ON_CONFIRM_AMMOUNT.py",
    # {"print": "Choose pixel for CLICK_ON_METAMASK_ORDER..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_ON_METAMASK_ORDER.py",
    # {"print": "Choose pixel for CLICK_ON_CLOSE_EXTENSION..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_ON_CLOSE_EXTENSION.py",
    # {"print": "Choose pixel for CHECK_IF_NEED_TO_CLOSE_PROMO_POPUP..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CHECK_IF_NEED_TO_CLOSE_PROMO_POPUP.py",
    # {"print": "Choose pixel for CHECK_IF_COLLECT_NEEDED..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CHECK_IF_COLLECT_NEEDED.py",
    # {"print": "Choose pixel for FILTER_BY_UNCOLLECTED..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_FILTER_BY_UNCOLLECTED.py",
    # {"print": "Choose pixel for CLICK_ON_COLLECT..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_ON_COLLECT.py",
    # {"print": "Choose pixel for CLICK_ON_COLLECT_ALL_CONFIRM..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_ON_COLLECT_ALL_CONFIRM.py",
    # {"print": "Choose pixel for CLICK_ON_CONFIRM_METAMASK_ORDER..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_ON_CONFIRM_METAMASK_ORDER.py",
    # {"print": "Choose pixel for CLICK_FINISH_AND_CLOSE_EXTENSION..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_FINISH_AND_CLOSE_EXTENSION.py",
    # {"print": "Choose pixel for CLICK_CLOSE_HISTORY_SIDEBAR..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_CLOSE_HISTORY_SIDEBAR.py",
    # {"print": "Choose pixel for CLICK_REFRESH_BROWSER..."},
    # "TOOLS/save_click.py",
    # "TOOLS/copy_click_to_CLICK_REFRESH_BROWSER.py",
    # # =========================================================
    "TOOLS/disable_RECONFIG_CLICKS.py",
]


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
