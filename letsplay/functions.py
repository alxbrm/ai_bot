import win32gui, win32process, win32clipboard, pyautogui, time, copy


def divide(a, b):
    try:
        res = a / b
    except ZeroDivisionError:
        res = 1
    return res


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


def num_mouse_click(list):
    for i in list:
        if int(i):
            x, y = pyautogui.locateCenterOnScreen('Plus.PNG')
            pyautogui.click(x=x, y=y, duration=0.5)
            x, y = pyautogui.locateCenterOnScreen(i+'.PNG')
            pyautogui.click(x=x, y=y, duration=0.5, tween=pyautogui.easeInBounce)
        else:
            break

    x, y = pyautogui.locateCenterOnScreen('Equal.PNG')
    pyautogui.click(x=x, y=y, duration=1)


def keyboard_click(list, Xpos, Ypos):
    pyautogui.moveTo(x=Xpos+5, y=Ypos+5, duration=1.5)
    pyautogui.click()

    for i in list:
        if int(i):
            pyautogui.hotkey(i, '+')
        else:
            pass

    pyautogui.press('=')


def capture_participants_banks(l):
    res = []
    for coords in l:
        t = (coords[0], coords[1] + coords[3], coords[2], coords[3])
        res.append(t)

    return res


def convert_max_bet_im_to_ints(coords):
    im = ['0_call', '1_call', '2_call', '3_call', '4_call', '5_call', '6_call', '7_call', '8_call', '9_call', 'dollar_call', 'dot_call']

    res = []

    there_is_dollar = False
    there_is_dot = False

    midlle_res = []

    for i, image in enumerate(im):
        if i < 10:
            try:
                r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=coords, grayscale=True))
                for rr in r:
                    rr = list(rr)
                    rr.append(i)
                    midlle_res.append(rr)
            except TypeError:
                r = [0, 0, 0, 0, 0]
                midlle_res.append(r)
        elif i == 10:
            if pyautogui.locateOnScreen('pics/' + image + '.png', region=coords, grayscale=True):
                there_is_dollar = True
        elif i == 11:
            if pyautogui.locateOnScreen('pics/' + image + '.png', region=coords, grayscale=True):
                there_is_dot = True

    pyautogui.screenshot('test.png', region=coords)

    midlle_res = sorted(midlle_res)

    template = ''

    for r in midlle_res:
        template += str(r[4])

    if there_is_dollar and not there_is_dot:
        template += str('00')

    try:
        template = int(template)
    except ValueError:
        template = 0

    res.append(template)

    return res


# учет ведется исключительно в центах
def convert_banks_im_to_ints(coords):
    im = ['0b', '1b', '2b', '3b', '4b', '5b', '6b', '7b', '8b', '9b', 'dollarb', 'dotb']

    res = []
    did_bets = []

    for n, coordinates in enumerate(coords):
        there_is_dollar = False
        there_is_dot = False

        midlle_res = []

        if n != 0 and pyautogui.locateOnScreen('pics/in_game_marker.png',
                                               region=(coordinates[0], coordinates[1] - coordinates[3]*2,
                                                       coordinates[2], coordinates[3]), grayscale=True):
            print('Сработал In_game_marker')

            did_bets.append(1)

            for i, image in enumerate(im):
                if i < 10:
                    r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=coordinates,
                                                         grayscale=True))
                    for rr in r:
                        rr = list(rr)
                        rr.append(i)
                        midlle_res.append(rr)
                elif i == 10:
                    if pyautogui.locateOnScreen('pics/' + image + '.png', region=coordinates, grayscale=True):
                        there_is_dollar = True
                elif i == 11:
                    if pyautogui.locateOnScreen('pics/' + image + '.png', region=coordinates, grayscale=True):
                        there_is_dot = True
        else:
            midlle_res.append([0, 0, 0, 0, 0])
            did_bets.append(0)

        midlle_res = sorted(midlle_res)

        template = ''

        for r in midlle_res:
            template += str(r[4])

        if there_is_dollar and not there_is_dot:
            template += str('00')

        try:
            template = int(template)
        except ValueError:
            template = 0

        res.append(template)

    return res, did_bets


def capture_participants_nicks(list_of_coordinates, participants):

    for i, amo in enumerate(list_of_coordinates):

        if i == 0:
            pass
            # pyautogui.screenshot('player.png', region=absolut)
        else:
            if not pyautogui.locateOnScreen('pics/in_game_marker.png',
                                            region=(amo[0], amo[1] - amo[3], amo[2], amo[3]), grayscale=True):
                pass
            else:
                print('Сработал In_game_marker в определении никс')
                if not pyautogui.locateOnScreen('opponent_' + str(i) + '.png', region=amo, grayscale=True):
                    pyautogui.screenshot('opponent_' + str(i) + '.png', region=amo)
                    participants[i].blef_rank = 0
                    participants[i].nick = 'Оппонент №' + str(i)
                    print('Вошел новый игрок взамен старого: {}'.format(participants[i].nick))
                else:
                    pass

    return


def capture_player_pos(base_point, game_num=0):
    d_1 = tuple(map(lambda x, y: x + y, (310, 326, 22, 22), base_point))
    d_2 = tuple(map(lambda x, y: x + y, (159, 197, 22, 22), base_point))
    d_3 = tuple(map(lambda x, y: x + y, (310, 121, 22, 22), base_point))
    d_4 = tuple(map(lambda x, y: x + y, (550, 121, 22, 22), base_point))
    d_5 = tuple(map(lambda x, y: x + y, (590, 197, 22, 22), base_point))
    d_6 = tuple(map(lambda x, y: x + y, (550, 326, 21, 21), base_point))

    p_pos = None

    if game_num == 3:
        d_perimetre = list(copy.copy(d_6))
        d_perimetre[2] /= 3
        d_perimetre[3] /= 3
        d_perimetre[0] += d_perimetre[2]
        d_perimetre[1] += d_perimetre[3]

        pyautogui.screenshot('pics/D.png', region=d_perimetre)

    if game_num > 3:
        d = pyautogui.locateOnScreen('pics/D.png', grayscale=True)
        print('Координаты фишки дилера {}'.format(d))
        if not d:
            time.sleep(0.3)
            d = pyautogui.locateOnScreen('pics/D.png', grayscale=True)
            print('Повторная попытка определить координаты {}, делаем скриншот...'.format(d))
            pyautogui.screenshot('screens/game_screen_' + str(game_num) + '.png', region=(base_point[0],
                                                                                          base_point[1], 900, 900))

        if d[0] - d_1[0] > 0 and d[1] - d_1[1] > 0 > d[0] + d[2] - d_1[0] - d_1[2] and d[1] + d[3] - d_1[1] - d_1[3] < 0:
            p_pos = 4
        elif d[0] - d_2[0] > 0 and d[1] - d_2[1] > 0 > d[0] + d[2] - d_2[0] - d_2[2] and d[1] + d[3] - d_2[1] - d_2[3] < 0:
            p_pos = 3
        elif d[0] - d_3[0] > 0 and d[1] - d_3[1] > 0 > d[0] + d[2] - d_3[0] - d_3[2] and d[1] + d[3] - d_3[1] - d_3[3] < 0:
            p_pos = 2
        elif d[0] - d_4[0] > 0 and d[1] - d_4[1] > 0 > d[0] + d[2] - d_4[0] - d_4[2] and d[1] + d[3] - d_4[1] - d_4[3] < 0:
            p_pos = 1
        elif d[0] - d_5[0] > 0 and d[1] - d_5[1] > 0 > d[0] + d[2] - d_5[0] - d_5[2] and d[1] + d[3] - d_5[1] - d_5[3] < 0:
            p_pos = 0
        elif d[0] - d_6[0] > 0 and d[1] - d_6[1] > 0 > d[0] + d[2] - d_6[0] - d_6[2] and d[1] + d[3] - d_6[1] - d_6[3] < 0:
            p_pos = 5
    else:
        # if game_num == 1:
        #     p_pos = 1
        # elif game_num == 2:
        #     p_pos = 0

        if pyautogui.locateOnScreen('pics/D_on_begin.png', region=d_1):
            p_pos = 4
        elif pyautogui.locateOnScreen('pics/D_on_begin.png', region=d_2):
            p_pos = 3
        elif pyautogui.locateOnScreen('pics/D_on_begin.png', region=d_3):
            p_pos = 2
        elif pyautogui.locateOnScreen('pics/D_on_begin.png', region=d_4):
            p_pos = 1
        elif pyautogui.locateOnScreen('pics/D_on_begin.png', region=d_5):
            p_pos = 0
        elif pyautogui.locateOnScreen('pics/D_on_begin.png', region=d_6):
            p_pos = 5

    return p_pos


def convert_player_c_into_cards(absolut_p_c_suit, absolut_p_c):
    im_1 = ['2_red', '2_black', '3_red', '3_black', '4_red', '4_black', '5_red', '5_black', '6_red', '6_black',
            '7_red', '7_black', '8_red', '8_black', '9_red', '9_black', '10_red', '10_black', 'J_red', 'J_black',
            'Q_red', 'Q_black', 'K_red', 'K_black', 'A_red', 'A_black']

    im_2 = ['Черви_', 'Пики_', 'Трефы_', 'Буби_']

    midlle_res_s = []

    for image in im_2:
        try:
            r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=absolut_p_c_suit, grayscale=True))
            for rr in r:
                rr = list(rr)
                rr.append(image)
                midlle_res_s.append(rr)
        except TypeError:
            pass

    midlle_res_c = []

    for image in im_1:
        try:
            r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=absolut_p_c, grayscale=True))
            i = image.split('_')[0]
            for rr in r:
                rr = list(rr)
                rr.append(i)
                midlle_res_c.append(rr)
        except TypeError:
            pass

    midlle_res_s = sorted(midlle_res_s)
    midlle_res_c = sorted(midlle_res_c)

    res = list(map(lambda x, y: x[4] + y[4], midlle_res_s, midlle_res_c))

    return res


def convert_river_into_cards(absolut_r_suit, absolut_river):
    im_1 = ['2_red', '2_black', '3_red', '3_black', '4_red', '4_black', '5_red', '5_black', '6_red', '6_black',
            '7_red', '7_black', '8_red', '8_black', '9_red', '9_black', '10_red', '10_black', 'J_red', 'J_black',
            'Q_red', 'Q_black', 'K_red', 'K_black', 'A_red', 'A_black']

    im_2 = ['Черви_', 'Пики_', 'Трефы_', 'Буби_']

    midlle_res_s = []

    for image in im_2:
        try:
            r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=absolut_r_suit, grayscale=True))
            for rr in r:
                rr = list(rr)
                rr.append(image)
                midlle_res_s.append(rr)
        except TypeError:
            pass

    midlle_res_c = []

    for image in im_1:
        try:
            r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=absolut_river, grayscale=True))
            i = image.split('_')[0]
            for rr in r:
                rr = list(rr)
                rr.append(i)
                midlle_res_c.append(rr)
        except TypeError:
            pass

    midlle_res_s = sorted(midlle_res_s)
    midlle_res_c = sorted(midlle_res_c)

    res = list(map(lambda x, y: x[4] + y[4], midlle_res_s, midlle_res_c))

    return res


def convert_turn_into_cards(absolut_t_suit, absolut_turn):
    im_1 = ['2_red', '2_black', '3_red', '3_black', '4_red', '4_black', '5_red', '5_black', '6_red', '6_black',
            '7_red', '7_black', '8_red', '8_black', '9_red', '9_black', '10_red', '10_black', 'J_red', 'J_black',
            'Q_red', 'Q_black', 'K_red', 'K_black', 'A_red', 'A_black']

    im_2 = ['Черви_', 'Пики_', 'Трефы_', 'Буби_']

    midlle_res_s = []

    for image in im_2:
        try:
            r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=absolut_t_suit, grayscale=True))
            for rr in r:
                rr = list(rr)
                rr.append(image)
                midlle_res_s.append(rr)
        except TypeError:
            pass

    midlle_res_c = []

    for image in im_1:
        try:
            r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=absolut_turn, grayscale=True))
            i = image.split('_')[0]
            for rr in r:
                rr = list(rr)
                rr.append(i)
                midlle_res_c.append(rr)
        except TypeError:
            pass

    midlle_res_s = sorted(midlle_res_s)
    midlle_res_c = sorted(midlle_res_c)

    res = list(map(lambda x, y: x[4] + y[4], midlle_res_s, midlle_res_c))

    return res


def convert_floop_into_cards(absolut_f_suit, absolut_floop):
    im_1 = ['2_red', '2_black', '3_red', '3_black', '4_red', '4_black', '5_red', '5_black', '6_red', '6_black',
            '7_red', '7_black', '8_red', '8_black', '9_red', '9_black', '10_red', '10_black', 'J_red', 'J_black',
            'Q_red', 'Q_black', 'K_red', 'K_black', 'A_red', 'A_black']

    im_2 = ['Черви_', 'Пики_', 'Трефы_', 'Буби_']

    midlle_res_s = []

    for image in im_2:
        try:
            r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=absolut_f_suit, grayscale=True))
            for rr in r:
                rr = list(rr)
                rr.append(image)
                midlle_res_s.append(rr)
        except TypeError:
            pass

    midlle_res_c = []

    for image in im_1:
        try:
            r = list(pyautogui.locateAllOnScreen('pics/' + image + '.png', region=absolut_floop, grayscale=True))
            i = image.split('_')[0]
            for rr in r:
                rr = list(rr)
                rr.append(i)
                midlle_res_c.append(rr)
        except TypeError:
            pass

    midlle_res_s = sorted(midlle_res_s)
    midlle_res_c = sorted(midlle_res_c)

    res = list(map(lambda x, y: x[4] + y[4], midlle_res_s, midlle_res_c))

    return res


# def capture_round(absolut_floop, absolut_turn, absolut_river):
#
#     if pyautogui.locateOnScreen('prefloop.png', region=absolut_floop, grayscale=True) or \
#             pyautogui.locateOnScreen('prefloop_v2.png', region=absolut_floop, grayscale=True):
#         rouund = 0
#     elif pyautogui.locateOnScreen('floop.png', region=absolut_turn, grayscale=True) or \
#             pyautogui.locateOnScreen('floop_v2.png', region=absolut_turn, grayscale=True):
#         rouund = 1
#     elif pyautogui.locateOnScreen('turn.png', region=absolut_river, grayscale=True) or \
#         pyautogui.locateOnScreen('turn_v2.png', region=absolut_river, grayscale=True):
#         rouund = 2
#     else:
#         rouund = 3
#
#     return rouund


def capture_round(absolut_common, rnd):

    if pyautogui.locateOnScreen('common_zone.png', region=absolut_common, grayscale=True):
        pass

    else:
        rnd += 1
        pyautogui.screenshot('common_zone.png', region=absolut_common)
        if rnd > 3:
            rnd = 3

    return rnd


def make_screenshot(game_num, basic_point):
    time.sleep(0)
    base_point = copy.copy(basic_point)
    base_point[2], base_point[3] = 1400, 1000

    pyautogui.screenshot('screens/game_screen_' + str(game_num) + '.png', region=base_point)

    # i = 0
    #
    # while True:
    #     time.sleep(sec)
    #     if pyautogui.locateOnScreen('pics/max_button.png', grayscale=True):
    #         pyautogui.screenshot('screens/game_screen_' + str(i) + '.png', region=base_point)
    #         i += 1
    #     else:
    #         pass


def push_max_button(abs_m_b):
    x, y = pyautogui.center(abs_m_b)
    pyautogui.moveTo(x, y, 0.2)
    pyautogui.click(button='left')
    time.sleep(0.2)


def put_cursor_and_get_from_input(x_y, game_num=0):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

    time.sleep(0.02)

    print(f'Двигаем мышку в {x_y}')
    pyautogui.moveTo(*x_y, 0.1)
    print(f'Выделяем {x_y}, реальная позиция {pyautogui.position()}')
    pyautogui.dragRel(-75, 0, 1, button='left')
    print(f'В конце выделения реальная позиция {pyautogui.position()}')
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')

    win32clipboard.OpenClipboard()

    value = win32clipboard.GetClipboardData(13)

    win32clipboard.CloseClipboard()

    print('Получено значение {}'.format(value))

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


def ai_make_bet(rise, made_rises, x_y):
    pyautogui.moveTo(*x_y, 0.1)
    pyautogui.dragRel(-75, 0, 0.1, button='left')

    print('RISING {}. SO WE...\n'.format(rise))

    if rise == 0:
        print('PRESS F6 CHECK')

        pyautogui.press('f6')

        time.sleep(0.2)

    else:
        print('rise {}'.format(rise))
        print('made_rise {}'.format(made_rises))
        input_rise = str(rise + made_rises)

        if len(input_rise) == 1:
            input_rise = '00' + input_rise
        elif len(input_rise) == 2:
            input_rise = '0' + input_rise

        print('input_rise {}'.format(input_rise))

        for i, amo in enumerate(input_rise):
            if len(input_rise) - i != 2:
                pyautogui.press(amo)
            else:
                pyautogui.press('.')
                pyautogui.press(amo)

        print('\n\nINPUT_RISING {}.\n\nPRESS F7\n\n'.format(input_rise))

        pyautogui.press('f7')

        time.sleep(0.2)


def adjust_basic_params():
    basic = {'base_point': 0, 'absolut_p_c': 0, 'absolut_p_c_suit': 0, 'absolut_floop': 0, 'absolut_turn': 0,
           'absolut_river': 0, 'absolut_f_suit': 0, 'absolut_t_suit': 0, 'absolut_r_suit': 0, 'absolut_call': 0,
           'absolut_fold': 0, 'is_call': 0, 'is_check': 0, 'abs_m_b': 0, 'absolut_bet_input': 0, 'absolut_nicks_coords': 0,
           'absolut_banks_coords': 0, 'absolut_bb_marker': 0, 'absolut_sb_marker': 0, 'absolut_common': 0,
             'relat_nick_coords': 0}

    player_coordinates = (420, 400, 130, 19)
    op1_coordinates = (190, 400, 130, 19)
    op2_coordinates = (2, 230, 130, 19)
    op3_coordinates = (190, 75, 130, 19)
    op4_coordinates = (420, 75, 130, 19)
    op5_coordinates = (625, 230, 130, 19)
    floop_coordinates = (255, 175, 156, 25)
    f_suit_coordinates = (251, 193, 160, 27)
    turn_coordinates = (415, 175, 30, 25)
    t_suits_coordinates = (410, 193, 35, 27)
    river_coordinates = (465, 175, 30, 25)
    r_suits_coordinates = (465, 193, 35, 27)
    common_zone_coordinates = (255, 175, 220, 25)
    sb_coords = (497, 317, 13, 33)
    bb_coords = (497, 317, 13, 33)

    player_cards_coordinates = (445, 350, 75, 26)
    p_suit_coordinates = (445, 368, 75, 27)

    basic['relat_nick_coords'] = [player_coordinates, op1_coordinates, op2_coordinates, op3_coordinates,
                                  op4_coordinates, op5_coordinates]

    basic['base_point'] = list(pyautogui.locateOnScreen('basic_point.png', grayscale=True))
    basic['base_point'][2], basic['base_point'][3] = 0, 0

    print(basic['base_point'])

    basic['absolut_p_c'] = tuple(map(lambda x, y: x + y, player_cards_coordinates, basic['base_point']))
    basic['absolut_p_c_suit'] = tuple(map(lambda x, y: x + y, p_suit_coordinates, basic['base_point']))

    basic['absolut_floop'] = tuple(map(lambda x, y: x + y, floop_coordinates, basic['base_point']))
    basic['absolut_turn'] = tuple(map(lambda x, y: x + y, turn_coordinates, basic['base_point']))
    basic['absolut_river'] = tuple(map(lambda x, y: x + y, river_coordinates, basic['base_point']))
    basic['absolut_f_suit'] = tuple(map(lambda x, y: x + y, f_suit_coordinates, basic['base_point']))
    basic['absolut_t_suit'] = tuple(map(lambda x, y: x + y, t_suits_coordinates, basic['base_point']))
    basic['absolut_r_suit'] = tuple(map(lambda x, y: x + y, r_suits_coordinates, basic['base_point']))
    basic['absolut_common'] = tuple(map(lambda x, y: x + y, common_zone_coordinates, basic['base_point']))

    basic['absolut_call'] = tuple(map(lambda x, y: x + y, (450, 481, 20, 14), basic['base_point']))
    basic['absolut_fold'] = tuple(map(lambda x, y: x + y, (284, 480, 21, 15), basic['base_point']))

    basic['is_call'] = tuple(map(lambda x, y: x + y, (339, 488, 54, 20), basic['base_point']))
    basic['is_check'] = tuple(map(lambda x, y: x + y, (370, 488, 54, 21), basic['base_point']))

    basic['absolut_bb_marker'] = tuple(map(lambda x, y: x + y, bb_coords, basic['base_point']))
    basic['absolut_sb_marker'] = tuple(map(lambda x, y: x + y, sb_coords, basic['base_point']))

    # basic['abs_m_b'] = tuple(map(lambda x, y: x + y, (506, 531, 43, 21), basic['base_point']))
    # basic['absolut_bet_input'] = (basic['abs_m_b'][0] + basic['abs_m_b'][2], basic['abs_m_b'][1] + basic['abs_m_b'][3])

    basic['absolut_nicks_coords'] = list(tuple(map(lambda i, y: i + y, i, basic['base_point']))
                                         for i in basic['relat_nick_coords'])

    print(basic['absolut_nicks_coords'])

    basic['absolut_banks_coords'] = capture_participants_banks(basic['absolut_nicks_coords'])

    print(basic['absolut_banks_coords'])

    return basic

# # Coruna NLH
# player_coordinates = (420, 400, 130, 19)
# op1_coordinates = (190, 400, 130, 19)
# op2_coordinates = (2, 230, 130, 19)
# op3_coordinates = (190, 75, 130, 19)
# op4_coordinates = (420, 75, 130, 19)
# op5_coordinates = (625, 230, 130, 19)
# floop_coordinates = (255, 182, 156, 18)
# f_suit_coordinates = (251, 200, 160, 20)
# turn_coordinates = (415, 182, 30, 18)
# t_suits_coordinates = (410, 200, 35, 20)
# river_coordinates = (470, 182, 30, 18)
# r_suits_coordinates = (465, 200, 35, 20)
#
# player_cards_coordinates = (445, 357, 75, 19)
# p_suit_coordinates = (445, 375, 75, 20)
#
#
# relatevly_coord_list = [player_coordinates, op1_coordinates, op2_coordinates, op3_coordinates, op4_coordinates, op5_coordinates]
#
# time.sleep(2)
#
# basic['base_point = list(pyautogui.locateOnScreen('basic_point.png'))
# basic['base_point[2], basic['base_point[3] = 0, 0
#
# print(basic['base_point)
#
# basic['absolut_p_c = tuple(map(lambda x, y: x + y, player_cards_coordinates, basic['base_point))
# basic['absolut_p_c_suit'] = tuple(map(lambda x, y: x + y, p_suit_coordinates, basic['base_point))
#
# basic['absolut_floop' = tuple(map(lambda x, y: x + y, floop_coordinates, basic['base_point))
# basic['absolut_turn' = tuple(map(lambda x, y: x + y, turn_coordinates, basic['base_point))
# basic['absolut_river']= tuple(map(lambda x, y: x + y, river_coordinates, basic['base_point))
# basic['absolut_f_suit = tuple(map(lambda x, y: x + y, f_suit_coordinates, basic['base_point))
# basic['absolut_t_suit = tuple(map(lambda x, y: x + y, t_suits_coordinates, basic['base_point))
# basic['absolut_r_suit = tuple(map(lambda x, y: x + y, r_suits_coordinates, basic['base_point))
#
# basic['absolut_call = tuple(map(lambda x, y: x + y, (450, 481, 17, 11), basic['base_point))
# basic['absolut_fold = tuple(map(lambda x, y: x + y, (284, 480, 18, 12), basic['base_point))
#
# basic['is_call = tuple(map(lambda x, y: x + y, (339, 495, 54, 13), basic['base_point))
# basic['is_check = tuple(map(lambda x, y: x + y, (370, 496, 40, 10), basic['base_point))
#
# basic['abs_m_b = tuple(map(lambda x, y: x + y, (506, 531, 43, 21), basic['base_point))
# basic['absolut_bet_input] = (basic['abs_m_b[0] + basic['abs_m_b[2], basic['abs_m_b[1] + basic['abs_m_b[3])
#
# basic['absolut_nicks_coords'] = capture_participants_nicks(relatevly_coord_list, participants=[])
# print(basic['absolut_nicks_coords'])
#
# basic['absolut_banks_coords = capture_participants_banks(basic['absolut_nicks_coords'])
# print(basic['absolut_banks_coords)
#
# pyautogui.screenshot('test.png', region=basic['is_call)

# time.sleep(2)
# basic = adjust_basic_params()
# print('Проверка обнаружения {}'.format(list(pyautogui.locateOnScreen('basic_point.png'))))
# print('Проверка обнаружения {}'.format(pyautogui.locateOnScreen('pics/sb_marker_1c.png', region=basic['absolut_bb_marker'])))


def interface(game, participants, basic, small_blind, limit):
    participants[0].limit = limit

    control_base_point = pyautogui.locateOnScreen('basic_point.png')

    print('Начало interface')

    if basic['base_point'][0] != control_base_point[0] or basic['base_point'][1] != control_base_point[1]:
        print('Обнаружено смещение окна!')
        basic = adjust_basic_params()

    if pyautogui.locateOnScreen('pics/f6.png', region=basic['absolut_call']):

        print('Начало interface.locateOnScreen')

        p_pos = capture_player_pos(basic['base_point'], game_num=game.game_num)

        print('Это p_pos {}'.format(p_pos))

        is_small_blind = pyautogui.locateOnScreen('pics/sb_marker_1c.png',
                                                  region=basic['absolut_bb_marker'], grayscale=True)
        if not is_small_blind:
            is_small_blind = pyautogui.locateOnScreen('pics/sb_marker_1c_v2.png',
                                                      region=basic['absolut_bb_marker'], grayscale=True)

        is_big_blind = pyautogui.locateOnScreen('pics/bb_marker_2c.png',
                                                region=basic['absolut_bb_marker'], grayscale=True)

        if not is_big_blind:
            is_big_blind = pyautogui.locateOnScreen('pics/bb_marker_2c_v2.png',
                                                    region=basic['absolut_bb_marker'], grayscale=True)

        p_cards = convert_player_c_into_cards(basic['absolut_p_c_suit'], basic['absolut_p_c'])
        pyautogui.screenshot('common_zone.png', region=basic['absolut_common'])
        game.handout(p_cards, p_pos)

        preflop_postflop = [[], [], [], []]

        iters = -1
        rnd = 0
        p_bet = 0
        p_bank = participants[0].bank
        made_rises_in_r = [0, 0, 0, 0]

        while True:
            if pyautogui.locateOnScreen('pics/f6.png', region=basic['absolut_call']):

                if p_pos != capture_player_pos(basic['base_point'], game_num=game.game_num+1):
                    break

                check_p_cards = convert_player_c_into_cards(basic['absolut_p_c_suit'], basic['absolut_p_c'])

                if p_cards != check_p_cards:
                    print('\n\n!!!НЕ УЗНАЛИ КАРТЫ!!!\n\n')
                    break

                make_screenshot(game.game_num, basic['base_point'])

                rnd = capture_round(basic['absolut_common'], rnd)

                iters += 1
                print('Раунд {}'.format(rnd))

                if not preflop_postflop[rnd] and rnd != 0:
                    if rnd == 1:
                        preflop_postflop[rnd] = convert_floop_into_cards(basic['absolut_f_suit'], basic['absolut_floop'])
                        print('Раунд {}, Вскрыты общие карты {}'.format(rnd, preflop_postflop[rnd]))
                    elif rnd == 2:
                        preflop_postflop[rnd] = convert_turn_into_cards(basic['absolut_t_suit'], basic['absolut_turn'])
                        print('Раунд {}, Вскрыты общие карты {}'.format(rnd, preflop_postflop[rnd]))
                    elif rnd == 3:
                        preflop_postflop[rnd] = convert_river_into_cards(basic['absolut_r_suit'], basic['absolut_river'])
                        print('Раунд {}, Вскрыты общие карты {}'.format(rnd, preflop_postflop[rnd]))

                abs_banks, bets = convert_banks_im_to_ints(basic['absolut_banks_coords'])
                print('Банки игроков {}'.format(abs_banks))

                there_is_max_button = pyautogui.locateOnScreen('pics/max_button.png', region=basic['abs_m_b'])

                if pyautogui.locateOnScreen('pics/check.png', region=basic['is_check']):
                    needed = 0
                    print('Никто не повысил ставки. Доступна кнопка Check')
                elif pyautogui.locateOnScreen('pics/call.png', region=basic['is_call']):
                    needed_coords = list(pyautogui.locateOnScreen('pics/call.png'))
                    needed_coords[0] += needed_coords[2]
                    needed_coords[2] += 20
                    needed = convert_max_bet_im_to_ints(needed_coords)[0]
                    if needed > p_bank:
                        p_bank = needed + small_blind * 2
                    print('Для Call необходимо {}'.format(needed))
                else:
                    print('От нас требуется ALL-INN. Наш текущий банк {}\n'.format(p_bank))
                    needed = p_bank

                if there_is_max_button:
                    print('basic_absolut_bet_input {}'.format(basic['absolut_bet_input']))
                    min_rising_bet = put_cursor_and_get_from_input(basic['absolut_bet_input'], game_num=game.game_num)
                    print('Минимальная общая повышающая ставка {}'.format(min_rising_bet))

                    push_max_button(basic['abs_m_b'])

                    p_bank = put_cursor_and_get_from_input(basic['absolut_bet_input'])
                else:
                    min_rising_bet = 0

                if is_small_blind and p_bet == 0 and rnd == 0:
                    print('\nАИ small blind в этой игре\n')
                    p_bet = small_blind
                    made_rises_in_r[rnd] += small_blind
                    p_bank -= p_bet
                elif is_big_blind and p_bet == 0 and rnd == 0:
                    print('\nАИ big blind в этой игре\n')
                    p_bet = small_blind * 2
                    made_rises_in_r[rnd] += small_blind * 2
                    p_bank -= p_bet

                op_bet = p_bet + needed
                bets = list(i*op_bet for i in bets)
                bets[0] = p_bet
                abs_banks[0] = p_bank

                if p_bank < limit * 0.50 and iters == 0:
                    print('Плохая игра, наш банк {}...'.format(participants[0].bank))
                    exit()
                elif participants[0].bank > limit * 2 and iters == 0:
                    print('Фиксируем прибыль, прерываем игру...')
                    exit()

                print('Уточненные банки игроков {}'.format(abs_banks))
                print('Текущие ставки {}, iters - {}'.format(bets, iters))

                p_rise = game.make_round(participants, rnd, bets, abs_banks, preflop_postflop[rnd])

                if needed <= p_rise < (min_rising_bet - made_rises_in_r[rnd]):
                    p_rise = needed
                    print('NEEDED <= P_RISE < MIN_ABLE_RISE. SO WE...\n\n PRESS f6 CALL'.format(p_rise, needed))
                    p_bank -= p_rise
                    p_bet += p_rise

                    pyautogui.press('f6')

                    time.sleep(0.2)
                    pass
                elif needed <= p_rise and (min_rising_bet - made_rises_in_r[rnd]) <= 0:
                    p_rise = needed
                    print('WE CANNOT RISE ANYMORE. SO WE...\n\n PRESS CALL f6'.format(p_rise, needed))
                    p_bank -= p_rise
                    p_bet += p_rise

                    pyautogui.press('f6')

                    time.sleep(0.2)
                    pass
                elif p_rise < needed:
                    print('ABLE RISING {}, NEEDED {}. SO WE...'.format(p_rise, needed))
                    print('\n\nPRESS F5 FOLD\n\n')

                    pyautogui.press('f5')

                    time.sleep(0.2)
                    pass

                else:

                    p_bank -= p_rise
                    p_bet += p_rise

                    ai_make_bet(p_rise, made_rises_in_r[rnd], basic['absolut_bet_input'])

                    made_rises_in_r[rnd] += p_rise
