import subprocess
import yaml
import sys

# ================= НАСТРОЙКИ =================
SETTINGS_FILE = "CORE/A_AUTORUN/B_log_in.yaml"
YAML_KEY_RUNNER = "B_LOG_IN"
RUNNER_ON_VALUE = "on"

MAIN_SCRIPTS = [
    {"print": "Metamask Log In..."},
    "CORE/A_AUTORUN/tools/click_metamask_icon.py",
    "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "CORE/A_AUTORUN/tools/insert_metamask_password.py",
    "CORE/A_AUTORUN/tools/click_unlock_metamask.py",
    "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "TOOLS/click_REFRESH_BROWSER.py",
    "TOOLS/SYSTEM_MEDIUM_DELAY_IN_SECONDS.py",
    "CORE/A_AUTORUN/tools/click_pancake_log_in_button.py",
    "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "CORE/A_AUTORUN/tools/click_choose_metamask_wallet.py",
    "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "CORE/A_AUTORUN/tools/click_choose_network.py",
    "TOOLS/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    "CORE/A_AUTORUN/tools/click_metamask_connect_button.py",
    "TOOLS/SYSTEM_MEDIUM_DELAY_IN_SECONDS.py",
    "TOOLS/click_REFRESH_BROWSER.py",
    "TOOLS/SYSTEM_MEDIUM_DELAY_IN_SECONDS.py",
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
