from engine import Player, Game, Opponent


def fill_banks_of_members(participants, num_of_members):
    elements = len(participants)
    for i, amo in enumerate(participants):
        if i <= num_of_members:
            amo.bank = 1000

    while elements > num_of_members:
        participants.pop()
        elements -= 1

    return participants


def check_banks(participants):
    for i, amo in enumerate(participants):
        if amo.bank == 0:
            participants.pop(i)


def execute(participants, game_num, small_blind, num_of_members):

    print('Начало игры №{}\n'.format(game_num))

    if game_num == 1:
        fill_banks_of_members(participants, num_of_members)

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
        exit()

    return kol.game_num


ai = Player()

opponent_1 = Opponent(nick='Сенсей')
opponent_2 = Opponent(nick='Гарри Поттер')
opponent_3 = Opponent(nick='Терминатор')
opponent_4 = Opponent()
opponent_5 = Opponent()
opponent_6 = Opponent()
opponent_7 = Opponent()

participants = [ai, opponent_1, opponent_2, opponent_3, opponent_4, opponent_5, opponent_6, opponent_7]

execute(participants, game_num=1, small_blind=10, num_of_members=2)

game_num = 2

while ai.bank > 0:
    if input('\n\nИграем игру? y/n\n\n') != 'n':
        execute(participants, game_num, small_blind=10, num_of_members=2)
        game_num += 1
    else:
        exit()
