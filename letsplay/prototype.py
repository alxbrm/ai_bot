import win32api, win32con, win32gui, win32process
import time
import pyautogui
import subprocess
from time import sleep

import win32com.client
from pywinauto import Application


def click(x, y):
    # сначала выставляем позицию
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    # а потом кликаем (небольшая задержка для большей человечности)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def collect_all_windows(hwnd, collection):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        proc_id = win32process.GetWindowThreadProcessId(hwnd)
        wind_title = win32gui.GetWindowText(hwnd)
        m = []
        m.append(hwnd)
        m.append(wind_title)
        m.append(proc_id)
        collection.append(m)
        return True


def focus_window(wind_name):
    for i in collection:
        if wind_name in i[1]:
            hwnd = i[0]
            return hwnd


collection =[]

# xls = subprocess.Popen('C:/Users/ШЕФ/Documents/test.xls', shell=True)


win32gui.EnumWindows(collect_all_windows, collection)

m = focus_window('Excel')

print(m)

win32gui.SetForegroundWindow(m)
win32gui.BringWindowToTop(m)
win32gui.SetActiveWindow(m)
# win32gui.SetFocus(m)

print(win32gui.GetClientRect(m))
print(win32gui.GetWindowRect(m))
s = win32gui.GetDC(m)
print(s)
print(win32gui.GetWindowDC(m))
print(win32gui.GetClassName(m))
print(win32gui.WindowFromPoint((500, 500)))
print(pyautogui.size())
# win32gui.PaintDesktop(s)
# win32gui.LineTo(s, 800, 500)

for i in collection:
    print('{} '.format(i))


# xls.kill()
# xl = win32com.client.Dispatch("Excel.Application")
# xl.Visible = 1
# xl.Workbooks.Open('test.xls')
# xl.ActiveCell = "=2+1"
# xl.SaveWorkspace('test.xls')

# xl.SendKeys('вводим текст')
#
# print(xl)
# print(type(xl))
# print(xl.Visible)

# app = Application().start("notepad.exe")
# # # Выбираем пункт меню
# # app.UntitledNotepad.menu_select("Help->About Notepad")
# # # Симулируем клик
# # app.AboutNotepad.OK.click()
# # # Вводим текст
# app.UntitledNotepad.Edit.type_keys("Заработало!", with_spaces = True)

