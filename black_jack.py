from random import shuffle
from time import sleep


class Cards:
    cards_value = ['двойка', 'тройка', 'четверка', 'пятерка',
                   'шестерка', 'семерка', 'восьмерка', 'девятка',
                   'десятка', 'валет', 'дама', 'король', 'туз']

    cards_suit = ['пик', 'черви', 'крести', 'буби']

    cards_number = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, [1, 11]]

    cards_s_v = []

    cards = {}

    def gen_cards_s_v(self):
        for i in self.cards_suit:
            for j in self.cards_value:
                self.cards_s_v.append(j + ' ' + i)

    def gen_cards(self):
        for i in range(2):
            self.cards_number += self.cards_number
        for i in range(len(self.cards_s_v)):
            self.cards[self.cards_s_v[i]] = self.cards_number[i]


class StartGame:
    def repeat_game(self):
        while True:
            user_answer = input('Играем?\nВведите "да" или "нет": ')
            if self.validation_user_answer(user_answer):
                if user_answer == 'да':
                    c = Cards()
                    c.cards_s_v = []
                    c.cards = {}
                    c.gen_cards_s_v()
                    c.gen_cards()
                    gp = GameProcesses(c.cards_s_v, c.cards, count=0, player_s_move=True, players_score_count=0,
                                       dealer_score_count=0)
                    gp.players_cards = []
                    gp.dealers_cards = []
                    gp.distribution_cards()
                else:
                    print('До свидания!')
                    break

    @staticmethod
    def validation_user_answer(answer):
        valid_user_answer = ['да', 'нет']
        return True if answer in valid_user_answer else False


class Player(StartGame):
    def __init__(self, cards_array, cards_dict, count=0, player_s_move=True, players_score_count=0):
        self.players_score_count = players_score_count
        self.player_s_move = player_s_move
        self.cards_dict = cards_dict
        self.count = count
        self.cards_array = cards_array

    players_cards = []

    def distribution_cards_to_player(self):
        if self.player_s_move:
            self.unpacking_cards(self.players_cards, self.players_cards_count())
            if self.player_move():
                self.players_cards.append(self.cards_array[0])
                del self.cards_array[0]
        elif self.player_s_move or self.players_score_count > 21:
            self.count += 1
        elif self.players_score_count == 21:
            self.count += 2
        else:
            self.count += 3

    def players_cards_count(self):
        aces = ['туз буби', 'туз пик', 'туз черви', 'туз крести']
        sum_players_cards = []
        for i in self.players_cards:
            if i in aces and sum(sum_players_cards) + 11 <= 21:
                sum_players_cards.append(self.cards_dict[i][1])
            elif i in aces and sum(sum_players_cards) + 11 > 21:
                sum_players_cards.append(self.cards_dict[i][0])
            else:
                sum_players_cards.append(self.cards_dict[i])
        sum_players_cards = sum(sum_players_cards)
        self.players_score_count = sum_players_cards
        return sum_players_cards

    def player_move(self):
        while self.players_cards_count() < 21:
            get_card = input('Будете брать карту?\nВведите "да" или "нет": ')
            if self.validation_user_answer(get_card):
                break
            else:
                print('Вы должны вводить только "да" или "нет"!')
                print(self.players_cards)
                continue
        else:
            get_card = 'нет'

        if get_card == 'да':
            self.player_s_move = True
            return True
        else:
            self.player_s_move = False
            return False

    def unpacking_cards(self, array, sum_array):
        if self.count <= 1:
            print('Ваши карты:', end=' ')
        else:
            print('Ход диллера!')
            sleep(1.5)
            print('Карты дилера:', end=' ')
        for n, i in enumerate(array):
            if n + 1 < len(array):
                print(i, end=', ')
            else:
                print(i, end='. ')
        if self.count <= 1:
            print(f'Сумма ваших карт: {sum_array}')
        else:
            print(f'Сумма карт дилера: {sum_array}')


class Dealer(Player):
    dealers_cards = []

    def __init__(self, cards_array, cards_dict, count=0, player_s_move=True, players_score_count=0,
                 dealer_score_count=0):
        self.dealer_score_count = dealer_score_count
        super().__init__(cards_array, cards_dict, count, player_s_move, players_score_count)

    def distribution_cards_to_dealer(self):
        while True:
            self.unpacking_cards(self.dealers_cards, self.dealers_cards_count())
            if ((self.dealer_score_count <= 15 and len(self.dealers_cards) <= 3) or
                    self.players_score_count > self.dealer_score_count):
                self.dealers_cards.append(self.cards_array[0])
                del self.cards_array[0]
            elif self.dealer_score_count > 21:
                self.count += 1
                break
            elif self.dealer_score_count == 21:
                self.count += 2
                break
            else:
                self.count += 3
                break

    def dealers_cards_count(self):
        aces = ['туз буби', 'туз пик', 'туз черви', 'туз крести']
        sum_dealers_cards = []
        for i in self.dealers_cards:
            if i in aces and sum(sum_dealers_cards) + 11 <= 21:
                sum_dealers_cards.append(self.cards_dict[i][1])
            elif i in aces and sum(sum_dealers_cards) + 11 > 21:
                sum_dealers_cards.append(self.cards_dict[i][0])
            else:
                sum_dealers_cards.append(self.cards_dict[i])
        sum_dealers_cards = sum(sum_dealers_cards)
        self.dealer_score_count = sum_dealers_cards
        return sum_dealers_cards


class GameProcesses(Dealer):
    def shuffling_cards(self):
        shuffle(self.cards_array)

    def distribution_cards(self):
        while self.count < 8:
            if self.count == 0:
                self.shuffling_cards()
                for n, i in enumerate(range(4)):
                    if n % 2 == 0:
                        self.players_cards.append(self.cards_array[0])
                    else:
                        self.dealers_cards.append(self.cards_array[0])
                    del self.cards_array[0]
                else:
                    self.count += 1
            elif self.count == 1:
                self.distribution_cards_to_player()
            elif self.count == 2:
                print(f'Дилер выйграл! У Вас перебор - сумма ваших карт: {self.players_score_count}')
                break
            elif self.count == 3:
                print('Вы выйграли первым набрав 21 очко!')
                break
            elif self.count == 4:
                self.distribution_cards_to_dealer()
            elif self.count == 5:
                print(f'Вы выйграли! У дилера перебор сумма его карт: {self.dealer_score_count}')
                break
            elif self.count == 6:
                print('Вы проиграли дилер набрал 21 очко!')
                break
            elif self.count == 7:
                self.who_wins()
                break

    def who_wins(self):
        if self.players_score_count > self.dealer_score_count:
            print(f'Вы выиграли - сумма ваших карт: {self.players_score_count}! '
                  f'Сумма карт дилера: {self.dealer_score_count}!')
        elif self.players_score_count < self.dealer_score_count:
            print(
                f'Вы проиграли - сумма ваших карт: {self.players_score_count}! '
                f'Сумма карт дилера: {self.dealer_score_count}!')
        else:
            print('Ничья!')


sg = StartGame()
sg.repeat_game()
