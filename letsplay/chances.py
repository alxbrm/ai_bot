from math import factorial
from functools import reduce
import copy, pyautogui, time
from random import randint


rangs = {'ElderCard': 147, 'Pair': 1200/(1/1.28), 'TwoPairs': 1200/(1/3.26), 'Set': 1200/(1/19.7),
         'Street': 1200/(1/20.6), 'Flash': 1200/(1/32.1), 'FullHouse': 1200/(1/37.5), 'Kare': 1200/(1/594),
         'StreetFlash': 1200/(1/3589.6)}


def ch_cor(chance, times):
    contr_chance = (1 - chance)
    contr_chance **= times
    new_chance = 1 - contr_chance
    return new_chance


def divide(a, b):
    try:
        res = a / b
    except ZeroDivisionError:
        res = 0
    return res


def divide_by_zero(a, b):
    try:
        res = a / b
    except ZeroDivisionError:
        res = a / 1
    return res


def correct_win_chance(win_chance, round=1, ops=1):
    # mile_stone = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    # floop_divergent = [0.295, 0.251, 0.25, 0.187, 0.133, 0.045, 0.029, 0.013, 0.005, 0.001]
    # turn_divergent = [0.197, 0.184, 0.161, 0.153, 0.141, 0.104, 0.072, 0.059, 0.030, 0.025]
    # river_divergent = [0.093, 0.039, 0.043, 0.036, 0.036, 0.036, 0.04, 0.04, 0.005, 0.005]

    mile_stone = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    pre_divergent = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    floop_divergent = [0.25, 0.25, 0.25, 0.244, 0.185, 0.158, 0.128, 0.063, 0.06, 0.045]
    turn_divergent = [0.09, 0.047, 0.036, 0.015, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    river_divergent = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    if round == 0:
        for i, amo in enumerate(mile_stone):
            if i < (len(mile_stone)-1):
                if amo < win_chance < mile_stone[i+1]:
                    win_chance -= pre_divergent[i]**ops
    elif round == 1:
        for i, amo in enumerate(mile_stone):
            if i == 0:
                if win_chance < amo:
                    win_chance -= floop_divergent[i]
            elif i < (len(mile_stone)-1):
                if amo < win_chance < mile_stone[i+1]:
                    win_chance -= floop_divergent[i]**ops
    elif round == 2:
        for i, amo in enumerate(mile_stone):
            if i == 0:
                if win_chance < amo:
                    win_chance -= turn_divergent[i]
            elif i < (len(mile_stone)-1):
                if amo < win_chance < mile_stone[i+1]:
                    win_chance -= turn_divergent[i]**ops

    elif round == 3:
        for i, amo in enumerate(mile_stone):
            if i == 0:
                if win_chance < amo:
                    win_chance -= river_divergent[i]
            elif i < (len(mile_stone)-1):
                if amo < win_chance < mile_stone[i+1]:
                    win_chance -= river_divergent[i]**ops

    return win_chance


def c(whole, take):
    if whole >= take:
        res = factorial(whole) / (factorial(take) * factorial(whole - take))
    else:
        res = 0
    return res


# конкретный шанс
def chance(in_x_cards, needed_cards, from_pool, search_cards_needed_by=1):
    n = len(from_pool)
    k = in_x_cards
    k2 = needed_cards
    k3 = search_cards_needed_by
    k4 = k - k3

    if in_x_cards >= search_cards_needed_by:
        try:
            all_combinations = c(n, k)

            ways_of_needed = c(k2, k3)

            ways_of_remains = c(n-k2, k4)

            needed_combies = ways_of_needed * ways_of_remains

            chance = needed_combies / all_combinations

            res = chance

        except ValueError:

            res = 0
    else:
        res = 0

    return res


def chance_for_1_pair(in_x_cards, needed_cards, from_pool, search_cards_needed_by=2):
    n = len(from_pool)
    k = in_x_cards
    k2 = needed_cards
    k3 = search_cards_needed_by
    k4 = k - k3

    try:
        all_combinations = c(n, k)

        # содержит удовлетворяющую комбинацию 2 по 4-м, как первая пара
        ways_of_needed = c(4,2)

        ways_of_remains = c(n - k2, k4) - c(4,2)*c(12,1)*c(4,1)*c(11,1) - c(4,3)*c(12,1)

        needed_combies = ways_of_needed * ways_of_remains

        chance = needed_combies / all_combinations

        res = chance

    except ValueError:

        res = 0

    return res


def chance_for_2_pairs(in_x_cards, needed_cards, from_pool, search_cards_needed_by=4):
    n = len(from_pool)
    k = in_x_cards
    k2 = needed_cards
    k3 = search_cards_needed_by
    k4 = k - k3

    try:
        all_combinations = c(n, k)

        # содержит удовлетворяющую комбинацию 2 по 4-м, как первая пара
        ways_of_needed = c(4, 2)*c(4, 2)

        ways_of_remains = c(n - k2, k4)

        needed_combies = ways_of_needed * ways_of_remains

        chance = needed_combies / all_combinations

        res = chance

    except ValueError:

        res = 0

    return res


def chance_for_set(in_x_cards, needed_cards, from_pool, search_cards_needed_by=3):
    n = len(from_pool)
    k = in_x_cards
    k2 = needed_cards
    k3 = search_cards_needed_by
    k4 = k - k3

    try:
        all_combinations = c(n, k)

        # содержит удовлетворяющую комбинацию 2 по 4-м, как первая пара
        ways_of_needed = c(4,3)

        ways_of_remains = c(n - k2, k4) - c(12,1)*c(4,2)

        needed_combies = ways_of_needed * ways_of_remains

        chance = needed_combies / all_combinations

        res = chance

    except ValueError:

        res = 0

    return res


def chance_for_street(in_x_cards, needed_cards, from_pool, search_cards_needed_by=5):
    n = len(from_pool)
    k = in_x_cards
    k2 = needed_cards
    k3 = search_cards_needed_by
    k4 = k - k3

    try:
        all_combinations = c(n, k)

        # комбинации конкретного 5-картового стрита
        ways_of_needed = c(4, 1)*c(4, 1)*c(4, 1)*c(4, 1)*c(4, 1)

        ways_of_remains = c(n - k3, k4)

        needed_combies = ways_of_needed * ways_of_remains

        chance = needed_combies / all_combinations

        res = chance

    except ValueError:

        res =0

    return res


def chance_for_fh(in_x_cards, needed_cards, from_pool, search_cards_needed_by=5):
    n = len(from_pool)
    k = in_x_cards
    k2 = needed_cards
    k3 = search_cards_needed_by
    k4 = k - k3

    try:
        all_combinations = c(n, k)

        # содержит удовлетворяющую комбинацию 2 по 4-м, как первая пара
        ways_of_needed = c(4,3) * c(4,2) * 2

        ways_of_remains = c(n - k2, k4)

        needed_combies = ways_of_needed * ways_of_remains

        chance = needed_combies / all_combinations

        res = chance

    except ValueError:

        res = 0

    return res


def chance_for_flush_street(in_x_cards, needed_cards, from_pool, search_cards_needed_by=5):
    n = len(from_pool)
    k = in_x_cards
    k2 = needed_cards
    k3 = search_cards_needed_by
    k4 = k - k3

    try:
        all_combinations = c(n, k)

        # содержит удовлетворяющую комбинацию 2 по 4-м, как первая пара
        ways_of_needed = 10

        ways_of_remains = c(n - k2, k4)

        needed_combies = ways_of_needed * ways_of_remains

        chance = needed_combies / all_combinations

        res = chance

    except ValueError:

        res = 0

    return res


def count_ways_of_1card_street(model, ways_of_1card_street, i_1):
    if model.count(1) >= 4:
        if model[0:4].count(1) == 3 and model[12] == 1:
            ways_of_1card_street += 1
            if i_1 == 1 and model[0:5].count(1) == 4:
                ways_of_1card_street += 1
            elif i_1 == 1 and model[i_1:i_1+5].count(1) == 4:
                ways_of_1card_street += 1
        elif i_1 == 0 and model[i_1:4] == 4:
            ways_of_1card_street += 2
        else:
            t = 0
            while t < 8:
                if model[t:t+5].count(1) == 4:
                    ways_of_1card_street += 1
                t += 1
    return ways_of_1card_street


def count_ways_of_1card_flash_street(model, suit_flash, map_of_cards, ways_of_1card_flash_street, i_1, i_2, i_3, i_4, i_5, i_6):
    if model[0:4].count(1) == 3 and model[12] == 1:
        if (suit_flash, row[12]) in map_of_cards and (suit_flash, row[i_1]) in map_of_cards:
            if (suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards:
                ways_of_1card_flash_street += 1
        if (i_1 == 1 and model[0:5].count(1) == 4) or (i_1 == 1 and model[i_1:i_1 + 5].count(1) == 4):
            if (suit_flash, row[i_4]) in map_of_cards and (suit_flash, row[i_1]) in map_of_cards:
                if (suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards:
                    ways_of_1card_flash_street += 1
    elif i_1 == 0 and model[i_1:4] == 4:
        if (suit_flash, row[i_4]) in map_of_cards and (suit_flash, row[i_1]) in map_of_cards:
            if (suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards:
                ways_of_1card_flash_street += 2
    else:
        if model[i_1:i_1 + 5].count(1) == 4:
            if (suit_flash, row[i_4]) in map_of_cards and (suit_flash, row[i_1]) in map_of_cards:
                if (suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards:
                    ways_of_1card_flash_street += 1
            if model[i_1:i_1 + 4].count(1) == 4:
                ways_of_1card_flash_street += 1
                if i_1 == 0 and model[12] == 1:
                    ways_of_1card_flash_street -= 1
                elif model.count(1) == 4 and model[12] == 1:
                    ways_of_1card_flash_street -= 1

        if model[i_2:i_2 + 5].count(1) == 4:
            if (suit_flash, row[i_5]) in map_of_cards and (suit_flash, row[i_2]) in map_of_cards:
                if (suit_flash, row[i_3]) in map_of_cards and (suit_flash, row[i_4]) in map_of_cards:
                    ways_of_1card_flash_street += 1
            if model[i_2:i_2 + 4].count(1) == 4:
                ways_of_1card_flash_street += 1
                if model.count(1) == 5 and model[12] == 1:
                    ways_of_1card_flash_street -= 1

        if model[i_3:i_3 + 5].count(1) == 4:
            if (suit_flash, row[i_6]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards:
                if (suit_flash, row[i_4]) in map_of_cards and (suit_flash, row[i_5]) in map_of_cards:
                    ways_of_1card_flash_street += 1
            if model[i_3:i_3 + 4].count(1) == 4:
                ways_of_1card_flash_street += 1
                if model[12] == 1:
                    ways_of_1card_flash_street -= 1

    return ways_of_1card_flash_street


def pre_chance_point(cards_pool, map_of_values, map_of_suits, weight_of_hand = None):
    ways_of_3cards_street = 0
    fh_chance = 0
    flash_chance = 0
    street_chance = 0
    pair_chance = 0
    two_pairs_chance = 0
    set_chance = 0
    kare_chance = 0

    _, suits_amount = zip(*map_of_suits)

    model = copy.copy(map_of_values)

    for i, amount in enumerate(model):
        if amount != 0:
            model[i] = 1

    if weight_of_hand < rangs['Pair']:
        pair_chance = chance(5, 6, cards_pool, search_cards_needed_by=1)

        two_pairs_chance = (c(3, 1)*c(3, 1)*c(len(cards_pool)-8, 3) - 11)/c(len(cards_pool), 5)

        set_chance = chance(5, 3, cards_pool, search_cards_needed_by=2) + chance(5, 3, cards_pool,
                                                                                       search_cards_needed_by=2)

        if model[12] == 1:
            if model[0:4].count(1) == 1 or model[8:12].count(1) == 1:
                ways_of_3cards_street += 1
        elif model[0:5].count(1) == 2:
            i_1 = model.index(1, 0, 5)
            i_2 = model.index(1, i_1 + 1, i_1 + 5)
            ways_of_3cards_street = i_1 + 2
            if ways_of_3cards_street > 5 - (i_2 - i_1):
                ways_of_3cards_street = 5 - (i_2 - i_1)
        elif model[0:5].count(1) == 1:
            i_1 = model.index(1, 0, 5)
            if model[i_1:i_1+5].count(1) == 2:
                i_1 = model.index(1, 0, 5)
                i_2 = model.index(1, i_1 + 1, i_1 + 5)
                ways_of_3cards_street = 5 - (i_2 - i_1)
                if ways_of_3cards_street > i_1 + 2:
                    ways_of_3cards_street = i_1 + 2
        else:
            if model[5:10].count(1) == 2:
                i_1 = model.index(1, 5, 10)
                i_2 = model.index(1, i_1 + 1, i_1 + 5)
                ways_of_3cards_street = 5 - (i_2 - i_1)
                if i_2 == 9 and i_1 == 8:
                    ways_of_3cards_street -= 1
            elif model[5:10].count(1) == 0:
                ways_of_3cards_street = 2
            else:
                i_1 = model.index(1, 5, 10)
                i_2 = model.index(1, i_1+1, 13)
                if i_2 - i_1 > 4:
                    ways_of_3cards_street = 0
                else:
                    ways_of_3cards_street = 5 - (i_2 - i_1)
                    if ways_of_3cards_street > 13 - i_2:
                        ways_of_3cards_street = 13 - i_2

        street_chance = (ways_of_3cards_street*c(4, 1)**3)*c(50-3, 2)/c(50, 5)

        kare_chance = 2*chance(5, 3, cards_pool, search_cards_needed_by=3)

        if 2 in suits_amount:

            flash_chance = chance(5, 11, cards_pool, search_cards_needed_by=3)

    else:
        set_chance = chance(5, 2, cards_pool, search_cards_needed_by=1)
        two_pairs_chance = c(12, 1)*chance(5, 4, cards_pool, search_cards_needed_by=2)
        street_chance = 0
        fh_chance = c(12, 1)*chance(5, 4, cards_pool, search_cards_needed_by=3) + \
                    c(2,1)*c(4,3)*12*c(50-3, 2)/c(50, 5)
        kare_chance = chance(5, 2, cards_pool, search_cards_needed_by=2)

    return [rangs['ElderCard'], round(pair_chance * rangs['Pair']), round(two_pairs_chance * rangs['TwoPairs']), round(set_chance * rangs['Set']),
            round(street_chance * rangs['Street']), round(flash_chance * rangs['Flash']), round(fh_chance * rangs['FullHouse']),
            round(kare_chance * rangs['Kare']), 0, 0, 0]


def floop_chance_point(cards_pool, map_of_values, map_of_suits, map_of_cards, weight_of_hand=None):
    _, suits_amount = zip(*map_of_suits)

    model = copy.copy(map_of_values)

    ways_of_1card_street = 0
    ways_of_1card_flash_street = 0
    fh_chance = 0
    flash_chance = 0
    kare_chance = 0
    flash_street_chance = 0
    street_chance = 0
    set_chance = 0
    two_pairs_chance = 0
    pair_chance = 0
    suit_flash = 0

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

    if weight_of_hand < rangs['Street']:
        ways_of_1card_street = count_ways_of_1card_street(model, ways_of_1card_street, i_1)

        street_chance = ways_of_1card_street * c(4, 1) * c(50 - 4, 1) / c(50 - 3, 2)

    if weight_of_hand < rangs['StreetFlash'] and model.count(1) >= 4:
        if 4 in suits_amount or 5 in suits_amount or 6 in suits_amount:
            for i in map_of_suits:
                if i[1] >= 4:
                    suit_flash = i[0][:-1]

            ways_of_1card_flash_street = count_ways_of_1card_flash_street(model, suit_flash, map_of_cards,
                                                                          ways_of_1card_flash_street, i_1, i_2, i_3, i_4, i_5, i_6)

        flash_street_chance = ways_of_1card_flash_street * c(50 - 4, 1) / c(50 - 3, 2)

    if weight_of_hand < rangs['Kare']:
        if weight_of_hand >= rangs['FullHouse']:
            kare_chance = chance(2, 1, cards_pool, search_cards_needed_by=1) + chance(2, 2, cards_pool,
                                                                                        search_cards_needed_by=2)
        elif rangs['Street'] > weight_of_hand > rangs['Set']:
            kare_chance = chance(2, 1, cards_pool, search_cards_needed_by=1)
        elif rangs['Street'] > weight_of_hand > rangs['TwoPairs']:
            kare_chance = 2*chance(2, 2, cards_pool, search_cards_needed_by=2)
        elif rangs['Street'] > weight_of_hand > rangs['Pair']:
            kare_chance = chance(2, 2, cards_pool, search_cards_needed_by=2)

    if weight_of_hand < rangs['FullHouse']:
        if rangs['Street'] > weight_of_hand > rangs['Set']:
            s = map_of_values.count(1)
            fh_chance = s*chance(2, 3, cards_pool, search_cards_needed_by=1)
        elif rangs['Street'] > weight_of_hand > rangs['TwoPairs']:
            s = map_of_values.count(2)
            fh_chance = s*chance(2, 2, cards_pool, search_cards_needed_by=1)
        elif rangs['Street'] > weight_of_hand > rangs['Pair']:
            s = map_of_values.count(1)
            fh_chance = s * chance(2, 3, cards_pool, search_cards_needed_by=2) + c(2, 1)*c(3, 1)/c(47, 2)

    if weight_of_hand < rangs['Flash']:
        if 4 in suits_amount:
            flash_chance = chance(2, 9, cards_pool, search_cards_needed_by=1)
        elif 3 in suits_amount:
            flash_chance = chance(2, 10, cards_pool, search_cards_needed_by=2)

    if weight_of_hand < rangs['Set']:
        if weight_of_hand > rangs['TwoPairs']:
            set_chance = 2*chance(2, 2, cards_pool, search_cards_needed_by=1)
        elif weight_of_hand > rangs['Pair']:
            set_chance = chance(2, 2, cards_pool, search_cards_needed_by=1)
        else:
            set_chance = 5*chance(2, 3, cards_pool, search_cards_needed_by= 2)

    if weight_of_hand < rangs['TwoPairs']:
        if weight_of_hand > rangs['Pair']:
            two_pairs_chance = chance(2, 9, cards_pool, search_cards_needed_by=1)
        elif weight_of_hand < rangs['Pair']:
            two_pairs_chance = c(5, 2)*c(3, 1)*c(3, 1)/c(47, 2)

    if weight_of_hand < rangs['Pair']:
        pair_chance = chance(2, 15, cards_pool, search_cards_needed_by=1)

    return [rangs['ElderCard'], round(pair_chance * rangs['Pair']), round(two_pairs_chance * rangs['TwoPairs']), round(set_chance * rangs['Set']),
            round(street_chance * rangs['Street']), round(flash_chance * rangs['Flash']), round(fh_chance * rangs['FullHouse']),
            round(kare_chance * rangs['Kare']), round(flash_street_chance * rangs['StreetFlash']),
            ways_of_1card_street, ways_of_1card_flash_street]


def turn_chance_point(cards_pool, map_of_values, map_of_suits, map_of_cards, weight_of_hand=None):
    _, suits_amount = zip(*map_of_suits)

    model = copy.copy(map_of_values)

    ways_of_1card_street = 0
    ways_of_1card_flash_street = 0
    fh_chance = 0
    flash_chance = 0
    kare_chance = 0
    flash_street_chance = 0
    street_chance = 0
    set_chance = 0
    two_pairs_chance = 0
    pair_chance = 0
    suit_flash = 0

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

    if weight_of_hand < rangs['Street']:
        ways_of_1card_street = count_ways_of_1card_street(model, ways_of_1card_street, i_1)

        street_chance = ways_of_1card_street * c(4, 1) / c(50 - 4, 1)

    if weight_of_hand < rangs['StreetFlash'] and model.count(1) >= 4:
        if 4 in suits_amount or 5 in suits_amount or 6 in suits_amount:
            for i in map_of_suits:
                if i[1] >= 4:
                    suit_flash = i[0][:-1]

            ways_of_1card_flash_street = count_ways_of_1card_flash_street(model, suit_flash, map_of_cards,
                                                                          ways_of_1card_flash_street, i_1, i_2, i_3, i_4, i_5, i_6)

        flash_street_chance = ways_of_1card_flash_street / c(50 - 4, 1)

    if weight_of_hand < rangs['Kare']:
        if weight_of_hand >= rangs['FullHouse']:
            kare_chance = chance(1, 1, cards_pool, search_cards_needed_by=1)
        elif rangs['Street'] > weight_of_hand > rangs['Set']:
            kare_chance = chance(1, 1, cards_pool, search_cards_needed_by=1)

    if weight_of_hand < rangs['FullHouse']:
        if rangs['Street'] > weight_of_hand > rangs['Set']:
            s = map_of_values.count(1)
            fh_chance = s*chance(1, 3, cards_pool, search_cards_needed_by=1)
        elif rangs['Street'] > weight_of_hand > rangs['TwoPairs']:
            s = map_of_values.count(2)
            fh_chance = s*chance(1, 2, cards_pool, search_cards_needed_by=1)

    if weight_of_hand < rangs['Flash']:
        if 4 in suits_amount:
            flash_chance = chance(1, 9, cards_pool, search_cards_needed_by=1)

    if weight_of_hand < rangs['Set']:
        if weight_of_hand > rangs['TwoPairs']:
            set_chance = 2*chance(1, 2, cards_pool, search_cards_needed_by=1)
        elif weight_of_hand > rangs['Pair']:
            set_chance = chance(1, 2, cards_pool, search_cards_needed_by=1)

    if weight_of_hand < rangs['TwoPairs']:
        if weight_of_hand > rangs['Pair']:
            two_pairs_chance = chance(1, 12, cards_pool, search_cards_needed_by=1)

    if weight_of_hand < rangs['Pair']:
        pair_chance = chance(2, 18, cards_pool,
                             search_cards_needed_by=1)

    return [rangs['ElderCard'], round(pair_chance * rangs['Pair']), round(two_pairs_chance * rangs['TwoPairs']), round(set_chance * rangs['Set']),
            round(street_chance * rangs['Street']), round(flash_chance * rangs['Flash']), round(fh_chance * rangs['FullHouse']),
            round(kare_chance * rangs['Kare']), round(flash_street_chance * rangs['StreetFlash']),
            ways_of_1card_street, ways_of_1card_flash_street]


suits = ['Черви_', 'Трефы_', 'Буби_', 'Пики_']
row = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

ch = list((suits[0]+i for i in row))
tr = list((suits[1]+i for i in row))
bu = list((suits[2]+i for i in row))
pi = list((suits[3]+i for i in row))

pool = bu+tr+ch+pi

pool2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

test = pool

flash_street = 4*chance_for_flush_street(5, 13, test, search_cards_needed_by=5)

kare = 13*chance(5, 4, test, search_cards_needed_by=4)
only_kare = kare

street = 10*chance_for_street(5, 5, test, search_cards_needed_by=5)
only_street = street - flash_street

flush = 4*chance(5, 13, test, search_cards_needed_by=5)
only_flush = flush - flash_street

fh = c(13,2)*chance_for_fh(5, 8, test, search_cards_needed_by=5)
only_fh = fh

sat = 13*chance_for_set(5, 4, test, search_cards_needed_by=3)
only_sat = sat

two_pairs = c(13, 2)*chance_for_2_pairs(5, 8, test, search_cards_needed_by=4)
only_two_pairs = two_pairs

# шанс выпадения в течение игры пары для одного игрока
one_pair = 13*chance_for_1_pair(5, 4, test, search_cards_needed_by=2)
only_one_pair = one_pair


# def count_ways_of_op_3card_street(model, ways_of_2cards_street, ways_of_3cards_street, i_1, i_2, i_3):
#     if model[12] == 1:
#         if model[0:4].count(1) == 1 or model[8:12].count(1) == 1:
#             ways_of_3cards_street += 1
#         elif model[0:4].count(1) == 2:
#             ways_of_2cards_street += 1
#             if i_1 == 2:
#                 ways_of_3cards_street += 2
#             elif i_1 == 1:
#                 ways_of_3cards_street += 1
#
#     elif model[0:5].count(1) == 3:
#         if model[i_1:i_3+1].count(0) == 0:
#             ways_of_2cards_street += 3 - (1 - i_1)
#         elif model[i_1:i_3+1].count(0) == 1:
#             ways_of_2cards_street += 2
#             ways_of_3cards_street += 1
#         elif model[i_1:i_3+1].count(0) == 2:
#             ways_of_2cards_street += 1
#             if i_2 - i_1 == 3:
#                 ways_of_3cards_street += 2
#             elif i_2 - i_1 == 2:
#                 ways_of_3cards_street += 1
#
#     elif model[0:5].count(1) == 2:
#         if model[i_1:i_2+1].count(0) == 0:
#             ways_of_3cards_street = 4 - (2 - i_1)
#
#             if ways_of_3cards_street > 4: ways_of_3cards_street = 4
#
#             if i_3 - i_2 == 3:
#                 ways_of_3cards_street -= 2
#                 ways_of_2cards_street += 1
#             elif i_3-i_2 == 2:
#                 ways_of_2cards_street += 2
#                 ways_of_3cards_street -= 3
#
#         elif model[i_1:i_2+1].count(0) == 1:
#             ways_of_3cards_street = 4 - (2 - i_1)
#
#             if ways_of_3cards_street > 3: ways_of_3cards_street = 3
#
#             if i_3 - i_2 == 2:
#                 ways_of_3cards_street -= 2
#                 ways_of_2cards_street += 1
#             elif i_3-i_2 == 1:
#                 ways_of_2cards_street += 2
#                 ways_of_3cards_street = 1
#
#
#
#
#
#         if ways_of_3cards_street > 5 - (i_2 - i_1):
#             ways_of_3cards_street = 5 - (i_2 - i_1)
#
#
#     elif model[0:5].count(1) == 1:
#         i_1 = model.index(1, 0, 5)
#         if model[i_1:i_1 + 5].count(1) == 2:
#             i_1 = model.index(1, 0, 5)
#             i_2 = model.index(1, i_1 + 1, i_1 + 5)
#             ways_of_3cards_street = 5 - (i_2 - i_1)
#             if ways_of_3cards_street > i_1 + 2:
#                 ways_of_3cards_street = i_1 + 2
#     else:
#         if model[5:10].count(1) == 2:
#             i_1 = model.index(1, 5, 10)
#             i_2 = model.index(1, i_1 + 1, i_1 + 5)
#             ways_of_3cards_street = 5 - (i_2 - i_1)
#             if i_2 == 9 and i_1 == 8:
#                 ways_of_3cards_street -= 1
#         elif model[5:10].count(1) == 0:
#             ways_of_3cards_street = 2
#         else:
#             i_1 = model.index(1, 5, 10)
#             i_2 = model.index(1, i_1 + 1, 13)
#             if i_2 - i_1 > 4:
#                 ways_of_3cards_street = 0
#             else:
#                 ways_of_3cards_street = 5 - (i_2 - i_1)
#                 if ways_of_3cards_street > 13 - i_2:
#                     ways_of_3cards_street = 13 - i_2
#
#     return ways_of_1card_street


def count_ways_of_op_street(model, suit_flash, map_of_cards, player_model, remain_pool):
    t = 0
    ways_of_3card_street, ways_of_2card_street, ways_of_1card_street, ways_of_2card_flash_street, \
    ways_of_1card_flash_street = 0, 0, 0, 0, 0

    previously_added_3card_way = False
    previously_added_2card_way = False
    previously_added_1card_way = False

    previously_added_2card_flash_street_way = False
    previously_added_1card_flash_street_way = False

    sch3_correction = 0

    while t <= 8:

        d = player_model[t:t + 5].count(1) - model[t:t + 5].count(1)
        last_correct = 0

        try:
            i_1 = model.index(1, t, t + 5)
        except ValueError:
            i_1 = 50
        try:
            i_2 = model.index(1, i_1 + 1, t + 5)
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

        if t == 0:
            if model[12] == 1 and model[t:t+4].count(1) == 1:
                ways_of_3card_street += 1
                previously_added_3card_way = True

            elif model[12] == 1 and model[t:t+4].count(1) == 2:
                ways_of_2card_street += 1
                previously_added_2card_way = True

                if (suit_flash, row[i_1]) in map_of_cards and (suit_flash, row[i_2]) in map_of_cards and (
                suit_flash, row[12]) in map_of_cards:
                    ways_of_2card_flash_street += 1
                    previously_added_2card_flash_street_way = True

            elif model[12] == 1 and model[t:t+4].count(1) == 3:
                ways_of_1card_street += 1
                previously_added_1card_way = True

                if (suit_flash, row[i_1]) in map_of_cards and (suit_flash, row[i_2]) in map_of_cards and (
                suit_flash, row[i_3]) in map_of_cards and (suit_flash, row[12]) in map_of_cards:
                    ways_of_1card_flash_street += 1
                    previously_added_1card_flash_street_way = True

                elif (suit_flash, row[i_1]) in map_of_cards and (suit_flash, row[i_2]) in map_of_cards and (
                suit_flash, row[i_3]) in map_of_cards or (suit_flash, row[i_2]) in map_of_cards and (
                suit_flash, row[i_3]) in map_of_cards and (suit_flash, row[12]) in map_of_cards or (
                suit_flash, row[i_1]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards and (
                suit_flash, row[12]) in map_of_cards or (suit_flash, row[i_1]) in map_of_cards and (
                suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[12]) in map_of_cards:

                    ways_of_2card_flash_street += 1
                    previously_added_2card_flash_street_way = True

        if model[t:t + 5].count(1) == 2:

            ways_of_3card_street += 1

            if d != 0:
                if d == 2:
                    sch3_correction += 1*c(3, 1)*c(4, 1) + c(3, 1)*1*c(4, 1) + 1*1*c(4, 1)
                    last_correct = 1*c(3, 1)*c(4, 1) + c(3, 1)*1*c(4, 1) + 1*1*c(4, 1)

                elif d == 1:
                    sch3_correction += 1*c(4, 1)*c(4, 1)
                    last_correct = 1*c(4, 1)*c(4, 1)
            else:
                last_correct = 0

            previously_added_3card_way = True

            if i_1 == t and i_3 == t + 5:
                ways_of_3card_street -= 1

                sch3_correction -= last_correct

                previously_added_3card_way = False

            elif previously_added_2card_way:
                ways_of_3card_street -= 1

                sch3_correction -= last_correct

                previously_added_3card_way = False

            previously_added_1card_way = False
            previously_added_2card_way = False

        elif model[t:t + 5].count(1) == 3:

            ways_of_2card_street += 1

            if (suit_flash, row[i_1]) in map_of_cards and (suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards:
                ways_of_2card_flash_street += 1
                previously_added_2card_flash_street_way = True

                if i_1 == t and i_4 == t + 5 and (suit_flash, row[i_4]) in map_of_cards:
                    ways_of_2card_flash_street -= 1
                    previously_added_2card_flash_street_way = False

                elif previously_added_1card_flash_street_way:
                    ways_of_2card_flash_street -= 1
                    previously_added_2card_flash_street_way = False

                previously_added_1card_flash_street_way = False
            else:
                previously_added_2card_flash_street_way = False
                previously_added_1card_flash_street_way = False

            if previously_added_3card_way:
                ways_of_3card_street -= 1

                sch3_correction -= last_correct

            previously_added_2card_way = True

            if i_1 == t and i_4 == t + 5:
                ways_of_2card_street -= 1
                previously_added_2card_way = False

            elif previously_added_1card_way:
                ways_of_2card_street -= 1
                previously_added_2card_way = False

            previously_added_3card_way = False
            previously_added_1card_way = False

        elif model[t:t + 5].count(1) == 4:

            ways_of_1card_street += 1

            if (suit_flash, row[i_1]) in map_of_cards and (suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards and (suit_flash, row[i_4]) in map_of_cards:
                ways_of_1card_flash_street += 1
                previously_added_1card_flash_street_way = True

                if previously_added_2card_flash_street_way:
                    ways_of_2card_flash_street -= 1

                if i_1 == t and i_5 == t + 5 and (suit_flash, row[i_5]) in map_of_cards:
                    ways_of_1card_flash_street -= 1
                    previously_added_1card_flash_street_way = False

                previously_added_2card_flash_street_way = False
            elif (suit_flash, row[i_1]) in map_of_cards and (suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards or (suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards and (suit_flash, row[i_4]) in map_of_cards or (suit_flash, row[i_1]) in map_of_cards and (suit_flash, row[i_3]) in map_of_cards and (suit_flash, row[i_4]) in map_of_cards or (suit_flash, row[i_1]) in map_of_cards and (suit_flash, row[i_2]) in map_of_cards and (suit_flash, row[i_4]) in map_of_cards:
                ways_of_2card_flash_street += 1
                previously_added_2card_flash_street_way = True

                previously_added_1card_flash_street_way = False
            else:
                previously_added_1card_flash_street_way = False
                previously_added_2card_flash_street_way = False

            if previously_added_2card_way:
                ways_of_2card_street -= 1

            previously_added_1card_way = True

            if i_1 == t and i_5 == t + 5:
                ways_of_1card_street -= 1
                previously_added_1card_way = False

            previously_added_3card_way = False
            previously_added_2card_way = False

        else:
            previously_added_3card_way = False
            previously_added_2card_way = False
            previously_added_1card_way = False

            previously_added_2card_flash_street_way = False
            previously_added_1card_flash_street_way = False

        t += 1

    return ways_of_1card_street, ways_of_2card_street, ways_of_3card_street, ways_of_1card_flash_street, ways_of_2card_flash_street, sch3_correction


def op_floop_chance(map_of_suits, map_of_cards, map_of_values, player_map_of_value, map_of_pool_suits, map_of_pool_value, remain_pool,
                    ways_of_player_1card_street, ways_of_p_1c_fs, weight_of_hand=None, p_has_pair=False, opc=1):

    op_suits, suits_amount = zip(*map_of_suits)

    pool_suits, pool_suits_amount = zip(*map_of_pool_suits)

    model = copy.copy(map_of_values)

    pm = copy.copy(player_map_of_value)

    fh_chance = 0
    flash_chance = 0
    kare_chance = 0
    flash_street_chance = 0
    street_chance = 0
    set_chance = 0
    two_pairs_chance = 0
    pair_chance = 0

    if suits_amount.count(4) != 0:
        i = suits_amount.index(4)
        suit_flash = op_suits[i][:-1]
    elif suits_amount.count(3) != 0:
        i = suits_amount.index(3)
        suit_flash = op_suits[i][:-1]
    else:
        suit_flash = 'Пики'

    s2cor = 0

    for i, amount in enumerate(model):
        if amount != 0:
            model[i] = 1

    for i, amount in enumerate(pm):
        if amount != 0:
            pm[i] = 1

    i_1 = model.index(1, 0, 14)
    aa = map_of_pool_value[i_1]

    try:
        i_2 = model.index(1, i_1 + 1, 14)
        bb = map_of_pool_value[i_2]
    except ValueError:
        i_2 = 100
        bb = 0
    try:
        i_3 = model.index(1, i_2 + 1, 14)
        cc = map_of_pool_value[i_3]
    except ValueError:
        i_3 = 200
        cc = 0
    try:
        i_4 = model.index(1, i_3 + 1, 14)
        dd = map_of_pool_value[i_4]
    except ValueError:
        i_4 = 300
        dd = 0
    try:
        i_5 = model.index(1, i_4 + 1, 14)
        ee = map_of_pool_value[i_5]
    except ValueError:
        i_5 = 400
        ee = 0

    if weight_of_hand < rangs['Street']:
        ways_of_1card_street, ways_of_2card_street, ways_of_3card_street, _, _, s3cor = \
            count_ways_of_op_street(model, suit_flash, map_of_cards, pm, remain_pool)

        # определяет участие карт игрока в стрите, если 0, то карты игрока ни при чем и коррекция 0

        if ways_of_1card_street != 0:
            differ = ways_of_player_1card_street - ways_of_1card_street
        else:
            differ = 0

        scho1c = c(4, 1) * c(len(remain_pool) - 1, 2)
        scho2c = c(4, 1) * c(4, 1) * c(len(remain_pool) - 2, 1)
        scho3c = c(4, 1) * c(4, 1) * c(4, 1)

        # print('s3cor {}'.format(s3cor))
        # print('ways_of_3card_street {}, scho3c {}'.format(ways_of_3card_street, scho3c))

        if differ > 0:
            # pair on prefloopchance
            if not p_has_pair:
                s2cor = 1*c(4, 1)*c(len(remain_pool) - 2, 1)*differ
            else:
                s2cor = 2*1*c(4, 1)*c(len(remain_pool) - 2, 1)*differ

        street_chance = (ways_of_2card_street * scho2c - s2cor) / c(len(remain_pool), 3) + \
                        (ways_of_3card_street * scho3c - s3cor) / c(len(remain_pool), 3) + \
                        (ways_of_1card_street * scho1c) / c(len(remain_pool), 3)

    if weight_of_hand < rangs['StreetFlash']:
        _, _, _, ways_of_1card_flash_street, ways_of_2card_flash_street, _ = \
            count_ways_of_op_street(model, suit_flash, map_of_cards, pm, remain_pool)

        flash_street_chance = (ways_of_2card_flash_street - ways_of_p_1c_fs) * 1 * 1 * c(len(remain_pool) - 2, 1) / c(len(remain_pool), 3) +\
                              ways_of_1card_flash_street * 1 * c(len(remain_pool) - 2, 2) / c(len(remain_pool), 3)

    if weight_of_hand < rangs['Flash']:

        # 2 имеющихся совпадения 2х карт по масти для 3карточного флеша
        if suits_amount.count(2) >= 1:
            for i, amount in enumerate(suits_amount):
                if amount == 2:
                    remain_amount_of_suit_flash = pool_suits_amount[i]
                    flash_chance += c(remain_amount_of_suit_flash, 3) / c(len(remain_pool), 3)
        # 1 совпание 2х карт по масти для 3карточного флеша
        elif suits_amount.count(3) == 1:
            for i, amount in enumerate(suits_amount):
                remain_amount_of_suit_flash = pool_suits_amount[i]
                if amount == 3:
                    flash_chance += c(remain_amount_of_suit_flash, 2)*c(len(remain_pool) - 2, 1) / c(len(remain_pool), 3)
        elif suits_amount.count(4) == 1:
            for i, amount in enumerate(suits_amount):
                remain_amount_of_suit_flash = pool_suits_amount[i]
                if amount == 4:
                    flash_chance += c(remain_amount_of_suit_flash, 1)*c(len(remain_pool) - 1, 2) / c(len(remain_pool), 3)

    if weight_of_hand < rangs['Kare']:

        # условие для ривера готово:
        if weight_of_hand > rangs['FullHouse']:

            x1 = map_of_values.index(3)
            x2 = map_of_values.index(2)
            minus1 = map_of_pool_value[x1]
            minus2 = map_of_pool_value[x2]

            kare_chance = (c(minus1, 1)*c(len(remain_pool) - 1, 1) + c(minus2, 2))/c(len(remain_pool), 2)

        elif rangs['Street'] > weight_of_hand > rangs['Set']:

            x = map_of_values.index(3)
            minus = map_of_pool_value[x]

            kare_chance = (c(minus, 1)*c(len(remain_pool) - minus, 2) + c(aa, 3) + c(bb, 3) + c(cc, 3)) / c(len(remain_pool), 3)

        elif rangs['Set'] > weight_of_hand > rangs['TwoPairs']:

            x1 = map_of_values.index(2)
            x2 = map_of_values.index(2, x1+1, 14)
            minus1 = map_of_pool_value[x1]
            minus2 = map_of_pool_value[x2]

            kare_chance = (c(minus1, 2) * c(len(remain_pool) - minus1, 1) + c(minus2, 2) * c(
                len(remain_pool) - minus2, 1)) / c(len(remain_pool), 3)

        elif rangs['TwoPairs'] > weight_of_hand > rangs['Pair']:

            x = map_of_values.index(2)
            minus = map_of_pool_value[x]

            kare_chance = (c(minus, 2) * c(len(remain_pool) - minus, 1) + c(aa, 3) + c(bb, 3) + c(cc, 3) + c(dd, 3)) / c(len(remain_pool), 3)

    if weight_of_hand < rangs['FullHouse']:
        if rangs['Street'] > weight_of_hand > rangs['Set']:

            x = map_of_values.index(3)
            minus = map_of_pool_value[x]

            try:
                y1 = map_of_values.index(1)
            except ValueError:
                y1 = -1

            try:
                y2 = map_of_values.index(1, y1+1, 14)
            except ValueError:
                y2 = -1

            def just_for_this():
                t = 0
                res = 0
                while t < 13:
                    if t != y1 and t != y2 and t != x:
                        res += c(map_of_pool_value[t], 2)*c(len(remain_pool) -2, 1)
                    t += 1

                return res

            fh_chance = chance(3, aa+bb+cc-minus, remain_pool, search_cards_needed_by=1) + just_for_this() / c(len(remain_pool), 3)

        elif rangs['Set'] > weight_of_hand > rangs['TwoPairs']:
            x1 = map_of_values.index(2)
            x2 = map_of_values.index(2, x1 + 1, 14)
            minus1 = map_of_pool_value[x1]
            minus2 = map_of_pool_value[x2]

            def just_for_this():
                t = 0
                res = 0
                while t < 13:
                    if t != x1 and t != x2:
                        res += c(map_of_pool_value[t], 3)
                    t += 1

                return res

            fh_chance = chance(3, minus1 + minus2, remain_pool, search_cards_needed_by=1) + just_for_this()/c(len(remain_pool), 3)

        elif rangs['TwoPairs'] > weight_of_hand > rangs['Pair']:
            x = map_of_values.index(2)
            minus = map_of_pool_value[x]

            try:
                y1 = map_of_values.index(1)
            except ValueError:
                y1 = -1

            try:
                y2 = map_of_values.index(1, y1+1, 14)
            except ValueError:
                y2 = -1

            try:
                y3 = map_of_values.index(1, y2+1, 14)
            except ValueError:
                y3 = -1

            def just_for_this():
                t = 0
                res = 0
                while t < 13:
                    if t != y1 and t != y2 and t != y3 and t != x:
                        res += c(map_of_pool_value[t], 3)
                    t += 1

                return res

            part = c(minus, 1)*(c(aa, 1) + c(bb, 1) + c(cc, 1) + c(dd, 1) - c(minus, 1))*c(len(remain_pool)-aa-bb-cc-dd-ee, 1)

            fh_chance = ((c(aa, 2) + c(bb, 2) + c(cc, 2) + c(dd, 2) - c(minus, 2))*c(len(remain_pool)-aa-bb-cc-dd, 1) +
                         just_for_this() + part) / c(len(remain_pool), 3)

        elif weight_of_hand < rangs['Pair']:
            part = c(aa, 2) * (c(bb, 1) + c(cc, 1) + c(dd, 1)) + c(bb, 2) * (c(aa, 1) + c(cc, 1) + c(dd, 1)) \
                   + c(cc, 2) * (c(aa, 1) + c(bb, 1) + c(dd, 1)) + c(dd, 2) * (c(aa, 1) + c(bb, 1) + c(cc, 1))

            fh_chance = part / c(len(remain_pool), 3)

    if weight_of_hand < rangs['Set']:
        if weight_of_hand > rangs['TwoPairs']:
            x1 = map_of_values.index(2)
            x2 = map_of_values.index(2, x1 + 1, 14)

            minus1 = map_of_pool_value[x1]
            minus2 = map_of_pool_value[x2]

            set_chance = chance(3, minus1+minus2, remain_pool, search_cards_needed_by=1)

        elif weight_of_hand > rangs['Pair']:
            x1 = map_of_values.index(2)

            minus1 = map_of_pool_value[x1]

            set_chance = chance(3, minus1, remain_pool, search_cards_needed_by=1)

        else:
            x1 = map_of_values.index(1)
            x2 = map_of_values.index(1, x1 + 1, 14)
            x3 = map_of_values.index(1, x2 + 1, 14)
            try:
                x4 = map_of_values.index(1, x3 + 1, 14)
            except ValueError:
                x4 = -1

            def just_for_this():
                t = 0
                res = 0
                while t < 13:
                    if t != x1 and t != x2 and t != x3 and t != x4:
                        res += c(map_of_pool_value[t], 3)
                    t += 1

                return res

            set_chance = (c(len(remain_pool)-aa-bb-cc-dd-ee, 1)*(c(aa, 2) + c(bb, 2) + c(cc, 2) +
                                                   c(dd, 2) + c(ee, 2)) + just_for_this())/c(len(remain_pool), 3)

    if weight_of_hand < rangs['TwoPairs']:
        if weight_of_hand > rangs['Pair']:
            x1 = map_of_values.index(2)

            minus1 = map_of_pool_value[x1]

            two_pairs_chance = c(len(remain_pool)-aa-bb-cc-dd-ee, 2)*(c(aa, 1) + c(bb, 1) + c(cc, 1) +
                                                         c(dd, 1) + c(ee, 1) - c(minus1, 1))/c(len(remain_pool), 3)

        elif weight_of_hand < rangs['Pair']:

            part = c(len(remain_pool)-aa-bb-cc-dd-ee, 1) * c(aa, 1) * (c(bb, 1) + c(cc, 1) + c(dd, 1)) + \
                   c(len(remain_pool)-aa-bb-cc-dd-ee, 1) * c(bb, 1) * (c(cc, 1) + c(dd, 1)) + \
                   c(len(remain_pool)-aa-bb-cc-dd-ee, 1) * c(cc, 1) * c(dd, 1)

            two_pairs_chance = part / c(len(remain_pool), 3)

    if weight_of_hand < rangs['Pair']:
        x1 = map_of_values.index(1)
        x2 = map_of_values.index(1, x1 + 1, 14)
        x3 = map_of_values.index(1, x2 + 1, 14)
        try:
            x4 = map_of_values.index(1, x3 + 1, 14)
        except ValueError:
            x4 = -1

        def just_for_this():
            t = 0
            res = 0
            while t < 13:
                if t != x1 and t != x2 and t != x3 and t != x4:
                    res += c(map_of_pool_value[t], 2)
                t += 1

            return res

        pair_chance = chance(3, aa+bb+cc+dd+ee, remain_pool, search_cards_needed_by=1) + \
                      just_for_this()*c(len(remain_pool)-aa-bb-cc-dd, 1) / c(len(remain_pool), 3)

    return [rangs['ElderCard'], round(ch_cor(pair_chance, opc)*rangs['Pair']),
            round(ch_cor(two_pairs_chance, opc)*rangs['TwoPairs']), round(ch_cor(set_chance, opc)*rangs['Set']),
            round(ch_cor(street_chance, opc)*rangs['Street']), round(ch_cor(flash_chance, opc)*rangs['Flash']),
            round(ch_cor(fh_chance, opc)*rangs['FullHouse']), round(ch_cor(kare_chance, opc)*rangs['Kare']),
            round(ch_cor(flash_street_chance, opc)*rangs['StreetFlash'])]


def op_river_chance(map_of_suits, map_of_cards, map_of_values, player_map_of_value, map_of_pool_suits, map_of_pool_value, remain_pool,
                    ways_of_player_1card_street, ways_of_p_1c_fs, weight_of_hand=None, p_has_pair=False, opc=1):

    op_suits, suits_amount = zip(*map_of_suits)

    pool_suits, pool_suits_amount = zip(*map_of_pool_suits)

    model = copy.copy(map_of_values)

    pm = copy.copy(player_map_of_value)

    fh_chance = 0
    flash_chance = 0
    kare_chance = 0
    flash_street_chance = 0
    street_chance = 0
    set_chance = 0
    two_pairs_chance = 0
    pair_chance = 0

    if suits_amount.count(4) != 0:
        i = suits_amount.index(4)
        suit_flash = op_suits[i][:-1]
    elif suits_amount.count(3) != 0:
        i = suits_amount.index(3)
        suit_flash = op_suits[i][:-1]
    else:
        suit_flash = 'Пики'

    s2cor = 0

    for i, amount in enumerate(model):
        if amount != 0:
            model[i] = 1

    for i, amount in enumerate(pm):
        if amount != 0:
            pm[i] = 1

    i_1 = model.index(1, 0, 14)
    aa = map_of_pool_value[i_1]

    try:
        i_2 = model.index(1, i_1 + 1, 14)
        bb = map_of_pool_value[i_2]
    except ValueError:
        i_2 = 100
        bb = 0
    try:
        i_3 = model.index(1, i_2 + 1, 14)
        cc = map_of_pool_value[i_3]
    except ValueError:
        i_3 = 200
        cc = 0
    try:
        i_4 = model.index(1, i_3 + 1, 14)
        dd = map_of_pool_value[i_4]
    except ValueError:
        i_4 = 300
        dd = 0
    try:
        i_5 = model.index(1, i_4 + 1, 14)
        ee = map_of_pool_value[i_5]
    except ValueError:
        i_5 = 400
        ee = 0

    if weight_of_hand < rangs['Street']:
        ways_of_1card_street, ways_of_2card_street, _, _, _, _ = \
            count_ways_of_op_street(model, suit_flash, map_of_cards, pm, remain_pool)

        # определяет участие карт игрока в стрите, если 0, то карты игрока ни при чем и коррекция 0
        differ = ways_of_player_1card_street - ways_of_1card_street

        scho1c = c(4, 1) * c(len(remain_pool) - 1, 1)
        scho2c = c(4, 1) * c(4, 1)

        if differ > 0:
            # pair on prefloopchance
            if not p_has_pair:
                s2cor = 1*c(4, 1)*differ
            else:
                s2cor = 2*1*c(4, 1)*differ

        street_chance = (ways_of_2card_street * scho2c - s2cor) / c(len(remain_pool), 2) + \
                        (ways_of_1card_street * scho1c) / c(len(remain_pool), 2)

    if weight_of_hand < rangs['StreetFlash']:
        _, _, _, ways_of_1card_flash_street, ways_of_2card_flash_street, _ = \
            count_ways_of_op_street(model, suit_flash, map_of_cards, pm, remain_pool)

        flash_street_chance = (ways_of_2card_flash_street - ways_of_p_1c_fs) * 1 * 1 / c(len(remain_pool), 2) +\
                              ways_of_1card_flash_street * 1 * c(len(remain_pool) - 1, 1) / c(len(remain_pool), 2)

    if weight_of_hand < rangs['Flash']:
        if suits_amount.count(3) == 1:
            for i, amount in enumerate(suits_amount):
                remain_amount_of_suit_flash = pool_suits_amount[i]
                if amount == 3:
                    flash_chance += c(remain_amount_of_suit_flash, 2) / c(len(remain_pool), 2)
        elif suits_amount.count(4) == 1:
            for i, amount in enumerate(suits_amount):
                remain_amount_of_suit_flash = pool_suits_amount[i]
                if amount == 4:
                    flash_chance += c(remain_amount_of_suit_flash, 1)*c(len(remain_pool) - 1, 1) / c(len(remain_pool), 2)

    if weight_of_hand < rangs['Kare']:

        # условие для ривера готово:
        if weight_of_hand > rangs['FullHouse']:

            x1 = map_of_values.index(3)
            x2 = map_of_values.index(2)
            minus1 = map_of_pool_value[x1]
            minus2 = map_of_pool_value[x2]

            kare_chance = (c(minus1, 1)*c(len(remain_pool) - 1, 1) + c(minus2, 2))/c(len(remain_pool), 2)

        elif rangs['Street'] > weight_of_hand > rangs['Set']:

            x = map_of_values.index(3)
            minus = map_of_pool_value[x]

            kare_chance = c(minus, 1)*c(len(remain_pool) - 1, 1) / c(len(remain_pool), 2)

        elif rangs['Set'] > weight_of_hand > rangs['TwoPairs']:

            x1 = map_of_values.index(2)
            x2 = map_of_values.index(2, x1+1, 14)
            minus1 = map_of_pool_value[x1]
            minus2 = map_of_pool_value[x2]

            kare_chance = (c(minus1, 2) + c(minus2, 2)) / c(len(remain_pool), 2)

        elif rangs['TwoPairs'] > weight_of_hand > rangs['Pair']:

            x = map_of_values.index(2)
            minus = map_of_pool_value[x]

            kare_chance = c(minus, 2) / c(len(remain_pool), 2)

    if weight_of_hand < rangs['FullHouse']:
        if rangs['Street'] > weight_of_hand > rangs['Set']:

            x = map_of_values.index(3)
            minus = map_of_pool_value[x]

            try:
                y1 = map_of_values.index(1)
            except ValueError:
                y1 = -1

            try:
                y2 = map_of_values.index(1, y1+1, 14)
            except ValueError:
                y2 = -1

            def just_for_this():
                t = 0
                res = 0
                while t < 13:
                    if t != y1 and t != y2 and t != x:
                        res += c(map_of_pool_value[t], 2)
                    t += 1

                return res

            fh_chance = chance(2, aa+bb+cc-minus, remain_pool, search_cards_needed_by=1) + just_for_this() / c(len(remain_pool), 2)

        elif rangs['Set'] > weight_of_hand > rangs['TwoPairs']:
            y = map_of_values.index(1)
            minus = map_of_pool_value[y]

            fh_chance = chance(2, aa+bb+cc-minus, remain_pool, search_cards_needed_by=1) + chance(2, minus, remain_pool, search_cards_needed_by=2)

        elif rangs['TwoPairs'] > weight_of_hand > rangs['Pair']:
            x = map_of_values.index(2)
            minus = map_of_pool_value[x]

            y1 = map_of_values.index(1)
            minus1 = map_of_pool_value[y1]

            y2 = map_of_values.index(1, y1+1, 14)
            minus2 = map_of_pool_value[y2]

            y3 = map_of_values.index(1, y2+1, 14)
            minus3 = map_of_pool_value[y3]

            fh_chance = c(minus, 1)*(c(minus1, 1) + c(minus2, 1) + c(minus3, 1))/c(len(remain_pool), 2)

    if weight_of_hand < rangs['Set']:
        if weight_of_hand > rangs['Pair']:
            x1 = map_of_values.index(2)

            minus1 = map_of_pool_value[x1]

            set_chance = chance(2, minus1, remain_pool, search_cards_needed_by=1)

        else:
            set_chance = (c(aa, 2) + c(bb, 2) + c(cc, 2) + c(dd, 2) + c(ee, 2)) / c(len(remain_pool), 2)

    if weight_of_hand < rangs['TwoPairs']:
        if weight_of_hand > rangs['Pair']:
            x = map_of_values.index(2)
            y1 = map_of_values.index(1)
            y2 = map_of_values.index(1, y1 + 1, 14)
            y3 = map_of_values.index(1, y2 + 1, 14)

            def just_for_this():
                t = 0
                res = 0
                while t < 13:
                    if t != y1 and t != y2 and t != y3 and t != x:
                        res += c(map_of_pool_value[t], 2)
                    t += 1

                return res

            minus1 = map_of_pool_value[x]

            two_pairs_chance = (c(len(remain_pool)-aa-bb-cc-dd, 1)*(c(aa, 1) + c(bb, 1) + c(cc, 1) +
                                                         c(dd, 1) + c(ee, 1) - c(minus1, 1)) + just_for_this()) / c(len(remain_pool), 2)

        elif weight_of_hand < rangs['Pair']:
            part = c(aa, 1) * (c(bb, 1) + c(cc, 1) + c(dd, 1) + c(ee, 1)) + \
                   c(bb, 1) * (c(cc, 1) + c(dd, 1) + c(ee, 1)) + \
                   c(cc, 1) * (c(dd, 1) + c(ee, 1)) + \
                   c(dd, 1) * c(ee, 1)

            two_pairs_chance = part / c(len(remain_pool), 2)

    if weight_of_hand < rangs['Pair']:

        x1 = map_of_values.index(1)
        x2 = map_of_values.index(1, x1 + 1, 14)
        x3 = map_of_values.index(1, x2 + 1, 14)
        x4 = map_of_values.index(1, x3 + 1, 14)
        x5 = map_of_values.index(1, x4 + 1, 14)

        def just_for_this():
            t = 0
            res = 0
            while t < 13:
                if t != x1 and t != x2 and t != x3 and t != x4 and t != x5:
                    res += c(map_of_pool_value[t], 2)
                t += 1

            return res

        pair_chance = chance(2, aa+bb+cc+dd+ee, remain_pool, search_cards_needed_by=1) + \
                      just_for_this() / c(len(remain_pool), 2)

    return [rangs['ElderCard'], round(ch_cor(pair_chance, opc)*rangs['Pair']),
            round(ch_cor(two_pairs_chance, opc)*rangs['TwoPairs']), round(ch_cor(set_chance, opc)*rangs['Set']),
            round(ch_cor(street_chance, opc)*rangs['Street']), round(ch_cor(flash_chance, opc)*rangs['Flash']),
            round(ch_cor(fh_chance, opc)*rangs['FullHouse']), round(ch_cor(kare_chance, opc)*rangs['Kare']),
            round(ch_cor(flash_street_chance, opc)*rangs['StreetFlash'])]


# print('Шанс одной пары {}%'.format(only_one_pair*100))
# print('Шанс двух пар {}%'.format(only_two_pairs*100))
# print('Шанс сета {}%'.format(only_sat*100))
# print('Шанс стрита {}%'.format(only_street*100))
# print('Шанс флэша {}%'.format(only_flush*100))
# print('Шанс фул хаус {}%'.format(only_fh*100))
# print('Шанс каре {}%'.format(only_kare*100))
# print('Шанс флэш-стрит {}%'.format(flash_street*100))

# x = [0,0,0,0,0,0,2,0,0,0,0,0,0]
# x1 = [0,0,1,0,1,1,1,0,1,0,0,0,1]
# map_of_cards = [('Трефы', '4'), ('Трефы', '6'), ('Трефы', '7'), ('Трефы', '8'), ('Буби', '10'), ('Трефы', 'A')]
# map_of_suits = [('Черви_', 0), ('Трефы_', 5), ('Буби_', 1), ('Пики_', 0)]


# poo_ = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
poo1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

# pre_chance_point(poo_, x, [('Черви_', 1), ('Трефы_', 1), ('Буби_', 0), ('Пики_', 0)], weight_of_hand = 1600)

# floop_chance_point(poo1, x1, map_of_suits, map_of_cards, weight_of_hand=900)

# turn_chance_point(poo1, x1, map_of_suits, map_of_cards, weight_of_hand=900)

# [('Пики', '7'), ('Пики', '5'), ('Буби', '5'), ('Пики', 'K'), ('Черви', 'Q'), ('Пики', '4')] [0, 0, 1, 2, 0, 1, 0, 0, 0, 0, 1, 1, 0]

# print(count_ways_of_op_street([0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0]))

# print(count_ways_of_op_street([0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1]))


# model = [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0]
# map_of_c = [('Пики', '9'), ('Пики', '10'), ('Трефы', '5'), ('Буби', 'Q'), ('Пики', '8')]
# suit_f = 'Пики'

# model2 = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1]
# map_of_c2 = [('Пики', 'Q'), ('Трефы', 'A'), ('Пики', '3'), ('Пики', '5'), ('Черви', 'K'), ('Буби', '4')]
# suit_f2 = 'Пики'

# print(count_ways_of_op_street(model, suit_f, map_of_c))
# print(count_ways_of_op_street(model2, suit_f2, map_of_c2))

# map_of_floop_val = [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
# map_of_c = [('Пики', '9'), ('Пики', '10'), ('Пики', '8')]
# map_of_s = [('Черви_', 0), ('Трефы_', 0), ('Буби_', 0), ('Пики_', 3)]
# suit_f = 'Пики'
#
# map_of_player_val = [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0]
# map_of_p_cards = [('Трефы', '5'), ('Пики', 'Q'), ('Пики', '9'), ('Пики', '10'), ('Пики', '8')]
# map_of_ssss = [('Черви_', 0), ('Трефы_', 0), ('Буби_', 1), ('Пики_', 4)]
#
# map_of_pool_value = [4, 4, 4, 3, 4, 4, 3, 3, 3, 4, 3, 4, 4]
# map_of_pool_s = [('Черви_', 13), ('Трефы_', 12), ('Буби_', 12), ('Пики_', 10)]
#
# res = op_floop_chance(map_of_s, map_of_c, map_of_floop_val, map_of_player_val, map_of_pool_s, map_of_pool_value, pool, 1, 1, 700, False)
#
# print(res)
#
# res_of_p = floop_chance_point(pool, map_of_player_val, map_of_ssss, map_of_p_cards, weight_of_hand=900)
# print(res_of_p)
# queue = list(i for i in range(5))
# for i in range(2, 2):
#     print(i)
#
# a = [20, 1]
# b = [10, 5]
# aa = [1, 80]
# c = [a, b, aa]
# c = sorted(c)
# print(c)
# try:
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#
#         time.sleep(2)
#
#         x1, y1 = pyautogui.position()
#
#         if x != x1 or y != y1:
#             print(positionStr, end='\n')
#
# except KeyboardInterrupt:
#     print('\n')

# a = [0, 0, 1, 0, 1, 0, 1]
# b = [2, 2, 2, 2, 2, 2, 2]
#
# ccc = list(map(lambda x, y: x / y, a, b))
# ccc = ccc[6:]
# print(ccc)
# ccc = reduce(lambda x, y: x + y, ccc)
# print(ccc)

# flash_street = (10*4)/c(52, 5)
# kare = 13*c(48, 1)/c(52, 5)
# fullh = 13*12*c(4, 3)*c(4, 2)/c(52, 5)
# flash = 4*c(13, 5)/c(52, 5) - flash_street
# street = 10*c(4, 1)*c(4, 1)*c(4, 1)*c(4, 1)*c(4, 1)/c(52, 5) - flash_street
# sat = 13*c(4, 3)*c(49, 2)/c(52, 5) - kare - fullh
# two_p = c(13, 2)*c(4, 2)*c(4, 2)*c(48, 1)/c(52, 5) - fullh
# p = 13*c(4, 2)*c(50, 3)/c(52, 5) - kare - fullh - sat - two_p
#
# print([p, two_p, sat, street, flash, fullh, kare, flash_street])
# a = [0, 1, 2, 1, 5]
#
# def make(num):
#     if num == 1:
#         pass
#
#         print('yes')
#
# make(1)
# time.sleep(2)
# print(pyautogui.locateOnScreen('turn_v2.png'))

def func(val):
    return val[1], val[0]


a = [(1, 2), (4, 3), (3, 3), (2, 6), (3, 1), (4, 1)]

a.sort(key=func)

print(a)

# def make(*args):
#     a = []
#     for i in args:
#         a.append(i)
#     return a
#
#
# print(make(a, b))
