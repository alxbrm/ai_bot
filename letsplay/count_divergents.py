from engine import Player, Game, Opponent


def execute():
    ai = Player()

    ai.bank = 3000
    ai.limit = 3000

    op = Opponent()

    op.bank = 3000

    participants = [ai, op]

    kol = Game()

    kol.handout(1)

    pre_chance, _ = kol.make_round(participants)

    floop_chance, _ = kol.make_round(participants)

    turn_chance, _ = kol.make_round(participants)

    kol.make_round(participants)

    river_chance, gess = kol.make_round(participants)

    return gess, river_chance, turn_chance, floop_chance, pre_chance


# list_of_percents = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

list_of_percents = [0.5, 0.55, 0.85, 0.9]


def divergents_pre_count(list):
    for z in list:
        tests = 0
        tries = 0
        pre_successes = 0
        river_successes = 0

        while tests <= 1:
            gess, river_chance, turn_chance, floop_chance, pre_chance = execute()

            tries += 1
            print('GOING {} {}'.format(pre_chance, z))
            if z + 0.05 > pre_chance > z:
                if gess:
                    river_successes += 1
                    if river_chance > 0.5:
                        pre_successes += 1
                tests += 1

        with open('divergent-pre.txt', 'a', encoding='utf-8') as f:
            print('{}-{}-{}||||всего циклов - {}, случаи выпадения вероятности - {}, river_successes - {}'.format(z, z + 0.05, pre_successes/tests, tries, tests, river_successes), file=f)

    with open('divergent-pre.txt', 'a', encoding='utf-8') as f:
        print('---------------------------------------------------\n'
              '---------------------------------------------------', file=f)


def divergents_floop_count(list):
    for z in list:
        tests = 0
        tries = 0
        floop_successes = 0
        river_successes = 0

        while tests <= 1000:
            gess, river_chance, turn_chance, floop_chance, pre_chance = execute()

            tries += 1

            if z + 0.05 > floop_chance > z:
                if gess:
                    river_successes += 1
                    if river_chance > 0.5:
                        floop_successes += 1
                tests += 1

        with open('divergent-floop.txt', 'a', encoding='utf-8') as f:
            print('{}-{}-{}||||всего циклов - {}, случаи выпадения вероятности - {}, river_successes - {}'.format(z, z + 0.05, floop_successes/tests, tries, tests, river_successes), file=f)

    with open('divergent-floop.txt', 'a', encoding='utf-8') as f:
        print('---------------------------------------------------\n'
              '---------------------------------------------------', file=f)


def divergents_turn_count(list, tests=0, turn_successes=0, river_successes=0):
    for z in list:
        tests = 0
        tries = 0
        turn_successes = 0
        river_successes = 0

        while tests <= 1000:
            gess, river_chance, turn_chance, floop_chance, pre_chance = execute()

            tries += 1

            if z + 0.05 > turn_chance > z:
                if gess:
                    river_successes += 1
                    if river_chance > 0.5:
                        turn_successes += 1
                        # if floop_chance > 0.5:
                        #     floop_successes += 1
                tests += 1

        with open('divergent-turn.txt', 'a', encoding='utf-8') as f:
            print('{}-{}-{}||||всего циклов - {}, случаи выпадения вероятности - {}, river_successes - {} '.format(z, z + 0.05, turn_successes/tests, tries, tests, river_successes), file=f)

    with open('divergent-turn.txt', 'a', encoding='utf-8') as f:
        print('---------------------------------------------------\n'
              '---------------------------------------------------', file=f)


def divergents_river_count(list, tests=0, river_successes=0):
    for z in list:
        tests = 0
        tries = 0
        river_successes = 0

        while tests <= 10000:
            gess, river_chance, turn_chance, floop_chance, pre_chance = execute()

            tries += 1

            if z + 0.05 >= river_chance > z:
                if gess:
                    river_successes += 1

                tests += 1

        with open('divergent-river.txt', 'a', encoding='utf-8') as f:
            print('{}-{}-{}||||всего циклов - {}, случаи выпадения вероятности - {}, river_successes - {}'.format(z, z + 0.05, river_successes/tests, tries, tests, river_successes), file=f)

    with open('divergent-river.txt', 'a', encoding='utf-8') as f:
        print('---------------------------------------------------\n'
              '---------------------------------------------------', file=f)


divergents_pre_count(list_of_percents)
