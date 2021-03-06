import random, copy
from functools import reduce
from combinations import suits, row, variations_of_streets, take_card_from_pool, counter, convert_to_point, quantity_combinations
from combinations import create_maps, elder_card, pair, two_pairs, sat, street, flash, full_house, kare, street_flash, results_count, find_out_the_strongest_possibilities
from chances import rangs, pre_chance_point, floop_chance_point, turn_chance_point, op_floop_chance, op_river_chance, correct_win_chance, divide, ch_cor
from decisions import basic_decision, player_makes_bet

rang_points = [147, 1200/(1/1.28), 1200/(1/3.26), 1200/(1/19.7), 1200/(1/20.6), 1200/(1/32.1), 1200/(1/37.5),
               1200/(1/594), 1200/(1/3589.6)]
hands = ['ElderCard', 'Pair', 'TwoPairs', 'Set', 'Street', 'Flash', 'FullHouse', 'Kare', 'StreetFlash']


class Player:
    def __init__(self, bank=0):
        self.bank = bank
        self.suit_maps, self.map_of_cards, self.map_of_values = [], [], []
        self.op_suit_maps, self.op_map_of_cards, self.op_map_of_values = [], [], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pool_suit_maps, self.pool_map_of_cards, self.pool_map_of_values = [], [], []
        self.win_chance = 0
        self.local_win_chance = 0
        self.op_count = 0
        self.round = 0
        self.pool = []
        self.ways_of_my_1c_s = 0
        self.ways_of_my_1c_fs = 0
        self.i_have_pair_on_prefloop = False
        self.in_game = True
        self.bet = 0
        self.rise = 0
        self.limit = bank
        self.available_cash = 0
        self.nick = 'ПокерБот'
        self.place_in_queue = 0
        self.map_of_player = []

    def calculate_chances_and_points(self):

        # print(self.map_of_cards, self.map_of_values)

        my_points = results_count(self.suit_maps, self.map_of_cards, self.map_of_values, False)
        my_max_points = max(my_points)

        op_points = results_count(self.op_suit_maps, self.op_map_of_cards, self.op_map_of_values, False)
        op_max_points = max(op_points)

        my_virt_points = [0]

        values = {'map_of_values': self.map_of_values, 'op_map_of_values': self.op_map_of_values,
                  'pool_map_of_values': self.pool_map_of_values, 'map_of_player': self.map_of_player,
                  'pool_from_ppv': self.pool, 'op_count': self.op_count, 'round': self.round}

        if self.round == 0:
            my_virt_points = pre_chance_point(self.pool, self.map_of_values, self.suit_maps, my_max_points)

            self.map_of_player = copy.copy(self.map_of_values)
            values['map_of_player'] = self.map_of_player

            if my_max_points > rangs['Pair']:
                self.i_have_pair_on_prefloop = True
            else:
                self.i_have_pair_on_prefloop = False

            if not self.i_have_pair_on_prefloop:
                if self.op_count > 2:
                    self.op_count = 2

            op_chances_on_pre = [1, ch_cor(0.514285, self.op_count), ch_cor(0.0504201, self.op_count),
                                 ch_cor(0.0218487, self.op_count), ch_cor(0.0039246, self.op_count),
                                 ch_cor(0.0019654, self.op_count), ch_cor(0.00144057, self.op_count),
                                 ch_cor(0.000240096, self.op_count), ch_cor(0.00001539077, self.op_count)]

            op_virt_points = list(map(lambda x, y: x * y, op_chances_on_pre, rang_points))

            maxis = find_out_the_strongest_possibilities(self.op_map_of_values)

            self.win_chance, self.local_win_chance = basic_decision(op_virt_points, my_virt_points, op_points,
                                                                    my_points, maxis, values)

            self.win_chance = correct_win_chance(self.win_chance, self.round, self.op_count)

            if self.win_chance < 0:
                self.win_chance = 0

        elif self.round == 1:

            my_virt_points = floop_chance_point(self.pool, self.map_of_values, self.suit_maps, self.map_of_cards, my_max_points)

            # print(my_virt_points)
            # print('количество оппонентов {}'.format(self.op_count))

            self.ways_of_my_1c_s = my_virt_points[9]
            self.ways_of_my_1c_fs = my_virt_points[10]

            op_virt_points = op_floop_chance(self.op_suit_maps, self.op_map_of_cards,
                                             self.op_map_of_values, self.map_of_values, self.pool_suit_maps,
                                             self.pool_map_of_values, self.pool, self.ways_of_my_1c_s, self.ways_of_my_1c_fs,
                                             op_max_points, self.i_have_pair_on_prefloop, self.op_count)

            maxis = find_out_the_strongest_possibilities(self.op_map_of_values)
            self.win_chance, self.local_win_chance = basic_decision(op_virt_points, my_virt_points, op_points, my_points, maxis, values)
            self.win_chance = correct_win_chance(self.win_chance, self.round, self.op_count)

            if self.win_chance < 0:
                self.win_chance = 0

        elif self.round == 2:
            my_virt_points = turn_chance_point(self.pool, self.map_of_values, self.suit_maps, self.map_of_cards, my_max_points)
            self.ways_of_my_1c_s = my_virt_points[9]
            self.ways_of_my_1c_fs = my_virt_points[10]

            op_virt_points = op_floop_chance(self.op_suit_maps, self.op_map_of_cards,
                                             self.op_map_of_values, self.map_of_values, self.pool_suit_maps,
                                             self.pool_map_of_values, self.pool, self.ways_of_my_1c_s, self.ways_of_my_1c_fs,
                                             op_max_points, self.i_have_pair_on_prefloop, self.op_count)

            maxis = find_out_the_strongest_possibilities(self.op_map_of_values)
            self.win_chance, self.local_win_chance = basic_decision(op_virt_points, my_virt_points, op_points, my_points, maxis, values)
            self.win_chance = correct_win_chance(self.win_chance, self.round, self.op_count)

            if self.win_chance < 0:
                self.win_chance = 0

        elif self.round == 3:
            my_virt_points = [0, 0, 0, 0, 0, 0, 0, 0, 0]

            op_virt_points = op_river_chance(self.op_suit_maps, self.op_map_of_cards,
                                             self.op_map_of_values, self.map_of_values, self.pool_suit_maps,
                                             self.pool_map_of_values, self.pool, self.ways_of_my_1c_s, self.ways_of_my_1c_fs,
                                             op_max_points, self.i_have_pair_on_prefloop, self.op_count)

            maxis = find_out_the_strongest_possibilities(self.op_map_of_values)

            self.win_chance, self.local_win_chance = basic_decision(op_virt_points, my_virt_points, op_points, my_points, maxis, values)

            self.win_chance = correct_win_chance(self.win_chance, self.round, self.op_count)

            if self.win_chance < 0:
                self.win_chance = 0

        else:
            pass

        return self.win_chance, max(my_virt_points)


class Opponent:
    def __init__(self, bank=0, nick='Оппонент', auto_bet=True):
        self.bank = bank
        self.available_cash = 0
        self.suit_maps, self.map_of_cards, self.map_of_values = [], [], []
        self.bet = 0
        self.rise = 0
        self.nick = nick
        self.auto_bet = auto_bet
        self.in_game = True
        self.blef_rank = 0


class Game:
    def __init__(self, game_num=1, small_blind=10, test_mode=False):
        self.ch = list((suits[0]+i for i in row))
        self.tr = list((suits[1]+i for i in row))
        self.bu = list((suits[2]+i for i in row))
        self.pi = list((suits[3]+i for i in row))
        self.pool = self.bu+self.tr+self.ch+self.pi
        # имеющийся пул с точки зрения игрока

        self.test_mode = test_mode
        self.round = 0
        self.stage = 1
        self.small_blind = small_blind
        self.maps = []
        self.op_maps = []
        self.map_of_pool_cards = []
        self.op_count = 1
        self.player_win_chance = 0
        self.opponent_win_chance = 0
        self.gess_or_not = None
        self.bets = [0, 0, 0, 0, 0, 0, 0, 0]
        self.refusals = 0
        self.stop_this_game = False
        self.game_num = game_num
        self.winners = []

        random.shuffle(self.pool)

    def handout(self, comp_players=1):
        self.player_cards = take_card_from_pool(self.pool, 2, test_mode=self.test_mode)
        self.cards_of_players = [self.player_cards]
        self.op_count = comp_players
        self.pool_from_popv = copy.copy(self.pool)

        for c_players in range(comp_players):
            self.cards_of_players.append(take_card_from_pool(self.pool, 2))

        return self.cards_of_players

    def make_round(self, participants):

        player = participants[0]
        player.small_blind = self.small_blind
        members = len(participants)

        blef_divergent = 1.235

        def make_bet(queue, stage=1, this_is_preflop=False):
            p_place_in_queue = 0

            cou = 0

            if stage == 1:

                print('------------------------------------\nИдёт {} фаза торгов\n'.format(stage))

                for i in queue:

                    if i != 0:
                        trigger_opponent(i, 0, True)
                        cou += 1
                    else:
                        trigger_player(0, True)
                        p_place_in_queue = cou

            else:

                print('------------------------------------\nИдёт {} фаза торгов\n'.format(stage))

                for index, i in enumerate(queue):

                    if i != 0:

                        if participants[i].bet != 0 and participants[i].bet < max(self.bets) and participants[i].bank > 0:

                            cou += 1

                            if stage == 2:
                                trigger_opponent(i, 0, True)

                            elif stage == 3:
                                trigger_opponent(i, 0, True, True)

                        else:

                            if index == 1:
                                if this_is_preflop and stage == 2:

                                    trigger_opponent(i, 0, True)

                                    if participants[i].rise == 0 and participants[i].bet == max(self.bets):
                                        break

                    else:

                        p_place_in_queue = cou

                        if player.bet != 0 and player.bet < max(self.bets) and player.bank > 0:
                            if stage == 2:
                                trigger_player(i, True)
                            elif stage == 3:
                                trigger_player(i, True, True)

                        else:
                            if index == 1:
                                if this_is_preflop and stage == 2:

                                    trigger_player(i, True)

                                    if participants[i].rise == 0 and participants[i].bet == max(self.bets):
                                        break

            return p_place_in_queue

        def implement_blindes_and_bets(small_blind, round=0):
            prize = 0
            list_of_winners = []
            current_bets = self.bets

            this_is_preflop = False

            queue = list(i for i in range(members))

            stop_this_game = False

            for _ in range(self.game_num):
                last_member = queue.pop()
                queue.insert(0, last_member)

            # print('Очередь игроков внутри implement {}'.format(queue))

            # надо допилить возможность делать ставки в первом раунде бигблайнду как заключительную ставку
            if round == 0:

                this_is_preflop = True

                print('\nСтавки делают Small Blind и Big Blind\n')

                if queue[0] == 0:
                    trigger_player(small_blind)
                    trigger_opponent(queue[1], small_blind*2)
                    for i in queue[2:members]:
                        trigger_opponent(i, 0, True)
                elif queue[1] == 0:
                    trigger_opponent(queue[0], small_blind)
                    trigger_player(small_blind*2)
                    for i in queue[2:members]:
                        trigger_opponent(i, 0, True)
                else:
                    trigger_opponent(queue[0], small_blind)
                    trigger_opponent(queue[1], small_blind * 2)
                    for i in queue[2:members]:
                        if i != 0:
                            trigger_opponent(i, 0, True)
                        else:
                            trigger_player(0, True)

                self.op_count = len(self.bets) - self.bets.count(0) - 1

            elif round == 1 or round == 2 or round == 3:

                if current_bets[:members].count(0) < (members - 1):
                    player.place_in_queue = make_bet(queue)

                self.op_count = len(self.bets) - self.bets.count(0) - 1

            elif round == 4:

                prize = reduce(lambda x, y: x + y, current_bets) + self.refusals

                list_of_ppoints = [0, 0, 0, 0, 0, 0, 0, 0]

                for i, m in enumerate(self.cards_of_players):
                    a = create_maps(m + self.floop + self.turn + self.river)
                    if i < len(participants):
                        if participants[i].bet != 0:
                            list_of_ppoints[i] = max(results_count(*a, False))
                        else:
                            list_of_ppoints[i] = 0

                num_of_winners = list_of_ppoints.count(max(list_of_ppoints))

                start = 0

                integral_won = 0

                for _ in range(num_of_winners):
                    if num_of_winners > 1:

                        try:
                            ind = list_of_ppoints.index(max(list_of_ppoints), start)

                            won = int((participants[ind].bet / max(current_bets)) * prize // num_of_winners)

                            participants[ind].bank += won

                            list_of_winners.append(participants[ind])

                            integral_won += won

                            print('В этой игре выигрыш в размере ${} забирает {}'.format(won, participants[ind].nick))

                            start += ind + 1
                        except ValueError:
                            pass

                    else:

                        ind = list_of_ppoints.index(max(list_of_ppoints), start)

                        won = 0
                        for i, bet in enumerate(current_bets[:len(participants)]):
                            if bet <= participants[ind].bet:
                                participants[ind].bank += bet
                                won += bet
                            else:
                                participants[ind].bank += participants[ind].bet
                                won += participants[ind].bet
                                participants[i].bank += bet - participants[ind].bet

                        if divide(self.refusals, current_bets[:members].count(0)) <= participants[ind].bet:
                            participants[ind].bank += self.refusals
                            won += self.refusals
                            integral_won = prize
                        else:
                            participants[ind].bank += participants[ind].bet * current_bets[:members].count(0)
                            won += participants[ind].bet * current_bets[:members].count(0)

                            integral_won = prize - (self.refusals -
                                                    participants[ind].bet * current_bets[:members].count(0))

                        list_of_winners.append(participants[ind])

                        print('В этой игре выигрыш в размере {} забирает {}'.format(won, participants[ind].nick))

                side_bank = prize - integral_won

                if side_bank > 0:
                    to_del = list_of_ppoints.index(max(list_of_ppoints))
                    list_of_ppoints[to_del] = 0

                    ind = list_of_ppoints.index(max(list_of_ppoints))

                    won = side_bank

                    list_of_winners.append(participants[ind])

                    participants[ind].bank += won

                    print('В этой игре побочный банк в размере {} забирает {}'.format(won, participants[ind].nick))

            if round != 4:
                if current_bets[:members].count(0) < (members - 1)\
                        and (current_bets[:members].count(0) + current_bets[:members].count(max(self.bets))) != members:

                    self.stage = 2

                    make_bet(queue, stage=self.stage, this_is_preflop=this_is_preflop)

                    self.op_count = len(self.bets) - self.bets.count(0) - 1

                else:
                    print('Все игроки выровняли ставки или скниули свои карты (кроме победителя)')

                if current_bets[:members].count(0) < (members - 1) \
                        and (current_bets[:members].count(0) + current_bets[:members].count(max(self.bets))) != members:

                    self.stage = 3
                    make_bet(queue, stage=self.stage)

                    self.op_count = len(self.bets) - self.bets.count(0) - 1

                else:
                    print('Все игроки выровняли ставки или скниули свои карты (кроме победителя)')

            # проверяем не скинули ли все игроки карты
                if current_bets[:members].count(0) == (members - 1):
                    prize = reduce(lambda x, y: x + y, current_bets) + self.refusals

                    for i, bet in enumerate(current_bets[:members]):
                        if bet != 0:
                            participants[i].bank += prize

                            print('В этой игре весь банк забирает {}'.format(participants[i].nick))

                            list_of_winners.append(participants[i])

                            participants[i].bet = 0

                            stop_this_game = True

            self.op_count = len(self.bets) - self.bets.count(0) - 1

            return stop_this_game, list_of_winners, prize

        def trigger_opponent(num_of_op=1, obligation=0, do_bet=False, cieling_of_bet=False):
            opponent = participants[num_of_op]
            auto_bet = opponent.auto_bet

            opponent.suit_maps, opponent.map_of_cards, opponent.map_of_values = \
                create_maps(self.cards_of_players[num_of_op])

            if obligation > opponent.bank:
                obligation = opponent.bank

            opponent.bet += obligation

            if not do_bet and opponent.in_game:
                opponent.bank -= opponent.bet
                self.bets[num_of_op] = opponent.bet

                print('МАКСИМАЛЬНАЯ СТАВКА ${}\n'.format(max(self.bets)))
                if num_of_op == 1:
                    print('ВАША ТЕКУЩАЯ СТАВКА ${}. ВАШ БАНК ${}.ВАШИ КАРТЫ:\n{}\n'.format(opponent.bet, opponent.bank,
                                                                                     opponent.map_of_cards))

                print('--ИНФОРМАЦИЯ ОТ ДИЛЕРА--')

                for i in participants:
                    lack = max(self.bets) - i.bet
                    print('{} - СТАВКА ${}, ОСТАТОК СРЕДСТВ ${}, ДЛЯ КОЛА ${} || ДОСТУПНЫЙ КЭШ {}'.format(i.nick, i.bet,
                                                                                                          i.bank, lack,
                                                                                                          i.available_cash))

            elif do_bet and opponent.in_game:

                print('\nМАКСИМАЛЬНАЯ СТАВКА ${}\n'.format(max(self.bets)))
                if num_of_op == 1:
                    print('\nВАША ТЕКУЩАЯ СТАВКА ${}. ВАШ БАНК ${}.ВАШИ КАРТЫ:\n{}\n'.format(opponent.bet, opponent.bank,
                                                                                     opponent.map_of_cards))

                print('--ИНФОРМАЦИЯ ОТ ДИЛЕРА--')

                for i in participants:
                    lack = max(self.bets)-i.bet
                    if lack > i.bank:
                        lack = i.bank
                    print('{} - СТАВКА ${}, ОСТАТОК СРЕДСТВ ${}, ДЛЯ КОЛА ${} || ДОСТУПНЫЙ КЭШ {}'.format(i.nick, i.bet, i.bank, lack, i.available_cash))

                if self.bets[:members].count(0) < (members - 1) and opponent.bank > 0:
                    if auto_bet:
                        if self.test_mode:
                            if self.round == 0 or self.round == 1 or self.round == 2:
                                action = opponent.bank
                            else:
                                action = opponent.bank
                        else:
                            if self.round == 0:
                                action = int(random.randint(-1, 2) * opponent.bank / random.randint(8, 16))
                            elif self.round == 1:
                                action = int(random.randint(0, 3) * opponent.bank / random.randint(5, 12))
                            elif self.round == 2:
                                action = int(random.randint(1, 4) * opponent.bank / random.randint(3, 8))
                            else:
                                action = int(random.randint(2, 5) * opponent.bank / random.randint(3, 8))
                    else:
                        try:
                            action = int(input('\nВыберите действие: колировать - введите 0, повысить - введите значение, пассовать - -1:\n'))
                        except ValueError:
                            action = 0

                else:
                    action = 0

                if cieling_of_bet and action > 0:
                    print('3-й круг ставок, повышение более невозможно. Call')
                    action = 0

                if action > 0:
                    self.rise = ((max(self.bets) - opponent.bet) + action)
                    opponent.bank -= self.rise
                    if opponent.bank < 0:
                        opponent.bank += self.rise
                        opponent.bet += opponent.bank
                        self.bets[num_of_op] = opponent.bet
                        opponent.bank = 0

                        if not auto_bet:
                            print('Ваша ставка превышает баланс, вы идете all-in, ваша ставка {}, '
                                  'остаток средств {}'.format(opponent.bet, opponent.bank))
                    else:
                        opponent.bet += self.rise
                        self.bets[num_of_op] = opponent.bet

                        if not auto_bet:
                            print('Ваша ставка {}, остаток средств {}'.format(opponent.bet, opponent.bank))

                elif action < 0:
                    self.refusals += opponent.bet
                    opponent.bet = 0
                    self.bets[num_of_op] = opponent.bet
                    opponent.in_game = False

                else:
                    self.rise = (max(self.bets) - opponent.bet)

                    if not auto_bet:
                        print('Вы повысили ставку на {}'.format(self.rise))

                    opponent.bank -= self.rise
                    if opponent.bank < 0:
                        opponent.bank += self.rise
                        opponent.bet += opponent.bank
                        self.bets[num_of_op] = opponent.bet
                        opponent.bank = 0

                        if not auto_bet:
                            print('Ваша ставка превышает баланс, вы идете all-in, ваша ставка {}, '
                                  'остаток средств {}'.format(opponent.bet, opponent.bank))
                    else:
                        opponent.bet += self.rise
                        self.bets[num_of_op] = opponent.bet

                        if not auto_bet:
                            print('Ваша ставка {}, остаток средств {}'.format(opponent.bet, opponent.bank))

            else:
                opponent.bet = 0

            return opponent.bet

        def trigger_player(obligation=0, do_bet=False, cieling_of_bet=False):
            player.suit_maps, player.map_of_cards, player.map_of_values = self.maps
            player.op_suit_maps, player.op_map_of_cards, player.op_map_of_values = self.op_maps
            player.pool_suit_maps, player.pool_map_of_cards, player.pool_map_of_values = self.map_of_pool_cards

            player.round = self.round

            player.pool = self.pool_from_popv

            player.op_count = self.op_count

            self.player_win_chance = player.calculate_chances_and_points()[0]

            player.win_chance = self.player_win_chance

            if obligation > player.bank:
                obligation = player.bank

            if not do_bet and player.in_game:

                player.bank -= obligation

                player.bet += obligation

                self.bets[0] = player.bet

            elif do_bet and player.in_game:

                for i, bet in enumerate(self.bets):
                    op_win_chance = (1 - self.player_win_chance) / self.op_count

                    if bet == max(self.bets) and i != 0:

                        if bet / (participants[i].bank + bet) > (op_win_chance**2) * blef_divergent:
                            participants[i].blef_rank += 1

                        else:
                            participants[i].blef_rank -= 0.1
                            if participants[i].blef_rank < 0:
                                participants[i].blef_rank = 0

                self.rise, needed = player_makes_bet(participants, self.bets, limit=player.limit)
                player.bank -= self.rise
                player.bet += self.rise

                if self.rise < needed:

                    if int(player.bank) > 0:
                        player.bank += self.rise
                        player.bet -= self.rise
                        self.refusals += player.bet
                        player.bet = 0
                        self.bets[0] = player.bet
                        player.in_game = False

                        print(f'\n\n{player.nick} скинул свои карты\n\n')

                    else:
                        self.bets[0] = player.bet
                        player.bank = 0
                        print(f'{player.nick} идет ALL-INN\n\n')

                else:
                    if cieling_of_bet:
                        player.bank += self.rise
                        player.bet -= self.rise
                        self.rise = needed
                        player.bank -= self.rise
                        player.bet += self.rise
                        self.bets[0] = player.bet

                    else:
                        self.bets[0] = player.bet

            else:
                player.bet = 0

            return player.bet

        if self.round == 0:

            print('ПРЕФЛОП ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ПРЕФЛОП\n')

            self.maps = create_maps(self.player_cards)
            self.op_maps = [], [], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.map_of_pool_cards = create_maps(self.pool_from_popv)

            self.stop_this_game, self.winners, prize = implement_blindes_and_bets(self.small_blind, self.round)

        elif self.round == 1 and not self.stop_this_game:

            print('ФЛОП ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ФЛОП\n')

            self.floop = take_card_from_pool(self.pool, 3)
            # имеющийся пул с точки зрения игрока
            self.pool_from_popv = list(set(self.pool_from_popv) - set(self.floop))

            self.maps = create_maps(self.player_cards + self.floop)
            self.op_maps = create_maps(self.floop)
            self.map_of_pool_cards = create_maps(self.pool_from_popv)

            print('ВСКРЫТЫй ФЛОП:\n{}'.format(self.op_maps[1]))

            self.stop_this_game, self.winners, prize = implement_blindes_and_bets(self.small_blind, self.round)

        elif self.round == 2 and not self.stop_this_game:

            print('ТЁРН ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ТЁРН\n')

            self.turn = take_card_from_pool(self.pool)
            self.pool_from_popv = list(set(self.pool_from_popv) - set(self.turn))

            self.maps = create_maps(self.player_cards + self.floop + self.turn)
            self.op_maps = create_maps(self.floop + self.turn)
            self.map_of_pool_cards = create_maps(self.pool_from_popv)

            print('ВСКРЫТЫй ТЁРН:\n{}'.format(self.op_maps[1]))

            self.stop_this_game, self.winners, prize = implement_blindes_and_bets(self.small_blind, self.round)

        elif self.round == 3 and not self.stop_this_game:

            print('РИВЕР ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| РИВЕР\n')

            self.river = take_card_from_pool(self.pool)
            self.pool_from_popv = list(set(self.pool_from_popv) - set(self.river))

            self.maps = create_maps(self.player_cards + self.floop + self.turn + self.river)
            self.op_maps = create_maps(self.floop + self.turn + self.river)
            self.map_of_pool_cards = create_maps(self.pool_from_popv)

            print('ВСКРЫТЫй РИВЕР:\n{}'.format(self.op_maps[1]))

            self.stop_this_game, self.winners, prize = implement_blindes_and_bets(self.small_blind, self.round)

        elif self.round == 4 and not self.stop_this_game:

            print('\nИТОГИ ИГРЫ №{} ПОСЛЕ ВСКРЫТИЯ:\n'.format(self.game_num))
            print('ВСКРЫТЫЙ РИВЕР:\n{}'.format(self.op_maps[1]))

            for ind, i in enumerate(self.cards_of_players):
                if ind < len(participants):
                    if participants[ind].bet != 0:
                        all_members_maps = create_maps(i + self.floop + self.turn + self.river)
                        points = max(results_count(*all_members_maps, False))

                        hand = hands[0]

                        for t, p in enumerate(rang_points[:-1]):
                            if p < points < rang_points[t+1]:
                                hand = hands[t]
                                break

                        print('У Игрока {} рука {} --> {}. Всего очков '
                              '{}\n'.format(participants[ind].nick, participants[ind].map_of_cards[:2], hand, points))

            _, self.winners, prize = implement_blindes_and_bets(self.small_blind, self.round)

            print('Победитель {}\n'.format(self.winners[0].nick))
            print('Общий выигрыш ${}'.format(prize))

            for member in participants:
                member.bet = 0

        self.round += 1

        return self.player_win_chance, self.gess_or_not
