# импортируем модули для работы с windows оберткой
# import win32api, win32con, win32gui
# import time, win32com.client

import win32api, win32gui, win32con

# функция клика в определенном месте
def click(x, y):
    # сначала выставляем позицию
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    # а потом кликаем (небольшая задержка для большей человечности)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


# данная функция - фильтр по выбору нужного окна (по названию этого окна)
def openItNow(hwnd, windowText):
    if windowText in win32gui.GetWindowText(hwnd):
        win32gui.SetForegroundWindow(hwnd)

# приступим
time.sleep(3)

# выбираем среди открытых окон то, которое содержит название Notepad
# заметьте что используется фильтр, описанный выше
win32gui.EnumWindows(openItNow, 'Notepad')

# нажимать на клавиши будет с помощью shell
shell = win32com.client.Dispatch("WScript.Shell")

# метод SendKeys программно нажимает на клавиши, поэтому далее записана последовательность нажатий
shell.SendKeys("%")
for i in range(0, 4, 1):
    shell.SendKeys("{RIGHT}")
    time.sleep(0.1)

shell.SendKeys("{DOWN}")
shell.SendKeys("{DOWN}")
shell.SendKeys("{DOWN}")
time.sleep(0.1)

shell.SendKeys("~")
time.sleep(7)

for i in range(0, 20, 1):
    shell.SendKeys("{PGUP}")
for i in range(0, 11, 1):
    shell.SendKeys("{DOWN}")

# здесь выполняем комбинацию клавиш Alt + 9
shell.SendKeys("%9")

# а теперь пара кликов
click(300, 700)
click(300, 600)

shell.SendKeys('вводим текст')
time.sleep(3)
# и опять комбинация
shell.SendKeys("^+{F1}")