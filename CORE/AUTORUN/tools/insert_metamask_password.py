#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from pynput.keyboard import Controller as KeyboardController
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# ==== Настройки ====
NEW_VALUE = os.getenv("insert_metamask_password")  # берем значение из .env
TYPING_DELAY = 0.3  # задержка между символами в секундах
# ===================

def type_with_delay(keyboard, text):
    """Функция для посимвольного ввода текста с задержкой."""
    for char in text:
        keyboard.type(char)
        time.sleep(TYPING_DELAY)
    # Нажимаем Enter в конце (удалите, если не нужно)
    keyboard.press('\n')
    keyboard.release('\n')

def main():
    if NEW_VALUE is None:
        print("Ошибка: переменная 'insert_metamask_password' не найдена в .env")
        return

    # Инициализация контроллера клавиатуры
    keyboard = KeyboardController()

    # Даем пользователю 5 секунд, чтобы переключиться на поле ввода
    time.sleep(5)

    # Вводим текст посимвольно
    type_with_delay(keyboard, NEW_VALUE)

if __name__ == "__main__":
    main()