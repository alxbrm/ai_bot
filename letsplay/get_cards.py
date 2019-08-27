import random, copy
from functools import reduce
from combinations import suits, row, variations_of_streets, take_card_from_pool, counter, convert_to_point, quantity_combinations
from combinations import create_maps, elder_card, pair, two_pairs, sat, street, flash, full_house, kare, street_flash, results_count, find_out_the_strongest_possibilities
from chances import rangs, pre_chance_point, floop_chance_point, turn_chance_point, op_floop_chance, op_river_chance, correct_win_chance, divide, ch_cor, divide_by_zero
from decisions import basic_decision, player_makes_bet

rang_points = [147, 1200/(1/1.28), 1200/(1/3.26), 1200/(1/19.7), 1200/(1/20.6), 1200/(1/32.1), 1200/(1/37.5),
     1200/(1/594), 1200/(1/3589.6)]


class Player():
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
        self.bet = 0
        self.rise = 0
        self.limit = 0
        self.small_blind = 0
        self.blef_rises = 0
        self.nick = 'Мистер Путин'
        self.place_in_queue = 0
        self.map_of_player = []

    def calculate_chances_and_points(self):

        # print(self.map_of_cards, self.map_of_values)

        my_points = results_count(self.suit_maps, self.map_of_cards, self.map_of_values, False)
        my_max_points = max(my_points)

        op_points = results_count(self.op_suit_maps, self.op_map_of_cards, self.op_map_of_values, False)
        op_max_points = max(op_points)

        my_virt_points = [0]

        # if not self.i_have_pair_on_prefloop:
        #     op_chances_on_pre = [1, ch_cor(0.514285, self.op_count), ch_cor(0.0504201, self.op_count),
        #                          ch_cor(0.0218487, self.op_count), ch_cor(0.0039246, self.op_count),
        #                          ch_cor(0.0019654, self.op_count), ch_cor(0.00144057, self.op_count),
        #                          ch_cor(0.000240096, self.op_count), ch_cor(0.00001539077, self.op_count)]
        # else:
        #     op_chances_on_pre = [1, ch_cor(0.514285, self.op_count), ch_cor(0.0504201, self.op_count),
        #                          ch_cor(0.0218487, self.op_count), ch_cor(0.0039246, self.op_count),
        #                          ch_cor(0.0019654, self.op_count), ch_cor(0.00144057, self.op_count),
        #                          ch_cor(0.000240096, self.op_count), ch_cor(0.00001539077, self.op_count)]

        values = {'map_of_values': self.map_of_values, 'op_map_of_values': self.op_map_of_values,
                  'pool_map_of_values': self.pool_map_of_values, 'map_of_player': self.map_of_player,
                  'pool_from_ppv': self.pool, 'op_count': self.op_count, 'round': self.round, }

        if self.round == 0:
            my_virt_points = pre_chance_point(self.pool, self.map_of_values, self.suit_maps, my_max_points)

            self.map_of_player = copy.copy(self.map_of_values)
            values['map_of_player'] = self.map_of_player
            # print(my_virt_points)

            if my_max_points > rangs['Pair']:
                self.i_have_pair_on_prefloop = True
                print('\n\nУ НАС ПАРА НА ПРЕФЛОПЕ\n\n')
            else:
                self.i_have_pair_on_prefloop = False
                print('\n\nИДЁМ ПО СТАРШЕЙ КАРТЕ\n\n')

            if not self.i_have_pair_on_prefloop:
                if self.op_count > 2:
                    self.op_count = 2
                    print('get_card/Искусственно учитываем только 2х противников ИИ, на самом деле их больше 2х')

            op_chances_on_pre = [1, ch_cor(0.514285, self.op_count), ch_cor(0.0504201, self.op_count),
                                 ch_cor(0.0218487, self.op_count), ch_cor(0.0039246, self.op_count),
                                 ch_cor(0.0019654, self.op_count), ch_cor(0.00144057, self.op_count),
                                 ch_cor(0.000240096, self.op_count), ch_cor(0.00001539077, self.op_count)]

            op_virt_points = list(map(lambda x, y: x * y, op_chances_on_pre, rang_points))

            maxis = find_out_the_strongest_possibilities(self.op_map_of_values)

            self.win_chance, self.local_win_chance = basic_decision(op_virt_points, my_virt_points, op_points, my_points, maxis, values)

            # print('Шанс выигрыша ИИ {} %'.format(self.win_chance * 100))

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
            # print(maxis)

            self.win_chance, self.local_win_chance = basic_decision(op_virt_points, my_virt_points, op_points, my_points, maxis, values)

            # print(self.op_map_of_cards)
            # print('Шанс выигрыша ИИ {} %'.format(self.win_chance * 100))

            self.win_chance = correct_win_chance(self.win_chance, self.round, self.op_count)
            # print('Скорректированный Шанс выигрыша ИИ {} %'.format(self.win_chance * 100))

            if self.win_chance < 0:
                self.win_chance = 0

        elif self.round == 2:
            my_virt_points = turn_chance_point(self.pool, self.map_of_values, self.suit_maps, self.map_of_cards, my_max_points)

            # print(my_virt_points)

            self.ways_of_my_1c_s = my_virt_points[9]
            self.ways_of_my_1c_fs = my_virt_points[10]

            op_virt_points = op_floop_chance(self.op_suit_maps, self.op_map_of_cards,
                                             self.op_map_of_values, self.map_of_values, self.pool_suit_maps,
                                             self.pool_map_of_values, self.pool, self.ways_of_my_1c_s, self.ways_of_my_1c_fs,
                                             op_max_points, self.i_have_pair_on_prefloop, self.op_count)

            maxis = find_out_the_strongest_possibilities(self.op_map_of_values)
            # print(maxis)

            self.win_chance, self.local_win_chance = basic_decision(op_virt_points, my_virt_points, op_points, my_points, maxis, values)

            # print('Шанс выигрыша ИИ {} %'.format(self.win_chance * 100))

            self.win_chance = correct_win_chance(self.win_chance, self.round, self.op_count)
            # print('Скорректированный Шанс выигрыша ИИ {} %'.format(self.win_chance * 100))

            if self.win_chance < 0:
                self.win_chance = 0

        elif self.round == 3:
            my_virt_points = [0, 0, 0, 0, 0, 0, 0, 0, 0]

            op_virt_points = op_river_chance(self.op_suit_maps, self.op_map_of_cards,
                                             self.op_map_of_values, self.map_of_values, self.pool_suit_maps,
                                             self.pool_map_of_values, self.pool, self.ways_of_my_1c_s, self.ways_of_my_1c_fs,
                                             op_max_points, self.i_have_pair_on_prefloop, self.op_count)

            maxis = find_out_the_strongest_possibilities(self.op_map_of_values)
            # print(maxis)

            self.win_chance, self.local_win_chance = basic_decision(op_virt_points, my_virt_points, op_points, my_points, maxis, values)

            # print('\n{} - виртуальные очки оппонента\n{} - виртуальные очки игрока\n {} - очки оппонента\n {} - очки игрока'.format(op_virt_points, my_virt_points, op_points, my_points))

            # print('Шанс выигрыша ИИ {} %'.format(self.win_chance * 100))

            self.win_chance = correct_win_chance(self.win_chance, self.round, self.op_count)

            # print('Скорректированный Шанс выигрыша ИИ {} %'.format(self.win_chance * 100))

            if self.win_chance < 0:
                self.win_chance = 0

        else:
            pass

        return self.win_chance, max(my_virt_points)


class Opponent():
    def __init__(self, nick='Оппонент', bank=0):
        self.bank = bank
        self.suit_maps, self.map_of_cards, self.map_of_values = [], [], []
        self.bet = 0
        self.rise = 0
        self.nick = nick

        self.blef_rank = 0


class Game():
    def __init__(self, game_num=1, small_blind=10):
        self.ch = list((suits[0]+i for i in row))
        self.tr = list((suits[1]+i for i in row))
        self.bu = list((suits[2]+i for i in row))
        self.pi = list((suits[3]+i for i in row))
        self.pool = self.bu+self.tr+self.ch+self.pi
        # имеющийся пул с точки зрения игрока

        self.round = 0
        self.stage = 1
        self.small_blind = small_blind
        self.maps = []
        self.op_maps = []
        self.map_of_pool_cards = []
        self.op_count = 1
        self.player_win_chance = 0
        self.opponent_win_chance = 0
        self.player_rise = 0
        self.gess_or_not = None
        self.bets = [0, 0, 0, 0, 0, 0, 0, 0]
        self.refusals = 0
        self.stop_betting = False
        self.end_of_game = False
        self.game_num = game_num
        self.winners = []
        self.p_place_in_queue = 0

        random.shuffle(self.pool)

    def get_cards_from_app(self, res_list_of_cards, cards):

        for card in cards:
            if card in self.pool:
                res_list_of_cards.append(card)
            else:
                print('Не смогли добавить карту {}'.format(card))

        return res_list_of_cards

    def handout(self, got_cards, p_position):

        self.player_cards = []
        self.p_place_in_queue = p_position

        self.get_cards_from_app(self.player_cards, got_cards)

        self.pool = list(i for i in self.pool if i not in self.player_cards)

        self.cards_of_players = [self.player_cards]
        self.pool_from_popv = copy.copy(self.pool)

        return self.cards_of_players

    def make_round(self, participants, raund, got_bets, got_banks, got_cards):

        player = participants[0]
        members = len(participants)
        print('Участники игры {}'.format(participants))
        print('Количество участников за столом {}'.format(members))
        player.place_in_queue = self.p_place_in_queue
        self.round = raund

        blef_divergent = 1.235

        def implement_blindes_and_bets():
            print('Количество участников за столом {}'.format(members))

            for i in range(1, members):
                trigger_opponent(i)

            print('Текущие ставки {}'.format(self.bets))

            if self.bets[0] != 0:
                self.op_count = len(self.bets) - self.bets.count(0) - 1
            else:
                self.op_count = len(self.bets) - self.bets.count(0)

            print('Количество оппонентов {}'.format(self.op_count))

            self.player_rise = trigger_player()

            print('Здесь работает алгоритм внесения ставки {}'.format(self.player_rise))

            return self.player_rise

        def trigger_opponent(num_of_op=1):

            opponent = participants[num_of_op]

            opponent.bet = got_bets[num_of_op]
            self.bets[num_of_op] = opponent.bet

            opponent.bank = got_banks[num_of_op]

            return opponent.bet

        def trigger_player():
            player.suit_maps, player.map_of_cards, player.map_of_values = self.maps
            player.op_suit_maps, player.op_map_of_cards, player.op_map_of_values = self.op_maps
            player.pool_suit_maps, player.pool_map_of_cards, player.pool_map_of_values = self.map_of_pool_cards

            player.round = self.round

            player.pool = self.pool_from_popv

            player.op_count = self.op_count
            player.small_blind = self.small_blind

            self.player_win_chance = player.calculate_chances_and_points()[0]
            self.bets[0] = got_bets[0]
            player.bet = got_bets[0]
            player.bank = got_banks[0]

            player.win_chance = self.player_win_chance

            for i, bet in enumerate(self.bets):

                op_win_chance = (1 - self.player_win_chance ** divide_by_zero(1, self.op_count))

                if bet == max(self.bets) and i != 0:

                    try:
                        if bet / (participants[i].bank + bet) > (op_win_chance**2) * blef_divergent:
                            participants[i].blef_rank += 1
                            print('Прибавили blef_rank. Общий ранг - {}'. format(participants[i].blef_rank))
                        else:
                            participants[i].blef_rank -= 0.1
                            if participants[i].blef_rank < 0:
                                participants[i].blef_rank = 0
                    except ZeroDivisionError:
                        pass

            player.rise, needed = player_makes_bet(participants, self.bets, limit=player.limit)

            print('Needed по расчетам в get_cards = {}'.format(needed))

            player.bank -= player.rise
            player.bet += player.rise

            if player.rise < needed:

                print('\n\nстр.562 Текущий банк ИИ {}\n\n'.format(player.bank))

                if int(player.bank) > 0:
                    player.bank += player.rise
                    player.bet -= player.rise
                    self.refusals += player.bet
                    player.bet = 0
                    self.bets[0] = player.bet

                    player.rise = 0
                    # кнопка пасс
                    self.stop_betting = True
                    print('\n\nИИ скинул свои карты\n\n')

                else:
                    self.bets[0] = player.bet
                    player.bank = 0
                    # кнопка алл-инн
                    self.stop_betting = True
                    print('ИИ идет ALL-INN\n\n')

            else:
                self.bets[0] = player.bet

            return player.rise

        if self.round == 0 and not self.stop_betting:

            print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\nИдёт нулевой раунд (префлоп)\n')

            self.maps = create_maps(self.player_cards)
            self.op_maps = [], [], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.map_of_pool_cards = create_maps(self.pool_from_popv)

            implement_blindes_and_bets()

        elif self.round == 1 and not self.stop_betting:

            print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\nИдёт первый раунд (флоп)\n')

            self.floop = []

            self.get_cards_from_app(self.floop, got_cards)

            self.pool_from_popv = list(set(self.pool_from_popv) - set(self.floop))

            self.maps = create_maps(self.player_cards + self.floop)
            self.op_maps = create_maps(self.floop)
            self.map_of_pool_cards = create_maps(self.pool_from_popv)

            print('ВСКРЫТЫй ФЛОП:\n{}'.format(self.op_maps[1]))

            implement_blindes_and_bets()

        elif self.round == 2 and not self.stop_betting:

            print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\nИдёт второй раунд (тёрн)\n')

            self.turn = []

            self.get_cards_from_app(self.turn, got_cards)

            self.pool_from_popv = list(set(self.pool_from_popv) - set(self.turn))

            self.maps = create_maps(self.player_cards + self.floop + self.turn)
            self.op_maps = create_maps(self.floop + self.turn)
            self.map_of_pool_cards = create_maps(self.pool_from_popv)

            print('ВСКРЫТЫй ТЁРН:\n{}'.format(self.op_maps[1]))

            implement_blindes_and_bets()

        elif self.round == 3 and not self.stop_betting:

            print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\nИдёт третий раунд (ривер)\n')

            self.river = []

            self.get_cards_from_app(self.river, got_cards)

            self.pool_from_popv = list(set(self.pool_from_popv) - set(self.river))

            self.maps = create_maps(self.player_cards + self.floop + self.turn + self.river)
            self.op_maps = create_maps(self.floop + self.turn + self.river)
            self.map_of_pool_cards = create_maps(self.pool_from_popv)

            print('ВСКРЫТЫй РИВЕР:\n{}'.format(self.op_maps[1]))

            implement_blindes_and_bets()

        else:
            pass

        return self.player_rise

    def show_results_of_ii(self, op_maps, my_maps, player_win_chance):
        op_p = max(results_count(*op_maps, False))
        print('В итоге очки оппонента {}'.format(op_p))
        my_p = max(results_count(*my_maps, False))
        print('В итоге очки игрока {}'.format(my_p))
        if (player_win_chance > 0.5 and my_p >= op_p) or (player_win_chance <= 0.5 and op_p > my_p):
            print('ИИ посчитал верно')
            return True
        else:
            print('ИИ ошибся')
            return False
