import pyautogui, win32clipboard, win32gui, subprocess, win32process
from time import sleep
from functions import collect_all_windows, focus_window, num_mouse_click, keyboard_click, collection

#калькулятор прозрачный - из-за этого проблемы с матчем картинок с кнопками
class BeginProc():
    def __init__(self, progname):
        self.progname = progname

    def go(self):
        subprocess.Popen('C://Windows.old//WINDOWS//System32//calc.exe', shell = True)
        sleep(5)
        win32gui.EnumWindows(collect_all_windows, collection)
        hwnd = focus_window(self.progname)
        self.operation = pyautogui.prompt(text='Введите цифры, которые хотите сложить(только однозначные)', default='пусто')
        win32gui.SetForegroundWindow(hwnd)
        self.Xpos, self.Ypos, Xsize, Ysize = win32gui.GetWindowRect(hwnd)
        sleep(2)


class DoOrNot(BeginProc):
    def __init__(self, progname = 'Калькулятор'):
        self.confirm = pyautogui.confirm(text='Подвердите выполение программы', title='Подтвердите действие', buttons=['YES', 'NO'])
        super().__init__(progname)

    def verify(self):
        if self.confirm == 'YES':
            self.go()
            print(self.operation)
            print(type(self.operation))
            # num_mouse_click(list(self.operation))
            keyboard_click(list(self.operation), self.Xpos, self.Ypos)
        else:
            exit()


make_interact = DoOrNot()

make_interact.verify()
