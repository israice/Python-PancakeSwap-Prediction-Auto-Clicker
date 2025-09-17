import tkinter as tk
from pynput.mouse import Listener
import threading
import os
import platform
import ctypes
from ctypes import wintypes
import win32gui
import win32con

# Настройки
IMAGE_PATH = "CORE/B_SETUP/CLICK_WINNINGS_COLOR/AA_image_CLICK_WINNINGS_COLOR.png"
SCALE_FACTOR = 1  # Уменьшение размера в 2 раза (50%)
BORDER_OFFSET = 10  # Отступ от края экрана в пикселях
POSITION = "bottom_left"  # Варианты: "top_left", "bottom_left", "top_right", "bottom_right"
SETTINGS_FILE = "CORE/Y_DATA/C_flow.yaml"  # Путь к файлу настроек
VARIABLE_NAME = "CLICK_WINNINGS_COLOR"  # Имя переменной для сохранения координат

# ---- DPI awareness (важно для корректных координат на Windows) ----
def _make_dpi_aware():
    if platform.system() != "Windows":
        return
    try:
        user32 = ctypes.windll.user32
        try:
            user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
            return
        except Exception:
            pass
        shcore = ctypes.windll.shcore
        PROCESS_PER_MONITOR_DPI_AWARE = 2
        shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    except Exception:
        user32.SetProcessDPIAware()

# ---- WinAPI типы/функции ----
class RECT(ctypes.Structure):
    _fields_ = [("left", wintypes.LONG),
                ("top", wintypes.LONG),
                ("right", wintypes.LONG),
                ("bottom", wintypes.LONG)]

class MONITORINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.DWORD),
                ("rcMonitor", RECT),
                ("rcWork", RECT),
                ("dwFlags", wintypes.DWORD)]

user32 = ctypes.windll.user32
user32.GetMonitorInfoW.argtypes = [wintypes.HMONITOR, ctypes.POINTER(MONITORINFO)]
user32.GetMonitorInfoW.restype = wintypes.BOOL

MonitorEnumProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL, wintypes.HMONITOR, wintypes.HDC, ctypes.POINTER(RECT), wintypes.LPARAM
)
user32.EnumDisplayMonitors.argtypes = [wintypes.HDC, ctypes.c_void_p, MonitorEnumProc, wintypes.LPARAM]
user32.EnumDisplayMonitors.restype = wintypes.BOOL

MONITOR_DEFAULTTONEAREST = 2
user32.MonitorFromPoint.argtypes = [wintypes.POINT, wintypes.DWORD]
user32.MonitorFromPoint.restype = wintypes.HMONITOR

def _enum_monitors():
    monitors = []
    def _cb(hmon, hdc, lprc, lparam):
        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)
        if user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
            x = mi.rcMonitor.left
            y = mi.rcMonitor.top
            w = mi.rcMonitor.right - mi.rcMonitor.left
            h = mi.rcMonitor.bottom - mi.rcMonitor.top
            monitors.append({"handle": hmon, "x": x, "y": y, "w": w, "h": h})
        return True
    cb = MonitorEnumProc(_cb)
    user32.EnumDisplayMonitors(0, None, cb, 0)
    return monitors

def _monitor_from_point(x, y):
    pt = wintypes.POINT(int(x), int(y))
    hmon = user32.MonitorFromPoint(pt, MONITOR_DEFAULTTONEAREST)
    mons = _enum_monitors()
    for i, m in enumerate(mons, start=1):
        if m["handle"] == hmon:
            m = m.copy()
            m["id"] = i
            return m
    if mons:
        m0 = mons[0].copy()
        m0["id"] = 1
        return m0
    return {"id": 1, "x": 0, "y": 0, "w": 0, "h": 0}

# ---- Работа с файлом настроек ----
def _update_line_in_text(text, var_name, new_line):
    lines = text.splitlines(keepends=True)
    if not lines:
        return new_line
    updated = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(f"{var_name}:"):
            indent = line[: len(line) - len(stripped)]
            nl = "\n" if line.endswith("\n") else "\n"
            lines[i] = f"{indent}{new_line.rstrip()}{nl}"
            updated = True
            break
    if not updated:
        if not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines.append(new_line if new_line.endswith("\n") else new_line + "\n")
    return "".join(lines)

def _save_variable_line(var_name, x_local, y_local, monitor_id):
    new_value_line = f"{var_name}: {x_local},{y_local},monitor={monitor_id}\n"
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            f.write(new_value_line)
        return
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        original = f.read()
    updated_text = _update_line_in_text(original, var_name, new_value_line)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        f.write(updated_text)

# ---- Основной код ----
_make_dpi_aware()

# Создаем окно
root = tk.Tk()
root.attributes('-topmost', True)
root.overrideredirect(True)

# Загружаем изображение
photo = tk.PhotoImage(file=IMAGE_PATH)

# Получаем оригинальные размеры изображения
original_width = photo.width()
original_height = photo.height()

# Уменьшаем размер на 50%
new_width = original_width // SCALE_FACTOR
new_height = original_height // SCALE_FACTOR
photo = photo.subsample(SCALE_FACTOR, SCALE_FACTOR)

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Вычисляем позицию в зависимости от настройки POSITION
if POSITION == "top_left":
    x_position = BORDER_OFFSET
    y_position = BORDER_OFFSET
elif POSITION == "bottom_left":
    x_position = BORDER_OFFSET
    y_position = screen_height - new_height - BORDER_OFFSET
elif POSITION == "top_right":
    x_position = screen_width - new_width - BORDER_OFFSET
    y_position = BORDER_OFFSET
elif POSITION == "bottom_right":
    x_position = screen_width - new_width - BORDER_OFFSET
    y_position = screen_height - new_height - BORDER_OFFSET
else:
    raise ValueError("Invalid POSITION value. Use 'top_left', 'bottom_left', 'top_right', or 'bottom_right'.")

# Создаем метку с изображением
label = tk.Label(root, image=photo, borderwidth=0)
label.pack()

# Устанавливаем позицию окна
root.geometry(f"{new_width}x{new_height}+{x_position}+{y_position}")

# Функция для отслеживания кликов мыши
def mouse_listener():
    def on_click(x, y, button, pressed):
        if pressed:
            mon = _monitor_from_point(x, y)
            x_local = int(x - mon["x"])
            y_local = int(y - mon["y"])
            _save_variable_line(VARIABLE_NAME, x_local, y_local, mon["id"])
            root.destroy()
            return False
    with Listener(on_click=on_click) as listener:
        listener.join()

# Запускаем слушатель мыши в отдельном потоке
thread = threading.Thread(target=mouse_listener)
thread.daemon = True
thread.start()

# Запускаем главный цикл Tkinter
root.mainloop()