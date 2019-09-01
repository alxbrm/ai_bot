from get_cards import Player, Game, Opponent
from functions import adjust_basic_params, interface, capture_participants_nicks
from pyautogui import screenshot, locateOnScreen


def catch_handout():
    print('Перехватываем начало новой раздачи-игры')
    pass
    return True


def exit_program():
    pass
    # прописываем выход из выполнения работы


def catch_ai_turn():
    print('Перехватываем очередь хода ИИ')
    return True


def catch_the_end_of_game(kol):
    res = False
    if input('Перехватываем окончание игры-раздачи. 1/-1') == 1:
        res = True
    # if cath_the_end:
    #     kol.end_of_game = True
    return res


def add_money(player, limit, cash):
    if 0 < player.bank / limit < 1:
        if limit - player.bank < cash:
            add = (limit - player.bank)

            # прописываем алгоритм добавления средств
            player.bank += add
            cash -= add
        else:
            add = cash

            # прописываем алгоритм добавления средств
            player.bank += add
            cash = 0
        print('ВНЕСЛИ БАБЛИШКО ЗА ИГРОКА {}, остаток на счету {}'.format(add, cash))
    return cash


def get_opponents(n):
    t = 1
    n.append(Player(bank=int(player_bank)))
    while t < quantity_of_m:
        n.append(Opponent(nick='Оппонент №' + str(t), bank=limit))
        t += 1

    return n


def actualize_opponents(participants):
    new_parts = []
    print('Актуализируем ставки оппонентов')
    get_opponents(new_parts)

    for i, amo in enumerate(participants):

        if amo.nick != new_parts[i].nick:
            amo.nick = new_parts[i].nick
            amo.blef_rank = 0

        amo.bank = new_parts[i].bank

    new_parts.clear()

    return participants


def execute(participants, game_num, basic, small_blind, limit):

    print('\n\n**********Начало игры №{}***************\n\n'.format(game_num))

    # screenshot('prefloop_v2.png', region=basic['absolut_floop'])
    # screenshot('floop_v2.png', region=basic['absolut_turn'])

    if game_num == 1:
        screenshot('pics/bb_marker_2c_v2.png', region=basic['absolut_bb_marker'])
        screenshot('pics/f6.png', region=basic['absolut_call'])
        basic['abs_m_b'] = locateOnScreen('pics/max_button.png')

        if not basic['abs_m_b']:
            print('\n\n\n!!!ПЕРЕХВАТИЛИ ОШИБКУ_1 НА СТАРТЕ!!!\n\n\n')
            basic['abs_m_b'] = tuple(map(lambda x, y: x + y, (506, 531, 43, 21), basic['base_point']))

        basic['absolut_bet_input'] = (basic['abs_m_b'][0] + basic['abs_m_b'][2]-5,
                                      basic['abs_m_b'][1] + basic['abs_m_b'][3]+5)

    elif game_num == 2:
        screenshot('pics/sb_marker_1c_v2.png', region=basic['absolut_bb_marker'])

    participants[0].blef_rises = 0

    capture_participants_nicks(basic['absolut_nicks_coords'], participants)

    kol = Game(game_num, small_blind)

    interface(kol, participants, basic, small_blind, limit)

    return kol.game_num


played_circles = 0
ii_wins = 0

small_blind = 1

player_bank = small_blind * 2 * 50
limit = small_blind * 2 * 50
available_cash = limit * 8

coefficient_of_stack_with_op = 1
quantity_of_m = 6

participants = []

get_opponents(participants)

game_num = 1

while True:
    if locateOnScreen('pics/f6.png'):
        break

basic = adjust_basic_params()

while True:

    execute(participants, game_num, basic, small_blind, limit)

    # player_cash_in_game = add_money(participants[0], player_bank, player_cash_in_game)

    game_num += 1
