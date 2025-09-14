#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys
from pathlib import Path, PurePosixPath

# ==== Настройки (только прямые слэши) ====
SETTINGS_FILE = "settings.yaml"   # путь к файлу настроек (ОТ base_dir)
CONFIG_KEY = "CANDLE_COLOR"      # имя ключа в YAML
CONFIG_CLICKS_EXPECTED = "RED"     # ожидаемое значение (регистр/кавычки игнорируются)

# base_dir по умолчанию — РОДИТЕЛЬ текущего файла (..)
BASE_DIR_POSIX = ".."             # можно поменять на "" (текущая папка) или абсолютный POSIX-путь

# Сценарии для запуска (ОТ base_dir):
#  - "TOOLS/file.py"                  -> запуск скрипта
#  - {"print": "message"}             -> просто вывести сообщение
#  - lambda: print("message")         -> выполнить произвольное действие без await
SCRIPTS_POSIX = [
    {"print": "RED..."},
    "TOOLS/click_CLICK_ENTER_DOWN.py",
]

def config_clicks_is_on(settings_path: str, key_name: str, expected_value: str) -> bool:
    """Простой парсер строки '<KEY>: <value>' без зависимостей."""
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.split("#", 1)[0].strip()
                if not line or ":" not in line:
                    continue
                key, value = line.split(":", 1)
                if key.strip() == key_name:
                    val = value.strip().strip("'\"").lower()
                    exp = expected_value.strip().strip("'\"").lower()
                    return val == exp
    except FileNotFoundError:
        print(f"[warn] Файл настроек не найден: {settings_path}")
    except Exception as e:
        print(f"[warn] Ошибка чтения {settings_path}: {e}")
    return False


async def run_script_posix(abs_path: Path) -> int:
    """Запускает один скрипт Python по абсолютному пути (печатает stdout/stderr)."""
    if not abs_path.exists():
        print(f"[skip] Не найден файл: {abs_path.as_posix()}")
        return 0

    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        abs_path.as_posix(),  # путь с прямыми слэшами
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if stdout:
        print(stdout.decode(errors="ignore"), end="")
    if stderr:
        print(stderr.decode(errors="ignore"), end="", file=sys.stderr)

    return proc.returncode


async def main() -> int:
    # base_dir = родитель текущего файла по умолчанию
    here = Path(__file__).parent
    base_dir = (here / PurePosixPath(BASE_DIR_POSIX)).resolve() if BASE_DIR_POSIX else here.resolve()

    settings_abs = (base_dir / PurePosixPath(SETTINGS_FILE)).resolve()

    # Проверяем ключ в настройках
    if not config_clicks_is_on(settings_abs.as_posix(), CONFIG_KEY, CONFIG_CLICKS_EXPECTED):
        return 0

    # Последовательно исполняем шаги
    for step in SCRIPTS_POSIX:
        # Шаг-печать через словарь {"print": "..."}
        if isinstance(step, dict) and "print" in step:
            print(str(step["print"]))
            continue

        # Любой вызываемый объект (например, lambda: print(...))
        if callable(step):
            try:
                ret = step()
                # если кто-то вернул код завершения — можно обработать
                if isinstance(ret, int) and ret != 0:
                    print(f"[error] Остановка: пользовательский шаг вернул код {ret}")
                    return ret
            except Exception as e:
                print(f"[warn] Ошибка в пользовательском шаге: {e}")
                return 1
            continue

        # Обычный путь к скрипту
        if isinstance(step, str):
            abs_path = (base_dir / PurePosixPath(step)).resolve()
            rc = await run_script_posix(abs_path)
            if rc != 0:
                print(f"[error] Остановка: скрипт вернул код {rc}")
                return rc
            continue

        # Неизвестный тип шага
        print(f"[warn] Неизвестный шаг, пропускаю: {step!r}")

    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[warn] Прервано пользователем (Ctrl+C).")
        exit_code = 130
    sys.exit(exit_code)
