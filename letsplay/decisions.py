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
        maximus = list(max_combos)

    max_e, max_p, max_tp, max_set, max_strt, max_f, max_fh, max_k, max_fs = maximus

    try:
        ko = max(max_strt) / supa_pupa_strt
    except TypeError:
        ko = max_strt / supa_pupa_strt
    except ValueError:
        ko = 1

    maximus[8] = flash_royal * ko

    hand_lvl = player_points.index(max(player_points))
    op_chance_hand_lvl = op_virt_points[hand_lvl] / r[hand_lvl]
    op_multiplier = 1

    if max(op_points) >= r[hand_lvl]:
        op_chance_hand_lvl = 1
        op_multiplier = values['op_count']

    # if values['round'] == 0 and hand_lvl == 0:
    #     op_multiplier = 1

    local_p_points = max(player_points) - r[hand_lvl]

    try:
        local_max_points = max(maximus[hand_lvl]) - r[hand_lvl]
    except TypeError:
        local_max_points = maximus[hand_lvl] - r[hand_lvl]

    try:
        local_p_win_chance_on_mp = local_p_points / local_max_points
    except ZeroDivisionError:
        local_p_win_chance_on_mp = 1

    if hand_lvl != 1 and hand_lvl != 5 and hand_lvl != 8 and max_combos:

        local_p_points = sorted(maximus[hand_lvl])

        local_p_ind = indexate(max(player_points), local_p_points)

        local_p_win_chance_on_mp = (local_p_ind + 1) / len(local_p_points)

    elif hand_lvl == 1:

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


    local_p_win_chance_on_mp **= op_multiplier
    local_lose_chance_on_mp = (1-local_p_win_chance_on_mp) * op_chance_hand_lvl
    other_p_lose_chance = list(map(lambda x, y: x/y, op_virt_points, r))
    other_p_win_chance = list(map(lambda x, y: x / y, player_virt_points, r))
    other_p_win_chance = other_p_win_chance[hand_lvl+1:]
    other_p_lose_chance = other_p_lose_chance[hand_lvl+1:]

    for i, chance in enumerate(other_p_lose_chance):
        if len(other_p_win_chance[i+1:]) > 0:
            if hand_lvl == 0:
                if i == 0:
                    ch = chance_of_win_if_p_got()
                    other_p_lose_chance[i] = \
                        chance * (1 - ch * other_p_win_chance[i] * other_p_lose_chance[i] -
                                  reduce(lambda x, y: x + y, other_p_win_chance[i + 1:]))
                else:
                    other_p_lose_chance[i] = chance * (1 - reduce(lambda x, y: x + y, other_p_win_chance[i + 1:]))
            else:
                other_p_lose_chance[i] = chance * (1 - reduce(lambda x, y: x + y, other_p_win_chance[i+1:]))
        else:
            pass

    try:
        other_p_lose_chance = reduce(lambda x, y: x + y, other_p_lose_chance)
    except TypeError:
        other_p_lose_chance = 0

    if values['round'] == 0:
        other_p_win_chance = 0

    general_p_lose_chance = local_lose_chance_on_mp * (1-other_p_lose_chance) + other_p_lose_chance

    if max(player_points) > max(op_points):

        if max(separate_points(player_points)) == max(separate_points(op_points)):
            general_p_lose_chance += 1 - (player_points[0] - r[0]) / (max(maximus[0]) - r[0])

        general_win_chance = 1 - general_p_lose_chance

        if general_win_chance < 0:
            general_win_chance = 0

    else:

        try:
            general_win_chance = reduce(lambda x, y: x + y, other_p_win_chance)
        except TypeError:
            general_win_chance = 1 - (2 / 45) * values['op_count']

        if general_win_chance == 0 and general_p_lose_chance == 0:
            general_win_chance = 1

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

        return max_bank, min_bank, mem_with_max_bank

    def get_blef():

        blef_coefs = []

        for ind, member in enumerate(participants):
            if ind != 0:
                if member.bet == max(opponent_bets):
                    blef_coefs.append(member.blef_rank)

        return min(blef_coefs)

    def react_on_blef(rise_to_correct, border):

        if player_max_bet == player_bank:
            pass

        else:

            if player_win_chance < border:

                if player_bet / player_bank > 0.5 and player_win_chance > 0.6:
                    rise_to_correct = max(opponent_bets) - player_bet
                    if rise_to_correct > player_bank - player_bet:
                        rise_to_correct = player_bank - player_bet

                elif player_bet / player_bank > 0.35 and player_win_chance > 0.72:
                    rise_to_correct = max(opponent_bets) - player_bet
                    if rise_to_correct > player_bank - player_bet:
                        rise_to_correct = player_bank - player_bet

                elif player_bet / player_bank > 0.25 and player_win_chance > 0.77:
                    rise_to_correct = max(opponent_bets) - player_bet
                    if rise_to_correct > player_bank - player_bet:
                        rise_to_correct = player_bank - player_bet

                elif player_bet / player_bank > 0.15 and player_win_chance > 0.82:
                    rise_to_correct = max(opponent_bets) - player_bet
                    if rise_to_correct > player_bank - player_bet:
                        rise_to_correct = player_bank - player_bet

                elif 0 < bet / limit < 0.06 and local_player_chance > 0.5:
                    if randint(1, (2 + memb_in_game_after_p)) == 2:
                        rise_to_correct = bet + player_bet
                else:

                    rise_to_correct = 0

            else:

                rise_to_correct *= get_blef()

                if rise_to_correct >= (player_bank - player_bet):

                    rise_to_correct = (player_bank - player_bet)

                else:

                    if rise_to_correct + player_bet < bet:

                        if player_bet / player_bank > 0.15:

                            rise_to_correct = bet - player_bet

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
                pass
            else:
                rise /= (memb_in_game_after_p * memb_in_game_after_p) / 10 + 1
                rise = int(rise // bet) * bet + int(2 * (rise % bet) / bet) * bet

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

        def bet_operation(rise, react_on_blef_border=0.85):
            if needed > 0:
                if coefficient > 5:
                    if raund != 3:
                        rise = bet * (1 + int(player_win_chance / risk_border)) + \
                               needed * 2
                        if randint(1, 6) == 2 and memb_in_game_after_p > 0:
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

                elif coefficient < 1:

                    rise = react_on_blef(rise, react_on_blef_border)

            else:
                if coefficient > 5:
                    if potential_lose_value > 0.3:
                        rise = int(bet * (int(player_win_chance / risk_border)*1.5 + 1.5))
                        if randint(1, 5) == 2 and raund != 3:
                            rise = needed
                    else:
                        rise = bet * 2

                    rise = take_pos_into_consider(rise)

                    if wait_for_open and rise > bet:
                        rise = bet

                elif coefficient > 4:
                    if potential_lose_value > 0.3:
                        rise = int(bet * (int(player_win_chance / risk_border)*1.25 + 1))
                        if randint(1, 5) == 2 and raund != 3:
                            rise = needed
                    else:
                        rise = int(bet * 1.5)

                    rise = take_pos_into_consider(rise)

                    if wait_for_open and rise > bet:
                        rise = bet

                elif coefficient > 3:
                    if potential_lose_value > 0.3:
                        rise = int(bet * (int(player_win_chance / risk_border)*1.5 + 0.5))
                        if randint(1, 5) == 2 and raund != 3:
                            rise = needed
                    else:
                        rise = bet

                    rise = take_pos_into_consider(rise)

                    if wait_for_open and rise > bet:
                        rise = bet

                elif coefficient > 2:
                    rise = needed
                    if memb_in_game_after_p < 2 and bet / limit < 0.06:
                        rise = bet
                    else:
                        if potential_lose_value > 0.3:
                            rise = bet * int(player_win_chance / risk_border)

                elif coefficient > 1:
                    rise = needed
                    if randint(1, 2) == 2 and memb_in_game_after_p < 2 and bet / limit < 0.06:
                        rise = randint(2, 4) * small_blind
                    else:
                        if bet/player_bank > 0.8:
                            rise = int(bet / 2)

                else:
                    rise = needed
                    if player_bet / limit < 0.15 and participants[0].blef_rises == 0 and raund != 0:
                        rise = int(player_bet)
                        participants[0].blef_rises += 1

            return rise

        coefficient = (player_bet + rise_to_correct) / bet

        if raund == 3:

            rise_to_correct = bet_operation(rise_to_correct)

        elif raund == 2:

            rise_to_correct = bet_operation(rise_to_correct)

        elif raund == 1:

            rise_to_correct = bet_operation(rise_to_correct)

        elif raund == 0:

            rise_to_correct = bet_operation(rise_to_correct)

        return int(rise_to_correct)

    # считаем от исходного банка
    player_bet = participants[0].bet
    player_bank = participants[0].bank + player_bet
    player_win_chance = participants[0].win_chance
    local_player_chance = participants[0].local_win_chance
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

    player_max_bet = 0

    strongest_op_bank_in_game, weakest_op_bank_in_game, member_with_max_bank = find_strongest_op_bank()

    if player_win_chance >= 0.85:
        player_max_bet = player_bank

    elif player_win_chance > 0.8:
        player_max_bet = (player_win_chance ** (1 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.85:
            player_max_bet = player_bank

    elif player_win_chance > 0.75:
        player_max_bet = (player_win_chance ** (1.5 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.8:
            player_max_bet = player_bank

    elif player_win_chance > 0.70:
        player_max_bet = (player_win_chance ** (2.25 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.6:
            player_max_bet = player_bank

    elif player_win_chance > 0.65:
        player_max_bet = (player_win_chance ** (3 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.4:
            player_max_bet = player_bank

    elif player_win_chance > 0.50:
        player_max_bet = (player_win_chance ** (3 + player_bank / limit - 1)) * player_bank

        if player_bank / limit < 0.2:
            player_max_bet = player_bank

    elif player_win_chance > 0.45:
        player_max_bet = (player_win_chance ** (3.5 - (player_win_chance - 0.45)*10 + player_bank / limit - 1)) * player_bank

    elif player_win_chance > 0:
        player_max_bet = (player_win_chance ** (3.5 + player_bank / limit - 1)) * player_bank

    if player_win_chance < 0.35:
        wait_for_open = True

    available = player_max_bet - 0.75 * player_bet
    needed = (max(opponent_bets) - player_bet)

    if available < 0:
        available = 0

    player_rise = available

    if player_rise < 0:
        player_rise = 0

    player_rise = actualize_bet(player_rise, needed)

    # print('ИИ сделал ставку {}'.format(player_rise))

    return player_rise, needed
