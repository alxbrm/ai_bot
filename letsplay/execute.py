from engine import Player, Game, Opponent


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
        print('{} пополнил банк ${}, остаток на счету ${}'.format(player.nick, add, player.available_cash))


def fill_banks_of_members(participants, num_of_members, bank=1000):
    elements = len(participants)
    for i, amo in enumerate(participants):
        if i <= num_of_members:
            amo.bank = int(bank)
            amo.available_cash = bank * 3
            if i == 0:
                amo.limit = int(bank)

    while elements > num_of_members:
        participants.pop()
        elements -= 1

    return participants


def check_banks(participants):
    if participants[1].bank <= 0:
        print('Увы, Вы банкрот')
        exit()

    to_remove = []
    for i, amo in enumerate(participants):
        if amo.bank == 0:
            to_remove.append(amo)

    for amo in to_remove:
        participants.remove(amo)


def execute(participants, game_num, small_blind, num_of_members):
    print('\n №{}\n'.format(game_num))

    if game_num == 1:
        fill_banks_of_members(participants, num_of_members, bank=limit)

    participants[0].limit = participants[0].bank
    participants[0].blef_rises = 0

    for p in participants:
        p.in_game = True

    kol = Game(game_num, small_blind)

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
        exit()

    return kol.game_num


small_blind = 1
limit = small_blind * 100
ai = Player()

lets_play = input(f'\n\nЖелаете сыграть в техасский холдем (SmallBlind $1; Limit $100; Available_Cash $300) против {ai.nick}? Y/N\n')

if not lets_play == 'Y' and not lets_play == 'y':
    exit()
else:
    human_name = input('\n\nКак к вам обращаться?\n\n')
    add_op = input(f'\n\nЗа ваш стол поммимо {ai.nick} могут присоединиться еще до 6 случайных участников. '
                   f'Игроки они слабые, но очень любят играть. Сколько таких ребят вы хотите пустить за стол? '
                   f'Укажите число от 0 до 6? \n\n')

    try:
        add_op = int(add_op)
    except ValueError:
        add_op = 0

    if isinstance(add_op, int):
        if add_op > 6:
            add_op = 6
        elif add_op < 0:
            add_op = 0
    else:
        add_op = 0

    opponent_1 = Opponent(nick=human_name, auto_bet=False)
    opponent_2 = Opponent(nick='Гарри Поттер')
    opponent_3 = Opponent(nick='Терминатор')
    opponent_4 = Opponent(nick='Робокоп')
    opponent_5 = Opponent(nick='Сыч')
    opponent_6 = Opponent(nick='Босс')
    opponent_7 = Opponent(nick='Бродяга')

    participants = [ai, opponent_1, opponent_2, opponent_3, opponent_4, opponent_5, opponent_6, opponent_7]

    execute(participants, game_num=1, small_blind=1, num_of_members=2+add_op)

    game_num = 2

    while ai.bank > 0:
        execute(participants, game_num, small_blind=1, num_of_members=2+add_op)
        game_num += 1

    print(f'{participants[0].nick} проиграл, а вы всё еще в Игре')
