import copy
from combinations import results_count, separate_points, elder_card, pair
from functools import reduce
from random import randint
from chances import c

r = [147, int(1200/(1/1.28)), int(1200/(1/3.26)), int(1200/(1/19.7)), int(1200/(1/20.6)),
     int(1200/(1/32.1)), int(1200/(1/37.5)), int(1200/(1/594)), int(1200/(1/3589.6))]

map_of_c = [('Пики', '10'), ('Пики', 'J'), ('Пики', 'Q'), ('Пики', 'K'), ('Пики', 'A')]
map_of_s = [('Черви_', 0), ('Трефы_', 0), ('Буби_', 0), ('Пики_', 5)]
map_of_v = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
map_of_v0 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 4]
map_of_v1 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 3]
map_of_v2 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 3]
map_of_v3 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2]
map_of_v4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2]


def divide(a, b):
    try:
        res = a / b
    except ZeroDivisionError:
        res = 1
    return res


def indexate(points, in_list_of_points):
    res = 0

    for ind, p in enumerate(in_list_of_points):
        if points >= p:
            res = ind

    return res


def det_max_res():
    max_e, _, _, _, max_strt, max_f, _, _, max_fs = results_count(map_of_s, map_of_c, map_of_v, False)
    _, _, _, _, _, _, _, max_k, _ = results_count(map_of_s, map_of_c, map_of_v0, False)
    _, _, _, _, _, _, max_fh, _, _ = results_count(map_of_s, map_of_c, map_of_v1, False)
    _, _, _,max_set, _, _, _, _, _ = results_count(map_of_s, map_of_c, map_of_v2, False)
    _, _, max_tp, _, _, _, _, _, _ = results_count(map_of_s, map_of_c, map_of_v3, False)
    _, max_p, _, _, _, _, _, _, _ = results_count(map_of_s, map_of_c, map_of_v4, False)

    return max_e, max_p, max_tp, max_set, max_strt, max_f, max_fh, max_k, max_fs


def create_model(map_of_values):
    model = copy.copy(map_of_values)
    for i, amount in enumerate(model):
        if amount != 0:
            model[i] = 1

    i_1 = model.index(1, 0, 14)
    try:
        i_2 = model.index(1, i_1 + 1, 14)
    except ValueError:
        i_2 = 100
    try:
        i_3 = model.index(1, i_2 + 1, 14)
    except ValueError:
        i_3 = 200
    try:
        i_4 = model.index(1, i_3 + 1, 14)
    except ValueError:
        i_4 = 300
    try:
        i_5 = model.index(1, i_4 + 1, 14)
    except ValueError:
        i_5 = 400
    try:
        i_6 = model.index(1, i_5 + 1, 14)
    except ValueError:
        i_6 = 500
    try:
        i_7 = model.index(1, i_6 + 1, 14)
    except ValueError:
        i_7 = 500

        return i_1, i_2, i_3, i_4, i_5, i_6, i_7


def basic_decision(op_virt_points, player_virt_points_base, op_points, player_points, max_combos=None, values=None):
    def chance_of_win_if_p_got():
        s = copy.copy(values['map_of_player'])
        print('это s {} {}'.format(s, values['map_of_player']))
        ind_1 = s.index(1)
        s[ind_1] = 2
        w1 = pair(s)
        s[ind_1] = 1
        ind_2 = s.index(1, ind_1 + 1)
        s[ind_2] = 2
        w2 = pair(s)
        s[ind_2] = 1
        cha = ((w1 + w2)/2 - r[1])/(max_p - r[1])

        return cha

    player_virt_points = copy.copy(player_virt_points_base[0:9])

    maximus = det_max_res()

    maximus = list(maximus)

    flash_royal = maximus[8]
    supa_pupa_strt = maximus[4]

    if max_combos:
        # print('Вычислены возможные комбинации')
        maximus = list(max_combos)

    max_e, max_p, max_tp, max_set, max_strt, max_f, max_fh, max_k, max_fs = maximus

    try:
        ko = max(max_strt) / supa_pupa_strt
    except TypeError:
        ko = max_strt / supa_pupa_strt
    except ValueError:
        ko = 1

    maximus[8] = flash_royal * ko

    oreshek = player_points.index(max(player_points))
    op_chance_oreshek = op_virt_points[oreshek] / r[oreshek]
    op_multiplier = 1

    if max(op_points) >= r[oreshek]:
        op_chance_oreshek = 1
        op_multiplier = values['op_count']

    if values['round'] == 0 and oreshek == 0:
        op_multiplier = 1

    print('Это op_chance_oreshek {}, а это орешек {}'.format(op_chance_oreshek, oreshek))

    local_p_points = max(player_points) - r[oreshek]

    try:
        local_max_points = max(maximus[oreshek]) - r[oreshek]
    except TypeError:
        local_max_points = maximus[oreshek] - r[oreshek]

    try:
        local_p_win_chance_on_mp = local_p_points / local_max_points
    except ZeroDivisionError:
        local_p_win_chance_on_mp = 1

    if oreshek != 1 and oreshek != 5 and oreshek != 8 and max_combos:

        local_p_points = sorted(maximus[oreshek])

        local_p_ind = indexate(max(player_points), local_p_points)

        local_p_win_chance_on_mp = (local_p_ind + 1) / len(local_p_points)

    elif oreshek == 1:

        if values['op_map_of_values'].count(2) > 0:
            local_p_win_chance_on_mp = elder_card(values['map_of_player'])[0]/elder_card([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])[0]

        else:
            if values['round'] > 0:
                local_p_ind = values['map_of_values'].index(2)
                local_p_win_chance_on_mp = 1
                change = 0

                while local_p_ind < 13:
                    if values['op_map_of_values'][local_p_ind] == 0:
                        change = c(values['pool_map_of_values'][local_p_ind], 2) / c(len(values['pool_from_ppv']), 2)
                    elif values['op_map_of_values'][local_p_ind] == 1:
                        change = c(values['pool_map_of_values'][local_p_ind], 1) * c(len(values['pool_from_ppv'])-1, 1) / c(len(values['pool_from_ppv']), 2)
                    local_p_win_chance_on_mp -= change
                    local_p_ind += 1
            else:
                local_p_ind = values['map_of_values'].index(2)
                local_p_win_chance_on_mp = (local_p_ind + 1) / 13

    # print('мультиплайер {}'.format(op_multiplier))
    local_p_win_chance_on_mp **= op_multiplier

    local_lose_chance_on_mp = (1-local_p_win_chance_on_mp) * op_chance_oreshek

    if local_lose_chance_on_mp < 0:
        print('Локальный шанс проигрыша меньше 0, этого быть не должно')

    other_p_lose_chance = list(map(lambda x, y: x/y, op_virt_points, r))

    print('\nЛокальный шанс победы {}\n'.format(local_p_win_chance_on_mp))
    # print('\nПрочий шанс проигрыша {}\n'.format(other_p_lose_chance))
    # print('\nВиртуальные очки ИИ {}\n'.format(player_virt_points))
    # print('\nТекущие очки ИИ {}\n'.format(player_points))
    # print('\nВиртуальные очки оппонента {}\n'.format(op_virt_points))
    # print('\nТекущие очки оппонента {}\n'.format(op_points))
    # print('\nБазовые очки комбинации {}\n'.format(r))

    other_p_win_chance = list(map(lambda x, y: x / y, player_virt_points, r))

    print(other_p_win_chance)

    other_p_win_chance = other_p_win_chance[oreshek+1:]

    print(player_virt_points)
    print(r)
    print('\nПрочий шанс шанс победы {}\n'.format(other_p_win_chance))

    # try:
    #     other_p_win_chance = reduce(lambda x, y: x + y, other_p_win_chance)
    # except TypeError:
    #     other_p_win_chance = 0

    other_p_lose_chance = other_p_lose_chance[oreshek+1:]

    print('\nПрочий шанс шанс проигрыша ЭТАП 1 {}\n'.format(other_p_lose_chance))

    # print('\nШансы выпадения ПОБЕДНОЙ комбинации у оппонента-человека {}\n'.format(other_p_lose_chance))

    # try:
    for i, chance in enumerate(other_p_lose_chance):
        if len(other_p_win_chance[i+1:]) > 0:
            if oreshek == 0:
                if i == 0:
                    ch = chance_of_win_if_p_got()
                    print('это шанс победы при выпадении пары ch - {}'.format(ch))
                    other_p_lose_chance[i] = \
                        chance * (1 - ch * other_p_win_chance[i] * other_p_lose_chance[i] -
                                  reduce(lambda x, y: x + y, other_p_win_chance[i + 1:]))
                else:
                    other_p_lose_chance[i] = chance * (1 - reduce(lambda x, y: x + y, other_p_win_chance[i + 1:]))
            else:
                other_p_lose_chance[i] = chance * (1 - reduce(lambda x, y: x + y, other_p_win_chance[i+1:]))
        else:
            pass

    print('Прочий шанс проигрыша ЭТАП 2 {}'.format(other_p_lose_chance))

    try:
        other_p_lose_chance = reduce(lambda x, y: x + y, other_p_lose_chance)
    except TypeError:
        other_p_lose_chance = 0

    print('Прочий шанс проигрыша ЭТАП 3 {}'.format(other_p_lose_chance))

    # print('\nСовокупный Шанс выпадения ПОБЕДНОЙ комбинации у оппонента-человека {}\n'.format(other_p_lose_chance))
    # except TypeError:
    #     other_p_lose_chance = 0

    if values['round'] == 0:
        other_p_win_chance = 0

    general_p_lose_chance = local_lose_chance_on_mp*(1-other_p_lose_chance) + other_p_lose_chance
    print(general_p_lose_chance)

    # print('\nЛокальный шанс выпадения победной комбинации у оппонента-человека {}\n'.format(local_lose_chance_on_mp))

    if max(player_points) > max(op_points):

        if max(separate_points(player_points)) == max(separate_points(op_points)):

            print('\nПроизошел случай, когда при наличии комбинации игрок лидирует по старшей карте\n')

            # print('\nШанс проигрыша игрока до уточнения {}\n'.format(general_p_lose_chance))

            general_p_lose_chance += 1 - (player_points[0] - r[0]) / (max(maximus[0]) - r[0])

            # print('\nШанс проигрыша игрока после уточнения {}\n'.format(general_p_lose_chance))

        general_win_chance = 1 - general_p_lose_chance

        if general_win_chance < 0:
            general_win_chance = 0

        print('\nСовокупный Шанс ПОБЕДЫ Искусства 1 - x {}\n'.format(general_win_chance))
    else:

        # print('\nШансы выпадения ПОБЕДНОЙ комбинации у Искусства {}\n'.format(other_p_win_chance))

        try:
            general_win_chance = reduce(lambda x, y: x + y, other_p_win_chance)
        except TypeError:
            general_win_chance = 1 - (2 / 45) * values['op_count']

        if general_win_chance == 0 and general_p_lose_chance == 0:
            general_win_chance = 1

        # print('\n Cовокупный Шанс выпадения ПОБЕДНОЙ комбинации у Искусства {}\n'.format(general_win_chance))

    return general_win_chance, local_p_win_chance_on_mp


def player_makes_bet(participants, opponent_bets, limit=0):

    def find_strongest_op_bank():

        max_bank = 0

        mem_with_max_bank = 0

        for i in participants:
            if i.bet != 0:
                if max_bank < (i.bet + i.bank):
                    max_bank = i.bet + i.bank
                    mem_with_max_bank = i

        min_bank = max_bank

        for i in participants:
            if i.bet != 0:
                if (min_bank > (i.bet + i.bank)) and (i.bet + i.bank) > 0:
                    min_bank = i.bet + i.bank

        # print('Максимальный банк {}'.format(max_bank))
        # print('Минимальный банк {}'.format(min_bank))

        return max_bank, min_bank, mem_with_max_bank

    def get_blef():

        blef_coefs = []

        for ind, member in enumerate(participants):
            if ind != 0:
                if member.bet == max(opponent_bets):
                    blef_coefs.append(member.blef_rank)

        return min(blef_coefs)

    def make_blef(p_rise, border_of_made_bet=0.2):

        print('\n\n make blef.decision строка 247\n\n')

        if 0.6 > player_win_chance > 0.2 and divide(player_bet, player_bank) > border_of_made_bet and members_in_game < 3 and (memb_in_game_after_p < 1):

            if randint(0, 3) == 0:
                print('Сработал блеф в make_blef')
                p_rise = strongest_op_bank_in_game - player_bet

                if p_rise > player_bank - player_bet:
                    p_rise = player_bank - player_bet

        return p_rise

    def react_on_blef(rise_to_correct, border):

        print('\n\n React on blef.decision строка 247\n\n')

        if player_max_bet == player_bank:
            pass

        else:

            if player_win_chance < border:

                if player_bet / player_bank > 0.5 and player_win_chance > 0.6:
                    print('стр.373 react on blef')
                    rise_to_correct = max(opponent_bets) - player_bet
                    if rise_to_correct > player_bank - player_bet:
                        rise_to_correct = player_bank - player_bet
                # снизить до 0.71
                elif player_bet / player_bank > 0.35 and player_win_chance > 0.72:
                    print('стр.206 react on blef')
                    rise_to_correct = max(opponent_bets) - player_bet
                    if rise_to_correct > player_bank - player_bet:
                        rise_to_correct = player_bank - player_bet

                elif player_bet / player_bank > 0.25 and player_win_chance > 0.77:
                    print('стр.196 react on blef')
                    rise_to_correct = max(opponent_bets) - player_bet
                    if rise_to_correct > player_bank - player_bet:
                        rise_to_correct = player_bank - player_bet

                elif player_bet / player_bank > 0.15 and player_win_chance > 0.82:
                    print('стр.196 react on blef')
                    rise_to_correct = max(opponent_bets) - player_bet
                    if rise_to_correct > player_bank - player_bet:
                        rise_to_correct = player_bank - player_bet

                elif 0 < bet / limit < 0.06 and local_player_chance > 0.5:
                    if randint(1, (2 + memb_in_game_after_p)) == 2:
                        print('\n\nВажно! Сработал blef! cтр. 275 react on blef\n\n')
                        rise_to_correct = bet + player_bet
                else:

                    rise_to_correct = 0

            else:

                print('\n\nКоэффициент блефа {}\n\n'.format(get_blef()))

                rise_to_correct *= get_blef()

                if rise_to_correct >= (player_bank - player_bet):

                    rise_to_correct = (player_bank - player_bet)

                    print('скрипт 64580990984')

                else:

                    if rise_to_correct + player_bet < bet:

                        if player_bet / player_bank > 0.15:

                            rise_to_correct = bet - player_bet

                            print('скрипт 64580840984')

                            if rise_to_correct > player_bank - player_bet:

                                rise_to_correct = player_bank - player_bet

                        else:

                            rise_to_correct = 0

                    elif rise_to_correct + player_bet > bet:

                        if (rise_to_correct + player_bet) / bet < 2:

                            rise_to_correct = bet - player_bet

        return rise_to_correct

    def take_pos_into_consider(rise):
        if memb_in_game_after_p > 0:
            if rise == (player_bank - player_bet) or rise == (strongest_op_bank_in_game - player_bet):
                print('take_pos пассуем')
                pass
            else:
                print('\nrise до take pos into consider {}\n'.format(rise))
                # print('rise до take_pos {}, membs_in_game {}, bet {}'.format(rise, memb_in_game_after_p, bet))
                rise /= (memb_in_game_after_p * memb_in_game_after_p) / 10 + 1

                rise = int(rise // bet) * bet + int(2 * (rise % bet) / bet) * bet

                print('\nrise после take pos into consider {}\n'.format(rise))
                try:
                    if rise / needed < 1.5:
                        rise = needed
                except ZeroDivisionError:
                    pass

                if rise < needed:
                    rise = needed

        return rise

    def actualize_bet(rise_to_correct, needed):
        potential_lose_value = player_max_bet / player_bank
        risk_border = 0.85
        print(f'potencial_lose_val {potential_lose_value}')

        def bet_operation(rise, react_on_blef_border=0.85):
            if needed > 0:
                if coefficient > 5:
                    if raund != 3:
                        rise = bet * (1 + int(player_win_chance / risk_border)) + \
                               needed * 2
                        if randint(1, 6) == 2 and memb_in_game_after_p > 0:
                            print('сработало выжидание при хорошем шансе')
                            rise = needed
                    else:
                        rise = bet * (1 + int(player_win_chance / risk_border)) + \
                               needed * 2

                    rise = take_pos_into_consider(rise)

                elif coefficient > 3:
                    if potential_lose_value > 0.22:
                        rise = bet * int(player_win_chance / risk_border) + \
                               needed * (1 + int(player_win_chance / risk_border))

                    else:
                        rise = bet + needed * 2

                    #     # elif randint(1, 6) == 2:
                    #     #     if divide(player_bet, player_bank) > 0.2 and members_in_game < 3 and \
                    #     #             (memb_in_game_after_p < 1):
                    #     #
                    #     #         if 0.3 < bet / weakest_op_bank_in_game < 0.4 and bet / player_bank < 0.2:
                    #     #             rise = strongest_op_bank_in_game - player_bet
                    #     #             print('сработал скрипт 65748754875')
                    #     #
                    #     #             if rise > player_bank - player_bet:
                    #     #                 rise = player_bank - player_bet
                    # else:
                    #     rise = bet + needed * 2

                    rise = take_pos_into_consider(rise)

                elif coefficient > 2:
                    if potential_lose_value > 0.15:
                        rise = bet * int(player_win_chance / risk_border) + \
                               needed * (1 + int(player_win_chance / risk_border))

                    else:
                        rise = bet * randint(0, 1) + needed * randint(1, 2)

                    rise = take_pos_into_consider(rise)

                elif coefficient > 1:
                    rise = needed

                # обработка блефа со стороны оппонента

                elif coefficient < 1:

                    rise = react_on_blef(rise, react_on_blef_border)

            else:
                if coefficient > 5:
                    if potential_lose_value > 0.3:
                        print('\nРешение о ставке 00021\n')
                        rise = int(bet * (int(player_win_chance / risk_border)*1.5 + 1.5))
                        if randint(1, 5) == 2 and raund != 3:
                            print('сработало выжидание при хорошем шансе')
                            rise = needed
                    else:
                        rise = bet * 2
                        print('\nРешение о ставке 00020\n')

                    rise = take_pos_into_consider(rise)

                    if wait_for_open and rise > bet:
                        rise = bet

                elif coefficient > 4:
                    if potential_lose_value > 0.3:
                        print('\nРешение о ставке 00021\n')
                        rise = int(bet * (int(player_win_chance / risk_border)*1.25 + 1))
                        if randint(1, 5) == 2 and raund != 3:
                            print('сработало выжидание при хорошем шансе')
                            rise = needed
                    else:
                        rise = int(bet * 1.5)
                        print('\nРешение о ставке 00020\n')

                    rise = take_pos_into_consider(rise)

                    if wait_for_open and rise > bet:
                        rise = bet

                elif coefficient > 3:
                    if potential_lose_value > 0.3:
                        print('\nРешение о ставке 00021\n')
                        rise = int(bet * (int(player_win_chance / risk_border)*1.5 + 0.5))
                        if randint(1, 5) == 2 and raund != 3:
                            print('сработало выжидание при хорошем шансе')
                            rise = needed
                    else:
                        rise = bet
                        print('\nРешение о ставке 00020\n')

                    # if raund != 3:
                    #     rise = bet * randint(1, 2)
                    #     if randint(1, 3) == 2 and memb_in_game_after_p > 0:
                    #         print('сработало выжидание при хорошем шансе')
                    #         rise = needed
                    #
                    # else:
                    #     rise = bet * 2

                    rise = take_pos_into_consider(rise)

                    if wait_for_open and rise > bet:
                        rise = bet

                elif coefficient > 2:
                    rise = needed
                    if memb_in_game_after_p < 2 and bet / limit < 0.06:
                        rise = bet
                        print('\nРешение о ставке 00010\n')
                    else:
                        if potential_lose_value > 0.3:
                            rise = bet * int(player_win_chance / risk_border)
                        print('\nРешение о ставке 00011\n')

                elif coefficient > 1:
                    rise = needed
                    if randint(1, 2) == 2 and memb_in_game_after_p < 2 and bet / limit < 0.06:
                        rise = randint(2, 4) * small_blind
                        print('\nРешение о ставке 00020\n')
                    else:
                        if bet/player_bank > 0.8:
                            rise = int(bet / 2)

                else:
                    rise = needed
                    if player_bet / limit < 0.15 and participants[0].blef_rises == 0 and raund != 0:
                        rise = int(player_bet)
                        participants[0].blef_rises += 1
                        print(f'Сделали blef_rise, кол-во раз {participants[0].blef_rises}')
                        print('\nРешение о ставке 00031\n')

            return rise

        coefficient = (player_bet + rise_to_correct) / bet

        print('\nplayer_bet {}. rise_to_correct {}. bet {}\n'.format(player_bet, rise_to_correct, bet))
        print('\ncoefficient {}\n'.format(coefficient))
        # print('Место Искуственного Интелекта в очереди ставок {}'.format(place_in_queue))

        if raund == 3:

            rise_to_correct = bet_operation(rise_to_correct)

        elif raund == 2:

            rise_to_correct = bet_operation(rise_to_correct)

        elif raund == 1:

            rise_to_correct = bet_operation(rise_to_correct)

        elif raund == 0:

            rise_to_correct = bet_operation(rise_to_correct)

        # print('\n\nРезультирующая ставка в функции actualize_bet {}\n\n'.format(rise_to_correct))

        return int(rise_to_correct)

    # считаем от исходного банка
    player_bet = participants[0].bet
    player_bank = participants[0].bank + player_bet
    player_win_chance = participants[0].win_chance
    local_player_chance = participants[0].local_win_chance
    print('\n\nШАНС АИ {} !!!!!!!!!!!!!!!!!!!!\n\n'.format(player_win_chance))
    place_in_queue = participants[0].place_in_queue
    raund = participants[0].round
    limit = participants[0].limit
    bet = max(opponent_bets)
    small_blind = participants[0].small_blind

    wait_for_open = False

    memb_to_do_bet_after_p = (len(participants) - 1) - place_in_queue
    memb_in_game_after_p = memb_to_do_bet_after_p - opponent_bets[1:memb_to_do_bet_after_p + 1].count(0)

    # для повышения агрессии ИИ
    if raund == 0 and memb_in_game_after_p > 1:
        memb_in_game_after_p = 1
        print('decis/Искусственно учитываем только 1го противника после  ИИ, на самом деле их больше 1го')

    print('Игроки в игре после АИ {}'.format(memb_in_game_after_p))

    player_max_bet = 0

    members_in_game = len(opponent_bets) - opponent_bets.count(0)

    strongest_op_bank_in_game, weakest_op_bank_in_game, member_with_max_bank = find_strongest_op_bank()

    print('\nstrongest_op_bank_in_game {}, weakest_op_bank_in_game {}\n'.format(strongest_op_bank_in_game, weakest_op_bank_in_game))

    if player_win_chance >= 0.85:
        player_max_bet = player_bank

    elif player_win_chance > 0.8:
        player_max_bet = (player_win_chance ** (1 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.85:
            print('Коррекция из-за короткого стека 45761478689846')
            player_max_bet = player_bank

    elif player_win_chance > 0.75:
        player_max_bet = (player_win_chance ** (1.5 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.8:
            print('Коррекция из-за короткого стека 45761478689846')
            player_max_bet = player_bank
    # elif player_win_chance > 0.75:
    #     player_max_bet = (player_win_chance ** (2 + player_bank / limit - 1)) * player_bank
    #
    #     if player_bank / limit < 0.75:
    #         print('Коррекция из-за короткого стека 45761478689846')
    #         player_max_bet = player_bank

    elif player_win_chance > 0.70:
        player_max_bet = (player_win_chance ** (2.25 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.6:
            print('Коррекция из-за короткого стека 45763758993846')
            player_max_bet = player_bank
        # elif player_bank / limit > 1.5:
        #     print('Коррекция из-за увеличенного стека 5')
        #     player_max_bet = (player_win_chance ** 2) * player_bank

    elif player_win_chance > 0.65:
        player_max_bet = (player_win_chance ** (3 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.4:
            print('Коррекция из-за короткого стека 45763483553689846')
            player_max_bet = player_bank
        # elif player_bank / limit > 1.5:
        #     print('Коррекция из-за увеличенного стека 4')
        #     player_max_bet = (player_win_chance ** 2.5) * player_bank

    elif player_win_chance > 0.50:
        player_max_bet = (player_win_chance ** (3 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.2:
            print('Коррекция из-за короткого стека 45763484689846')
            player_max_bet = player_bank
        # elif player_bank / limit > 1.8:
        #     print('Коррекция из-за увеличенного стека 3')
        #     player_max_bet = (player_win_chance ** 3) * player_bank

    elif player_win_chance > 0.45:
        player_max_bet = (player_win_chance ** (3.5 - (player_win_chance - 0.45)*10 + player_bank / limit - 1)) * player_bank

        # if player_bank / limit > 1.8:
        #     print('Коррекция из-за увеличенного стека 2')
        #     player_max_bet = (player_win_chance ** 3.5) * player_bank

    elif player_win_chance > 0:
        player_max_bet = (player_win_chance ** (3.5 + player_bank / limit - 1)) * player_bank

        # if player_bank / limit > 1.8:
        #     print('Коррекция из-за увеличенного стека 1')
        #     player_max_bet = (player_win_chance ** 3.5) * player_bank

    if player_win_chance < 0.35:
        wait_for_open = True

    available = player_max_bet - 0.75 * player_bet
    needed = (max(opponent_bets) - player_bet)

    if available < 0:
        available = 0

    player_rise = available

    if player_rise < 0:
        player_rise = 0

    # print('\n\nСтавка до функции actualize_bet {}\n\n'.format(player_rise))

    player_rise = actualize_bet(player_rise, needed)

    print('ИИ сделал ставку {}'.format(player_rise))

    return player_rise, needed

# необходимо внести учет ставки ии в зависимости от уже имеющихся максимальных ставок, а то получается что при мак. ставке 20
# ии повышает на 400 ------> тестируется

# сделать при резком изменении шанса возможность блефа ---------> тестируется

# реакция на возможный блеф ------------> тестируется

# допилить игру на низких стеках, ниже 10BB

# допилить подсчет очков для two pairs, - должна учитываться только одна карта
