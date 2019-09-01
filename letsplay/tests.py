from engine import Player, Game, Opponent
import copy


def add_money(player, limit):
    if 0 <= player.bank / limit < 1:
        if limit - player.bank < player.available_cash:
            add = (limit - player.bank)
            player.bank += add
            player.available_cash -= add
        else:
            add = player.available_cash
            player.bank += add
            player.available_cash = 0
        print('{} внёс ${}, остаток на счету ${}'.format(player.nick, add, player.available_cash))


def fill_banks_of_members(participants, num_of_members, bank=1000, coe_stack=1):
    elements = len(participants)
    for i, amo in enumerate(participants):
        if i < num_of_members:
            amo.bank = int(bank)
            amo.available_cash = bank * 3
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
    for i, amo in enumerate(participants):
        if amo.bank == 0 and i != 0:
            print('Из игры удалён {}'.format(amo.nick))

            setattr(amo, 'nick', amo.nick + str(1))

            amo.bank = limit
            amo.available_cash = limit * 3

            print('\nВ игру вступил {}, его банк {}, доступный кэш {}\n'.format(amo.nick, amo.bank, amo.available_cash))


def execute(participants, game_num, small_blind, num_of_members, bank=1000, coe_stack=1):

    print('\n\nНачало игры №{}\n\n'.format(game_num))

    if game_num == 1:
        fill_banks_of_members(participants, num_of_members, bank, coe_stack=coe_stack)

    participants[0].limit = participants[0].bank
    participants[0].blef_rises = 0

    for p in participants:
        p.in_game = True

    kol = Game(game_num, small_blind, test_mode=False)

    kol.handout(num_of_members-1)
    kol.make_round(participants)
    kol.make_round(participants)
    kol.make_round(participants)
    kol.make_round(participants)
    kol.make_round(participants)

    for p in participants:
        add_money(p, limit)

    check_banks(participants)

    if len(participants) == 1:
        print('Игра окончена: победитель {}, выигрыш ${}'.format(participants[0].nick, participants[0].bank))

    return kol.game_num


played_circles = 0
ii_wins = 0

small_blind = 1
limit = small_blind * 2 * 50
available_cash = limit * 3

coefficient_of_stack_with_op = 1
quantity_of_m = 2
max_circles = 100

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
            bank=limit, coe_stack=coefficient_of_stack_with_op)

    game_num = 2

    quantity_of_remain_members = len(participants)

    while (ai.bank + ai.available_cash) > limit / 3:

        if (ai.bank + ai.available_cash) > (limit + available_cash) * 2:
            ii_wins += 1
            break

        execute(participants, game_num, small_blind=small_blind, num_of_members=quantity_of_members)

        game_num += 1

    played_circles += 1

print('{} побед ii из {} игровых циклов'.format(ii_wins, max_circles))
