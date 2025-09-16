import subprocess
import yaml
import sys

# Запуск если значения переменных одинаковые 
SETTINGS_FILE = "settings.yaml"
YAML_KEY_MAIN = "MAXIMUM_ROUND_COUNTER_CONFIG"
# check if =
CONFIG_FILE = "CORE/C_RELOAD_ALL.yaml"
YAML_KEY_CONFIG = "MAXIMUM_ROUND_COUNTER"

MAIN_SCRIPTS = [
    {"print": "Reloading ALL..."},
    "TOOLS/enable_RESET.py",
    "CORE/A_RESET.py",
    # ##############################
    "CORE/CAA_CHECK_IF_NEED_TO_CLOSE_PROMO_POPUP.py",
    "CORE/CAB_if_true.py",
    # ##############################
    "TOOLS/click_OPEN_HISTORY_SIDEBAR.py",
        "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "TOOLS/click_FILTER_BY_UNCOLLECTED.py",
        "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "CORE/CAC_CHECK_WINNINGS_COLOR.py",
        "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "CORE/CAD_if_true.py",    
    # ##############################
    "TOOLS/click_REFRESH_BROWSER.py",
        "TOOLS/SYSTEM_MEDIUM_DELAY_IN_SECONDS.py",
    "TOOLS/get_METAMASK_BNB_BALANCE.py",
    "TOOLS/create_INSERT_AMMOUNT_IN_BNB.py",
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
