import random, copy


rangs = {'ElderCard': 147, 'Pair': 1200/(1/1.28), 'TwoPairs': 1200/(1/3.26), 'Set': 1200/(1/19.7),
         'Street': 1200/(1/20.6), 'Flash': 1200/(1/32.1), 'FullHouse': 1200/(1/37.5), 'Kare': 1200/(1/594),
         'StreetFlash': 1200/(1/3589.6)}

suits = ['Черви_', 'Трефы_', 'Буби_', 'Пики_']
row = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

variations_of_streets = [
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
]

map_of_c = [('Пики', '10'), ('Пики', 'J'), ('Пики', 'Q'), ('Пики', 'K'), ('Пики', 'A')]
map_of_s = [('Черви_', 0), ('Трефы_', 0), ('Буби_', 0), ('Пики_', 5)]
map_of_v = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
map_of_v3 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2]


def take_card_from_pool(pool, times=1, test_mode=False):
    player_cards = ['Трефы_K', 'Буби_J']
    floop_cards = ['Трефы_6', 'Пики_Q', 'Черви_J']
    turn_cards = ['Буби_5']
    river_cards = ['Буби_J']

    i = 0
    got_cards = []
    if not test_mode:
        while i < times:
            x = random.choice(pool)
            got_cards.append(x)
            pool.remove(x)
            i += 1
    elif test_mode == 1:
        while i < times:
            x = player_cards[i]
            got_cards.append(x)
            pool.remove(x)
            i += 1
    elif test_mode == 2:
        while i < times:
            x = floop_cards[i]
            got_cards.append(x)
            pool.remove(x)
            i += 1
    elif test_mode == 3:
        while i < times:
            x = turn_cards[i]
            got_cards.append(x)
            pool.remove(x)
            i += 1
    elif test_mode == 4:
        while i < times:
            x = river_cards[i]
            got_cards.append(x)
            pool.remove(x)
            i += 1

    return got_cards


def counter(i, in_list, where_add, quantity_of_cells):
    t = 0
    while t < quantity_of_cells:
        if i in in_list[t]:
            where_add[t] += 1
        t += 1


def convert_to_point(value):
    try:
       return int(value)
    except ValueError:
        if value == 'J':
            return 11
        elif value == 'Q':
            return 12
        elif value == 'K':
            return 13
        elif value == 'A':
            return 14


def quantity_combinations(suits_in_hand, values_in_hand):
    suits_amount = [0, 0, 0, 0]
    values_amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in suits_in_hand:
        counter(i, suits, suits_amount, len(suits_amount))
    for i in values_in_hand:
        counter(i, row, values_amount, len(values_amount))
    map_of_suits = list(zip(suits, suits_amount))
    map_of_values = list(zip(row, values_amount))
    return map_of_suits, map_of_values, values_amount


def create_maps(hand):
    suits_in_hand = []
    values_in_hand = []
    points = []
    for i in hand:
        suit, value = i.split('_')
        suits_in_hand.append(suit)
        values_in_hand.append(value)
        try:
            points.append(int(value))
        except ValueError:
            points.append(convert_to_point(value))
    # map_of_cards = list(zip(suits_in_hand, values_in_hand, points))
    map_of_cards = list(zip(suits_in_hand, values_in_hand))
    map_of_suits, map_of_values, values_amount = quantity_combinations(suits_in_hand, values_in_hand)
    return map_of_suits, map_of_cards, values_amount


def find_out_the_strongest_possibilities(values_amount):

    max_e, _, _, _, _, max_f, _, _, max_fs = results_count(map_of_s, map_of_c, map_of_v, False)
    _, max_p, _, _, _, _, _, _, _ = results_count(map_of_s, map_of_c, map_of_v3, False)

    elder_card_weights = []
    streets_weights = []
    set_weights = []
    two_pairs_weights = []
    full_house_weights = []
    kare_weights = []

    def simulate_vars(start, where_append_weights, func_to_count_weight):

        try:
            first_ind = model.index(0, start)
            model[first_ind] = 1
        except ValueError:
            first_ind = 13

        try:
            second_ind = model.index(0, first_ind)
            model[second_ind] = 1
        except ValueError:
            second_ind = 13

        while second_ind < 13:

            weight, _ = func_to_count_weight(model)
            weight_2, _ = elder_card(model)

            where_append_weights.append(weight)

            model[second_ind] = 0

            try:
                second_ind = model.index(0, second_ind + 1)
                model[second_ind] = 1
            except ValueError:
                second_ind = 13

        try:
            model[first_ind] = 0
        except IndexError:
            pass

    model = copy.copy(values_amount)

    for i, amount in enumerate(model):
        if amount != 0:
            model[i] = 1

    # print('model {}'.format(model))
    t = 0

    while t < 13:
        simulate_vars(t, streets_weights, street)
        t += 1

    # print('model после симулэйт {}'.format(model))
    streets_weights = set(streets_weights)

    try:
        streets_weights.remove(0)
    except KeyError:
        pass

    streets_weights = list(streets_weights)

    n = 0

    while n < 13:
        simulate_vars(n, elder_card_weights, elder_card)
        n += 1

    elder_card_weights = sorted(elder_card_weights)

    for i, w in enumerate(model):
        if w != 0:
            model[i] = 3
            set_weights.append(sat(model))
            model[i] = 1

    if values_amount.count(2) > 0 and values_amount.count(3) == 0:
        a = values_amount.index(2)
        try:
            a = values_amount.index(2, a + 1)
        except ValueError:
            pass

        for i, w in enumerate(values_amount):

            if i != a:
                model[a] = 2
                sxs = model[i]
                model[i] = 2
                two_pairs_weights.append(two_pairs(model))
                model[a] = 1
                model[i] = sxs

    elif values_amount.count(2) == 0 and values_amount.count(3) == 0:

        for i, w in enumerate(values_amount):

            if w != 0:
                model[i] = 2
                try:
                    a = model.index(1, i + 1)
                except ValueError:
                    a = 13

                while a < 13:
                    model[a] = 2
                    two_pairs_weights.append(two_pairs(model))
                    model[a] = 1
                    try:
                        a = model.index(1, a + 1)
                    except ValueError:
                        a = 13

                model[i] = 1

    if values_amount.count(2) > 0 and values_amount.count(3) == 0:
        for i, w in enumerate(values_amount):

            a = values_amount.index(2)
            try:
                b = values_amount.index(2, a + 1)
            except ValueError:
                b = 13

            if w == 1:
                model[i] = 2
                model[a] = 3
                full_house_weights.append(full_house(model))
                model[a] = 2
                model[i] = 3
                full_house_weights.append(full_house(model))
                model[a] = 1
                try:
                    model[b] = 2
                    full_house_weights.append(full_house(model))
                    model[b] = 3
                    model[i] = 2
                    full_house_weights.append(full_house(model))
                    model[b] = 1
                except IndexError:
                    pass
                model[i] = 1

            elif w == 2 and i == a:
                pass

            elif w == 2 and i != a:
                model[i] = 2
                model[a] = 3
                full_house_weights.append(full_house(model))
                model[i] = 3
                model[a] = 2
                full_house_weights.append(full_house(model))
                model[a] = 1
                model[i] = 1

    elif values_amount.count(3) > 0:
        for i, w in enumerate(values_amount):
            sxs = model[i]
            model[i] = 2
            b = values_amount.index(3)
            model[b] = 3
            full_house_weights.append(full_house(model))

            if i == b:
                pass

            if w == 1 or w == 2:
                model[i] = 3
                model[b] = 2
                full_house_weights.append(full_house(model))

            model[i] = sxs
            model[b] = 1

    for i, w in enumerate(values_amount):
        if w > 1:
            model[i] = 4
            kare_weights.append(kare(model))

    return elder_card_weights, max_p, two_pairs_weights, set_weights, streets_weights, max_f, full_house_weights, kare_weights, max_fs


def elder_card(values_amount):
    basic_weight = []
    add_weight = []
    for i, amount in enumerate(values_amount):
        if amount == 1:
            basic_weight.append(rangs['ElderCard'])
            add_weight.append(i+1)

    add_weight = sorted(add_weight, reverse=True)

    k = 70
    max_add_w = 0

    for i in add_weight:
        max_add_w += i*k
        k /= 10

    try:
        weight_of_hand = max(basic_weight) + max_add_w
    except ValueError:
        weight_of_hand = 0

    return weight_of_hand, 0


def pair(values_amount):
    basic_weight = []
    add_weight = []
    for i, amount in enumerate(values_amount):
        if amount == 2:
            basic_weight.append(rangs['Pair'])
            add_weight.append((i + 2) * 70)

    try:
        weight_of_hand = max(basic_weight) + max(add_weight)
    except ValueError:
        weight_of_hand = 0

    return weight_of_hand


def two_pairs(values_amount):
    basic_weight = []
    add_weight = []
    weight_of_hand = 0
    for i, amount in enumerate(values_amount):
        if amount == 2:
            basic_weight.append(rangs['TwoPairs'])
            add_weight.append((i + 2) * 70)

    add_weight = sorted(add_weight, reverse=True)

    if len(basic_weight) > 1:
        try:
            weight_of_hand = max(basic_weight) + add_weight[0] + add_weight[1]/70
        except ValueError:
            weight_of_hand = 0

    return weight_of_hand


def sat(values_amount):
    basic_weight = []
    add_weight = []
    for i, amount in enumerate(values_amount):
        if amount == 3:
            basic_weight.append(rangs['Set'])
            add_weight.append((i + 2) * 70)

    try:
        weight_of_hand = max(basic_weight) + max(add_weight)
    except ValueError:
        weight_of_hand = 0

    return weight_of_hand


def street(values_amount):
    s0 = str([1,1,1,1])[1:-1]
    s1 = str([1,1,1,1,1])[1:-1]
    s2 = str([1,1,1,1,1,1])[1:-1]
    s3 = str([1,1,1,1,1,1,1])[1:-1]
    model = copy.copy(values_amount)
    strt = []
    for i, amount in enumerate(model):
        if amount != 0:
            model[i] = 1

    if model.count(1) == 6:
        if s1 in str(model[0:5]) and model[12] > 0:
            strt.append(variations_of_streets[0])
            strt.append(variations_of_streets[1])
        elif s0 in str(model[0:4]) and model[12] > 0:
            strt.append(variations_of_streets[0])
        else:
            cut_from = 0
            end_on = 6
            while end_on < 14:
                if s2 in str(model[cut_from:end_on]):
                    strt.append(variations_of_streets[end_on-5])
                    strt.append(variations_of_streets[end_on-4])
                elif s1 in str(model[cut_from:end_on]):
                    if s1 in str(model[cut_from+1:end_on]):
                        strt.append(variations_of_streets[end_on-4])
                    else:
                        strt.append(variations_of_streets[end_on-5])
                cut_from += 1
                end_on += 1

    if model.count(1) == 7:
        if s2 in str(model[0:6]) and model[12] > 0:
            strt.append(variations_of_streets[0])
            strt.append(variations_of_streets[1])
            strt.append(variations_of_streets[2])
        elif s1 in str(model[0:5]) and model[12] > 0:
            strt.append(variations_of_streets[0])
            strt.append(variations_of_streets[1])
        elif s0 in str(model[0:4]) and model[12] > 0:
            strt.append(variations_of_streets[0])
        else:
            cut_from = 0
            end_on = 7
            while end_on < 14:
                if s3 in str(model[cut_from:end_on]):
                    strt.append(variations_of_streets[end_on - 6])
                    strt.append(variations_of_streets[end_on - 5])
                    strt.append(variations_of_streets[end_on - 4])
                elif s2 in str(model[cut_from:end_on]):
                    if s2 in str(model[cut_from+1:end_on]):
                        strt.append(variations_of_streets[end_on - 5])
                        strt.append(variations_of_streets[end_on - 4])
                    elif s2 in str(model[cut_from:end_on-1]):
                        strt.append(variations_of_streets[end_on - 6])
                        strt.append(variations_of_streets[end_on - 5])
                elif s1 in str(model[cut_from:end_on]):
                    if s1 in str(model[cut_from+2:end_on]):
                        strt.append(variations_of_streets[end_on - 4])
                    elif s1 in str(model[cut_from:end_on-2]):
                        strt.append(variations_of_streets[end_on - 6])
                    elif s1 in str(model[cut_from+1:end_on-1]):
                        strt.append(variations_of_streets[end_on - 5])
                cut_from += 1
                end_on += 1

    basic_weight = []
    add_weight = []

    if strt:
        model = strt
    else:
        model = [model]

    for i, amount in enumerate(variations_of_streets):
        for t in model:
            if t == amount:
                basic_weight.append(rangs['Street'])
                add_weight.append(i*110)
            else:
                pass

    try:
        weight_of_hand = max(basic_weight) + max(add_weight)
    except ValueError:
        weight_of_hand = 0

    try:
        weight_of_hand_vars = list(map(lambda x: max(basic_weight) + x, add_weight))
    except ValueError:
        weight_of_hand_vars = [0]

    return weight_of_hand, weight_of_hand_vars


def flash(map_of_suits, map_of_cards):

    basic_weight = []
    add_weight = []
    suit_flash = 0

    for i in map_of_suits:
        if i[1] >= 5:
            basic_weight.append(rangs['Flash'])
            suit_flash = i[0][:-1]
            for card in map_of_cards:
                if i[0][:-1] in card[0]:
                    add_weight.append(convert_to_point(card[1]))
        else:
            pass

    add_weight = sorted(add_weight, reverse=True)

    try:
        max_add_w = add_weight[0]*100 + add_weight[1]*10 + add_weight[2] + add_weight[3]*0.1 + add_weight[4]*0.01
    except IndexError:
        max_add_w = 0

    try:
        weight_of_hand = max(basic_weight) + max_add_w
    except ValueError:
        weight_of_hand = 0

    return weight_of_hand, suit_flash, basic_weight, add_weight


def full_house(values_amount):
    basic_weight = []
    add_weight = []
    weight_of_hand = 0

    if sat(values_amount) > 0 and pair(values_amount) > 0:
        basic_weight.append(rangs['FullHouse'])
        add_weight.append(sat(values_amount) - rangs['Set'] + (pair(values_amount) - rangs['Pair'])/70)

    add_weight = sorted(add_weight, reverse=True)

    if len(basic_weight) > 0:
        try:
            weight_of_hand = max(basic_weight) + max(add_weight)
        except ValueError:
            weight_of_hand = 0

    return weight_of_hand


def kare(values_amount):
    basic_weight = []
    add_weight = []
    for i, amount in enumerate(values_amount):
        if amount == 4:
            basic_weight.append(rangs['Kare'])
            add_weight.append((i+2)*70)

    try:
        weight_of_hand = max(basic_weight) + max(add_weight)
    except ValueError:
        weight_of_hand = 0

    return weight_of_hand


def street_flash(suit_flash, street_weight_vars, map_of_cards):
    basic_weight = []
    add_weight = []
    that_is_flush = False

    for sv in street_weight_vars:
        i = int((sv - rangs['Street'])/110)
        if i >= 0:
            pass
        else:
            break

        s = variations_of_streets[i]

        for t, amount in enumerate(s):
            if amount == 1:
                if (suit_flash, row[t]) in map_of_cards:
                    that_is_flush = True
                else:
                    that_is_flush = False
                    break

        if that_is_flush:
            basic_weight.append(rangs['StreetFlash'])
            add_weight.append(i*110)

    try:
        weight_of_hand = max(basic_weight) + max(add_weight)
    except ValueError:
        weight_of_hand = 0

    return weight_of_hand


def separate_points(list):
    new_list = copy.copy(list)

    new_list[1] -= new_list[0]/70
    new_list[2] -= new_list[0]/700
    new_list[3] -= new_list[0]/70
    new_list[7] -= new_list[0]/70

    return new_list


def results_count(map_of_suits, map_of_cards, values_amount, show_info=True):

    points = []

    weight_of_elder_card, _ = elder_card(values_amount)
    if weight_of_elder_card == 0:
        weight_of_elder_card = rangs['ElderCard']
    points.append(weight_of_elder_card)
    if weight_of_elder_card > 0 and show_info:
        print('Максимально очков за ELDER_CARD:{}'.format(weight_of_elder_card))

    weight_of_pair = pair(values_amount) + weight_of_elder_card/70
    points.append(weight_of_pair)
    if pair(values_amount) > 0 and show_info:
        print('Максимально очков за PAIR:{}'.format(weight_of_pair))

    weight_of_two_pairs = two_pairs(values_amount) + weight_of_elder_card/700
    points.append(weight_of_two_pairs)
    if two_pairs(values_amount) > 0 and show_info:
        print('Максимально очков за TWO-PAIRS:{}'.format(weight_of_two_pairs))

    weight_of_set = sat(values_amount) + weight_of_elder_card/70
    points.append(weight_of_set)
    if sat(values_amount) > 0 and show_info:
        print('Максимально очков за SET:{}'.format(weight_of_set))

    weight_of_strt, strt_weight_vars = street(values_amount)
    points.append(weight_of_strt)
    if weight_of_strt > 0 and show_info:
        print('Максимально очков за STREET:{}'.format(weight_of_strt))

    weight_of_flash, suit_flash, _, _ = flash(map_of_suits, map_of_cards)
    points.append(weight_of_flash)
    if weight_of_flash > 0 and show_info:
        print('Максимально очков за FLUSH:{}'.format(weight_of_flash))

    weight_of_fh = full_house(values_amount)
    points.append(weight_of_fh)
    if weight_of_fh > 0 and show_info:
        print('Максимально очков за FULL-HOUSE:{}'.format(weight_of_fh))

    weight_of_kare = kare(values_amount) + weight_of_elder_card/70
    points.append(weight_of_kare)
    if weight_of_kare >= rangs['Kare'] and show_info:
        print('Максимально очков за KARE:{}'.format(weight_of_kare))

    weight_of_strt_flash = street_flash(suit_flash, strt_weight_vars, map_of_cards)
    points.append(weight_of_strt_flash)
    if weight_of_strt_flash > 0 and show_info:
        print('Максимально очков за FLUSH-STREET:{}'.format(weight_of_strt_flash))

    return points
