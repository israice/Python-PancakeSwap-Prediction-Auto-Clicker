import subprocess
import yaml
import sys

# ================= НАСТРОЙКИ =================
SETTINGS_FILE = "settings.yaml"
YAML_KEY_RUNNER = "STRATEGY_TYPE"
RUNNER_ON_VALUE = "SHORT"

MAIN_SCRIPTS = [
    {"print": "RELOAD ORDER..."},

    "CORE/D_FLOW/B_RELOAD_ORDER/tools/click_the_CHECK_IF_NEED_TO_CLOSE_PROMO_POPUP.py",    
        "CORE/D_FLOW/B_RELOAD_ORDER/tools/SYSTEM_SMALL_DELAY_IN_SECONDS.py",
    
    "CORE/D_FLOW/B_RELOAD_ORDER/BCAB_run_short.py",

    "CORE/D_FLOW/B_RELOAD_ORDER/BCAE_if_CANDLE_COLOR_is_RED.py",
    
    "CORE/D_FLOW/A_RELOAD_ALL/tools/enable_STRATEGY_TYPE_BOTH.py",
    "CORE/D_FLOW/A_RELOAD_ALL/tools/enable_STRATEGY_GO_WITH_FLOW.py",
    "CORE/Z_TOOLS/next_desktop.py",
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
