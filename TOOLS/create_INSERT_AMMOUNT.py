#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Обновляет INSERT_AMMOUNT в settings.yaml на
END_METAMASK_BNB_BALANCE / (MAXIMUM_ROUND_COUNTER_CONFIG + 1)
с точностью ровно 4 знака ПОСЛЕ точки (УСЕЧЕНИЕ, не округление).
Если итоговое записываемое значение < 0.001 — выставляет LOOP_RUNNER: off.

• Меняет только значения целевых ключей, сохраняя отступы/порядок/комментарии.
• Все настраивается переменными ниже.
"""

from decimal import Decimal, ROUND_DOWN, InvalidOperation
import re
from pathlib import Path

# ==========================
# НАСТРОЙКИ (меняйте здесь)
# ==========================
SETTINGS_PATH = "settings.yaml"       # путь к файлу (прямые слэши)
KEY_BALANCE   = "END_METAMASK_BNB_BALANCE"
KEY_ROUNDS    = "MAXIMUM_ROUND_COUNTER_CONFIG"
KEY_INSERT    = "INSERT_AMMOUNT"      # орфография как в файле
KEY_LOOP      = "LOOP_RUNNER"
DECIMALS      = 4                     # сколько знаков после точки
THRESHOLD_MIN = Decimal("0.001")      # порог для отключения лупа
LOOP_OFF_VAL  = "off"                 # что писать в LOOP_RUNNER при срабатывании порога
MAKE_BACKUP   = False                  # создавать .bak
ENCODING      = "utf-8"               # кодировка файла

# =============== НЕ ТРОГАТЬ НИЖЕ ===============
NUM_RE = r"[-+]?\d+(?:\.\d+)?"

def _find_number_by_key(text: str, key: str) -> Decimal:
    pattern = rf"(?m)^(?P<prefix>\s*{re.escape(key)}\s*:\s*)(?P<value>{NUM_RE})(?P<suffix>[^\n]*)$"
    m = re.search(pattern, text)
    if not m:
        raise ValueError(f"Ключ «{key}» не найден в файле.")
    raw = m.group("value")
    try:
        return Decimal(raw)
    except InvalidOperation:
        raise ValueError(f"Невозможно прочитать число у «{key}»: {raw!r}")

def _replace_number_by_key(text: str, key: str, new_value_str: str) -> str:
    pattern = rf"(?m)^(?P<prefix>\s*{re.escape(key)}\s*:\s*)(?P<value>{NUM_RE})(?P<suffix>[^\n]*)$"
    def _sub(m: re.Match) -> str:
        return f"{m.group('prefix')}{new_value_str}{m.group('suffix')}"
    new_text, n = re.subn(pattern, _sub, text, count=1)
    if n == 0:
        raise ValueError(f"Ключ «{key}» не найден для замены.")
    return new_text

def _replace_scalar_by_key(text: str, key: str, new_value_str: str) -> str:
    """
    Заменяет скалярное значение после `key:` (любое, не только число),
    аккуратно сохраняя комментарии/отступы и исходные кавычки, если они были.
    """
    pattern = rf"(?m)^(?P<prefix>\s*{re.escape(key)}\s*:\s*)(?P<value>[^\n#]*?)(?P<suffix>\s*(?:#.*)?)$"

    def _sub(m: re.Match) -> str:
        val = m.group("value")
        vtrim = val.strip()
        # Сохраняем кавычки, если они были
        if vtrim and len(vtrim) >= 2 and vtrim[0] == vtrim[-1] and vtrim[0] in ("'", '"'):
            q = vtrim[0]
            newv = f"{q}{new_value_str}{q}"
        else:
            newv = new_value_str
        return f"{m.group('prefix')}{newv}{m.group('suffix')}"

    new_text, n = re.subn(pattern, _sub, text, count=1)
    if n == 0:
        raise ValueError(f"Ключ «{key}» не найден для замены.")
    return new_text

def _append_key_value(text: str, key: str, value: str) -> str:
    # Добавляет "key: value" новой строкой в конец файла
    ending_newline = text.endswith("\n")
    line = f"{key}: {value}\n"
    return text + (line if ending_newline else "\n" + line)

def _format_truncated(value: Decimal, decimals: int) -> str:
    quant = Decimal("1").scaleb(-decimals)  # напр., 0.0001 при decimals=4
    q = value.quantize(quant, rounding=ROUND_DOWN)
    return f"{q:.{decimals}f}"

def main():
    path = Path(SETTINGS_PATH)
    if not path.exists():
        raise SystemExit(f"Файл не найден: {path}")

    text = path.read_text(encoding=ENCODING)

    balance = _find_number_by_key(text, KEY_BALANCE)
    rounds  = _find_number_by_key(text, KEY_ROUNDS)

    if rounds < 0:
        raise SystemExit(f"{KEY_ROUNDS} не может быть отрицательным: {rounds}")
    divisor = rounds + 1
    if divisor == 0:
        raise SystemExit("Деление на ноль: MAXIMUM_ROUND_COUNTER_CONFIG + 1 = 0")

    result = balance / divisor
    result_str = _format_truncated(result, DECIMALS)
    result_trunc_dec = Decimal(result_str)

    # Обновляем INSERT_AMMOUNT
    new_text = _replace_number_by_key(text, KEY_INSERT, result_str)

    # Порог: если < 0.001 — ставим LOOP_RUNNER: off
    loop_changed = False
    if result_trunc_dec < THRESHOLD_MIN:
        try:
            new_text = _replace_scalar_by_key(new_text, KEY_LOOP, LOOP_OFF_VAL)
        except ValueError:
            # ключа нет — добавим в конец
            new_text = _append_key_value(new_text, KEY_LOOP, LOOP_OFF_VAL)
        loop_changed = True

    if MAKE_BACKUP:
        path.with_suffix(path.suffix + ".bak").write_text(text, encoding=ENCODING)

    path.write_text(new_text, encoding=ENCODING)

if __name__ == "__main__":
    main()
