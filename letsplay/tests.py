from engine import Player, Game, Opponent
import copy


def add_money(player, limit, cash):
    if 0 < player.bank / limit < 1:
        if limit - player.bank < cash:
            add = (limit - player.bank)
            player.bank += add
            cash -= add
        else:
            add = cash
            player.bank += add
            cash = 0
        print('ВНЕСЛИ БАБЛИШКО ЗА ИГРОКА {}, остаток на счету {}'.format(add, cash))
    return cash


def fill_banks_of_members(participants, num_of_members, bank=1000, coe_stack=1):
    elements = len(participants)
    for i, amo in enumerate(participants):
        if i < num_of_members:
            amo.bank = int(bank)
            if i == 0:
                amo.limit = int(bank)
            # тестируем случай, когда банк P меньше банка О в 2 раза
            if i != 0:
                amo.bank *= coe_stack

    while elements > num_of_members:
        participants.pop()
        elements -= 1

    return participants


def check_banks(participants):
    dupl = copy.copy(participants)
    for i, amo in enumerate(dupl):
        if amo.bank == 0 and i != 0:
            print('Из игры удалён {}'.format(amo.nick))

            # participants.remove(amo)

            setattr(amo, 'nick', amo.nick + str(1))

            amo.bank = player_bank

            print('\nВ игру вступил {}, его банк {}\n'.format(amo.nick, amo.bank))


def execute(participants, game_num, small_blind, num_of_members, bank=1000, coe_stack=1):

    print('\n\nНачало игры №{}\n\n'.format(game_num))

    if game_num == 1:
        fill_banks_of_members(participants, num_of_members, bank, coe_stack=coe_stack)

    kol = Game(game_num, small_blind)

    kol.handout(num_of_members-1)

    kol.make_round(participants)

    kol.make_round(participants)

    kol.make_round(participants)

    kol.make_round(participants)

    kol.make_round(participants)

    check_banks(participants)

    if len(participants) == 1:
        print('Игра окончена: победитель {}, выигрыш {}'.format(participants[0].nick, participants[0].bank))

    return kol.game_num


played_circles = 0
ii_wins = 0

small_blind = 1
player_bank = small_blind * 2 * 50
available_cash = player_bank

coefficient_of_stack_with_op = 1
quantity_of_m = 3
max_circles = 1000


# 2 игрока выигрыш с равными банкроллами P и O у P 74% all-in на префлопе
# 2 игрока выигрыш с банкроллами P < O в 2 раза у P 53% all-in на префлопе
# 2 игрока выигрыш с банкроллами P < O в 3 раза у P 39% all-in на префлопе

# 2 игрока выигрыш с равными банкроллами P и O у P 82% all-in на флопе
# 2 игрока выигрыш с банкроллами P < O в 2 раза у P 67% all-in на флопе
# 2 игрока выигрыш с банкроллами P < O в 3 раза у P 53% all-in на флопе

# 2 игрока выигрыш с равными банкроллами P и O у P 86% all-in на терне
# 2 игрока выигрыш с банкроллами P < O в 2 раза у P 69% all-in на терне
# 2 игрока выигрыш с банкроллами P < O в 3 раза у P 53% all-in на терне

# 2 игрока выигрыш с равными банкроллами P и O у P 75 % all-in на ривере
# 2 игрока выигрыш с банкроллами P < O в 2 раза у P 52% all-in на ривере
# 2 игрока выигрыш с банкроллами P < O в 3 раза у P 34% all-in на ривере

while played_circles < max_circles:

    quantity_of_members = quantity_of_m

    ai = Player()

    opponent_1 = Opponent(nick='Сенсей')
    opponent_2 = Opponent(nick='Гарри Поттер')
    opponent_3 = Opponent(nick='Терминатор')
    opponent_4 = Opponent(nick='Робокоп')
    opponent_5 = Opponent(nick='Сыч')
    opponent_6 = Opponent(nick='Босс')
    opponent_7 = Opponent(nick='Бродяга')

    participants = [ai, opponent_1, opponent_2, opponent_3, opponent_4, opponent_5, opponent_6, opponent_7]

    execute(participants, game_num=1, small_blind=small_blind, num_of_members=quantity_of_members,
            bank=player_bank, coe_stack=coefficient_of_stack_with_op)

    player_cash_in_game = add_money(ai, player_bank, available_cash)

    game_num = 2

    quantity_of_remain_members = len(participants)

    while ai.bank > 0:

        # if len(participants) == 1:
        #     break

        if ai.bank > (player_bank + available_cash) * 2:
            break

        execute(participants, game_num, small_blind=small_blind, num_of_members=quantity_of_members)

        player_cash_in_game = add_money(ai, player_bank, player_cash_in_game)

        game_num += 1

    # if ai.bank > 0:
    #     ii_wins += 1

    if ai.bank > (player_bank + available_cash) * 2:
        ii_wins += 1

    played_circles += 1

print('{} побед ii из {} игровых циклов'.format(ii_wins, max_circles))
