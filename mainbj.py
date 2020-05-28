'''
BLACK JACK

'''



class Deck():
    '''
    Contains an array of tuples representing cards("suit", val) where val can be a string or int
    '''
    def __init__(self, arr=[]):
        self.arr = arr

    def add_card(self, card):
        self.arr.append(card)

    def remove_card(self):
        return self.arr.pop()

    def __str__(self):
        # when a Deck is passed as argument to print, the array is given.
        return str(self.arr)


class Player(Deck):
    '''
    Makes an instance of a unique, empty hand for each instance of a player.
    Methods are the moves a player can make.
    '''
    def __init__(self, p_hand=Deck([]), bet_amount=0):
        self.p_hand = p_hand
        self.bet_amount = bet_amount

    def bet(self, amount):
        self.bet_amount += amount

    def stay(self):
        pass

    def hit(self, card):
        return self.p_hand.add_card(card)

    def double(self, card):
        self.bet_amount *= 2
        self.hit(card)

    def __str__(self):
        return str(self.p_hand.arr[0])

    def surrender(self):
        self.bet_amount = self.bet_amount / 2
        return self.bet_amount

    def loose(self):
        b = self.bet_amount
        self.bet_amount = 0
        return b

    def count(self):
        count = {"hard": 0, "soft":0} #[hard, soft]
        for a, b in self.p_hand.arr:
            if type(b) is int:
                count['hard'] += b
                count['soft'] += b
            elif b == "A":
                count['hard'] += 1
                count['soft'] += 11
            else:
                count['hard'] += 10
                count['soft'] += 10
        return count


## HELPER FUNCTIONS

'''
basic stratgy for hard counts using 4-8 Decks and given the dealer hits on a soft 17
'''

BASIC_STRATEGY_HARD = {
    '0 to 8':"Hit",
    9:[[[2, 7, 8, 9, 10, 'A'], "Hit"], [[3, 4, 5, 6], "Double"]],
    10:[[[2, 3, 4, 5, 6, 7, 8, 9], 'Double'], [[10, 'A'], "Hit"]],
    11:[[[2, 3, 4, 5, 6, 7, 8, 9, 10], 'Double'], [['A'], 'H']],
    12:[[[2, 3, 7, 8, 9, 10, 'A'], 'Hit'], [[4, 5, 6], 'Stay']],
    '13 to 15':[[[2, 3, 4, 5, 6], 'Stay'], [[7, 8, 9, 10, 'A'], "Hit"]],
    '17 to 21':'Stay'
}


def assistant(dealer, player, number_of_deqs=6):
    '''
    matches the players count and the dealers card to the adequate move based on basic strategy
    '''
    player_count = player.count()['hard']
    dealer_card = dealer.p_hand.arr[0][1]
    if dealer_card in ['J', 'K', 'Q']:
        dealer_card = 10

    if player_count in list(range(13,17)):
        player_count = '13 to 15'
    elif player_count in list(range(17,22)):
        player_count =  '17 to 21'
    elif player_count in list(range(0, 9)):
        player_count = '0 to 8';

    first = BASIC_STRATEGY_HARD[player_count]
    if type(first) is str:
        return first
    else:
        for ranges in first:
            if dealer_card in ranges[0]:
                return ranges[1]


def full_deck(number_of_decks=1):
    '''
    initializes a deck to contain all 52 cards in one deq by default
    '''
    deq = Deck()
    while number_of_decks > 0:
        for x in ["HEARTS", "SPADES", 'CLUBS', 'DIAMONDS']:
          for y in ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "K", "J", "Q"]:
            deq.add_card((x, y))
        number_of_decks -= 1
    return deq


def print_stuf(player):
    print(player.p_hand)
    print("Your bet is {}".format(player.bet_amount))
    print(f"your hard count is: {player.count()['hard']}")
    print(f"your soft count is: {player.count()['soft']}")

import random


def shuf(deck):
    '''
    Shuffles an array, necessary as full_deck() initizlizes a Deck instance in some order
    '''
    random.shuffle(deck.arr)


def game():
    '''
    Initializes the game. Only one player supported at the moment
    '''

    print("This is a blackjack game")
    n = input("Do you wish to play? [y/n] : ")
    if n == "y":

        dealer = Player()
        player = Player()

        money_bet = 0
        first_round = True
        while True:
            '''
            main game loop
            '''
            if first_round == False:
                n = input("Do you wish to play again? [y/n]  ")
            else:
                n = 'y'

            if n == 'n':
                print("You made {}".format(
                    player.bet_amount -
                    money_bet))
                break

            #default
            number_decks = 1

            while True:
                try:
                    number_decks = int(input("How many decks do you want to play with :"))
                except:
                    print("input a valid number")
                    continue
                else:
                    break

            deq = full_deck(number_decks)
            dealer.p_hand = Deck([])
            player.p_hand = Deck([])

            # set up
            shuf(deq)
            shuf(deq)
            #make a bet
            while True:
                try:
                    amount = int(input("How much we betting? : "))
                except:
                    print("Input a valid number")
                    continue
                else:
                    print("Thanks")
                    money_bet += amount
                    player.bet(amount)
                    dealer.bet(amount)
                    break

            #Dealer gets cards
            card = deq.remove_card()
            print("Dealer's card:")
            dealer.hit(card)
            print(dealer)
            card = deq.remove_card()
            dealer.hit(card) #Second card not shown

            #Player gets cards
            card = deq.remove_card()
            player.hit(card)
            card = deq.remove_card()
            player.hit(card)
            print("Your cards:")
            print(player.p_hand)

            lost = False
            double = False

            # Player is making moves
            first_round = True

            # default
            assitant_enabled = True
            while True:

                if player.count()['hard'] > 21:  #hardcount
                    player.loose()
                    lost = True
                    print("You busted, You have exceeded 21, you loose")
                    break
                if double:   # check if busted after double
                    break

                # Assitant
                if assitant_enabled:
                    help_me = input("Assitant enabled. Disable it? [y] Nah [Any key]:")
                    if help_me == 'y':
                        assitant_enabled = False
                elif assitant_enabled == False:
                    help_me = input("Assitant disabled. Enable it? [y] Nah [Any key]")
                    if help_me == 'y':
                        assitant_enabled = True

                if assitant_enabled:
                    print("recommended move: " + assistant(dealer, player, 1))

                if first_round:
                    action = input("Select action: STAY, HIT, SURRENDER, DOUBLE : ").upper()
                else:
                    action = input("Select action: STAY, HIT, SURRENDER : ").upper()

                if action == "SURRENDER":
                    player.surrender()
                    lost = True
                    print("You loose half of your bet")
                    break
                elif action == "STAY":
                    break
                elif action == "HIT":
                    card = deq.remove_card()
                    player.hit(card)
                    print_stuf(player)
                elif action == "DOUBLE" and first_round:
                    card = deq.remove_card()
                    player.double(card)
                    print_stuf(player)
                    print("you can't hit anymore")
                    double = True
                elif action == "DOUBLE":
                    print("can't double now")

            first_round = False

            # Dealer makes move:
            if lost:
                print_stuf(player)
                continue
            win = False
            print("Dealers deck: ")
            print(dealer.p_hand)
            print("Dealer's turn: ")

            while dealer.count()['hard'] < 17:
                print("Dealer Hits")
                card = deq.remove_card()
                dealer.hit(card)
                print(dealer.p_hand)
                if dealer.count()['soft'] == 21:
                    dealer.count()['hard'] = dealer.count()['soft'] #he'll win and you don't need to make adjustment
                if dealer.count()['hard'] > 21:
                    player.bet(dealer.loose())  #player wins
                    win = True
                    print("Dealer busted, you win!")
                    break

            if win:
                print_stuf(player)
                continue

            print("Dealer can't hit anymore :")
            print(dealer.p_hand)
            if dealer.count()['hard'] >= player.count()['hard']:
                print("Dealer got closer, you loose: ")
                player.loose()
            else:
                print("Congrats! you got closer, you won")
                player.bet(dealer.loose())

            # show your new balance
            print_stuf(player)


game()




