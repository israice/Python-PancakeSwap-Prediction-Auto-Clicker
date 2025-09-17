import subprocess
import yaml
import sys

# ================= НАСТРОЙКИ =================
SETTINGS_FILE = "CORE/Y_DATA/A_runners.yaml"
YAML_KEY_RUNNER = "RUNNER_RECONFIG_CLICKS"
RUNNER_ON_VALUE = "on"

MAIN_SCRIPTS = [
    {"print": "START CONFIG CLICKS..."},
    # # =========================================================
    {"print": "Choose pixel for click_metamask_icon..."},
    # "CORE/C_SETUP/click_metamask_icon/A_run.py",    
    # {"print": "Choose pixel for click_unlock_metamask..."},
    # "CORE/C_SETUP/click_unlock_metamask/A_run.py",
    # {"print": "Choose pixel for click_pancake_log_in_button..."},
    # "CORE/C_SETUP/click_pancake_log_in_button/A_run.py",
    # {"print": "Choose pixel for click_choose_metamask_wallet..."},
    # "CORE/C_SETUP/click_choose_metamask_wallet/A_run.py",
    # {"print": "Choose pixel for click_choose_network..."},
    # "CORE/C_SETUP/click_choose_network/A_run.py",
    # {"print": "Choose pixel for click_metamask_connect_button..."},
    # "CORE/C_SETUP/click_metamask_connect_button/A_run.py",
    # # # =========================================================
    # {"print": "Choose pixel for CHECK_IF_NEED_TO_CLOSE_PROMO_POPUP..."},
    # "CORE/C_SETUP/CHECK_IF_NEED_TO_CLOSE_PROMO_POPUP/A_run.py",
    # {"print": "Choose pixel for CLICK_OPEN_HISTORY_SIDEBAR..."},
    # "CORE/C_SETUP/CLICK_OPEN_HISTORY_SIDEBAR/A_run.py",
    # {"print": "Choose pixel for CLICK_FILTER_BY_UNCOLLECTED..."},
    # "CORE/C_SETUP/CLICK_FILTER_BY_UNCOLLECTED/A_run.py",
    # {"print": "Choose pixel for CLICK_WINNINGS_COLOR..."},
    # "CORE/C_SETUP/CLICK_WINNINGS_COLOR/A_run.py",
    # {"print": "Choose pixel for CLICK_COLLECT_WINNINGS..."},
    # "CORE/C_SETUP/CLICK_COLLECT_WINNINGS/A_run.py",
    # {"print": "Choose pixel for CLICK_COLLECT_ALL_CONFIRM..."},
    # "CORE/C_SETUP/CLICK_COLLECT_ALL_CONFIRM/A_run.py",
    # {"print": "Choose pixel for CLICK_CONFIRM_METAMASK_ORDER..."},
    # "CORE/C_SETUP/CLICK_CONFIRM_METAMASK_ORDER/A_run.py",
    # {"print": "Choose pixel for CLICK_FINISH_AND_CLOSE_METAMASK..."},
    # "CORE/C_SETUP/CLICK_FINISH_AND_CLOSE_METAMASK/A_run.py",
    # {"print": "Choose pixel for CLICK_REFRESH_BROWSER..."},
    # "CORE/C_SETUP/CLICK_REFRESH_BROWSER/A_run.py",
    # # # =========================================================
    # {"print": "Choose pixel for CLICK_CANDLE_COLOR..."},
    # "CORE/C_SETUP/CLICK_CANDLE_COLOR/A_run.py",
    # {"print": "Choose pixel for CLICK_ENTER_UP..."},
    # "CORE/C_SETUP/CLICK_ENTER_UP/A_run.py",
    # {"print": "Choose pixel for CLICK_ENTER_DOWN..."},
    # "CORE/C_SETUP/CLICK_ENTER_DOWN/A_run.py",
    # {"print": "Choose pixel for CLICK_INSIDE_SET_POSITION..."},
    # "CORE/C_SETUP/CLICK_INSIDE_SET_POSITION/A_run.py",
    # {"print": "Choose pixel for CLICK_ON_PANCAKE_CONFIRM_BUTTON..."},
    # "CORE/C_SETUP/CLICK_ON_PANCAKE_CONFIRM_BUTTON/A_run.py",
    # {"print": "Choose pixel for CLICK_ON_METAMASK_CONFIRM_BUTTON..."},
    # "CORE/C_SETUP/CLICK_ON_METAMASK_CONFIRM_BUTTON/A_run.py",
    # {"print": "Choose pixel for CLICK_ON_CLOSE_METAMASK..."},
    # "CORE/C_SETUP/CLICK_ON_CLOSE_METAMASK/A_run.py",
    # # # =========================================================
    "CORE/C_SETUP/tools/disable_RECONFIG_CLICKS.py",
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
