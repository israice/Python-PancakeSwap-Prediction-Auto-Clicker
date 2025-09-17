import subprocess
import yaml
import sys

# Запуск если значения переменных одинаковые 
SETTINGS_FILE = "settings.yaml"
YAML_KEY_MAIN = "MAXIMUM_ROUND_COUNTER_CONFIG"
# check if =
CONFIG_FILE = "CORE/Y_DATA/C_flow.yaml"
YAML_KEY_CONFIG = "MAXIMUM_ROUND_COUNTER"

MAIN_SCRIPTS = [
    {"print": "Reloading ALL..."},
    "CORE/D_FLOW/A_RELOAD_ALL/tools/enable_RESET.py",
    "CORE/B_RESET/A_run.py",
    # ##############################
    "CORE/D_FLOW/A_RELOAD_ALL/AAA_CHECK_IF_NEED_TO_CLOSE_PROMO_POPUP.py",
    "CORE/D_FLOW/A_RELOAD_ALL/AAB_if_true.py",
    # ##############################
    "CORE/D_FLOW/A_RELOAD_ALL/tools/click_OPEN_HISTORY_SIDEBAR.py",
        "CORE/D_FLOW/A_RELOAD_ALL/tools/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "CORE/D_FLOW/A_RELOAD_ALL/tools/click_FILTER_BY_UNCOLLECTED.py",
        "CORE/D_FLOW/A_RELOAD_ALL/tools/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "CORE/D_FLOW/A_RELOAD_ALL/AAC_CHECK_WINNINGS_COLOR.py",
        "CORE/D_FLOW/A_RELOAD_ALL/tools/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "CORE/D_FLOW/A_RELOAD_ALL/AAD_if_true.py",    
    # ##############################
    "CORE/D_FLOW/A_RELOAD_ALL/tools/click_REFRESH_BROWSER.py",
        "CORE/D_FLOW/A_RELOAD_ALL/tools/SYSTEM_MEDIUM_DELAY_IN_SECONDS.py",
    "CORE/D_FLOW/A_RELOAD_ALL/tools/get_METAMASK_BNB_BALANCE.py",
    "CORE/D_FLOW/A_RELOAD_ALL/tools/create_INSERT_AMMOUNT_IN_BNB.py",
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
