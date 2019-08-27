import pyautogui, sys, time
import win32clipboard
import subprocess


# win32clipboard.OpenClipboard()
# data = win32clipboard.GetClipboardData()
# win32clipboard.CloseClipboard()

# pyautogui.alert(text='Тестовое инфоокно', title='Богатырушка', button='ЖМИИИИИИ')
#
# m = pyautogui.prompt(text='', title='Что введешь, то и получишь', default='Не ссы, введи...')
#
# print(data)
# print(m)
#
#
# ss = pyautogui.screenshot('test_screenshot.png', region=(100, 100, 500, 550))
#
# sleep(2)
#
# subprocess.Popen('test_screenshot.png', shell=True)
#
#
# print(ss)

def put_cursor_and_get_from_input(x_y):

    win32clipboard.OpenClipboard()

    win32clipboard.EmptyClipboard()

    pyautogui.moveTo(*x_y, 0.1)
    pyautogui.dragRel(-75, 0, 0.2, button='left')
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')

    rc = win32clipboard.EnumClipboardFormats(0)
    print('первый rc {}'.format(rc))
    while rc:
        try:
            format_name = win32clipboard.GetClipboardFormatName(rc)
        except win32clipboard.error:
            format_name = "?"
        print("format", rc, format_name)
        rc = win32clipboard.EnumClipboardFormats(rc)

    win32clipboard.CloseClipboard()

    win32clipboard.OpenClipboard()
    # win32clipboard.EmptyClipboard()

    # pyautogui.moveTo(*x_y, 0.1)
    # pyautogui.dragRel(-75, 0, 0.2, button='left')
    # pyautogui.keyDown('ctrl')
    # pyautogui.press('c')
    # pyautogui.keyUp('ctrl')

    # a = win32clipboard.GetClipboardFormatName(1)

    # print('Формат {}'.format(a))
    value = win32clipboard.GetClipboardData(13)

    win32clipboard.CloseClipboard()

    print('Метка пройдена')
    print(value)

    try:
        dollars, cents = value.split('.')
    except ValueError:
        dollars = value
        cents = None

    if not cents:
        res_value = int(str(dollars) + str('00'))
    else:
        res_value = int(str(dollars) + str(cents))

    return res_value


time.sleep(2)

put_cursor_and_get_from_input((500, 500))
d = pyautogui.locateOnScreen('pics/D.png', grayscale=True)
print('Координаты фишки дилера {}'.format(d))
