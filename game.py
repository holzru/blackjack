import random
import sys

def set_up():
    dealer = Dealer()
    while True:
        try:
            nop = int(raw_input("How many people will be playing? (please enter in 1-9 players) "))
        except:
            print "Please enter a number between 1-9"
            continue
        else:
            print "Great let's get their names"
            break

    players = []
    count = 0
    while count < nop:
        name = raw_input("What's your name? ")
        name = Player(name)
        players.append(name)
        count += 1
    else:
        players.append(dealer)
        print
        game(players, dealer)


def game(players, dealer):
    game_deck = Deck(8)
    intermediate_list = []
    for player in players:
        if player != dealer:
            while True:
                try:
                    if player.bankroll <= 0:
                        player.bankroll = 20
                    print "{} has {}".format(player.name, player.bankroll)
                    bet = float(raw_input("how much would you like to bet? "))
                    if bet > player.bankroll:
                        print "Sorry you don't have that much"
                        continue
                except:
                    print "That's not an acceptable bet."
                    continue
                else:
                    player.make_bet(bet)
                    print "You bet: {}, current bankroll: {}\n".format(bet, player.bankroll)
                    break
            intermediate_list.append(Hand(dealer.hit(game_deck), dealer.hit(game_deck), player, bet))
        else:
            intermediate_list.append(Hand(dealer.hit(game_deck), dealer.hit(game_deck), dealer, bet))

    hands = []
    for item in intermediate_list[:-1]:
        receipt = item.player
        if item.blackjack() == True:
            receipt.bankroll += item.bet * 2.5
            print '{} hit Blackjack! You win {}, your bankroll is now: {}\n'.format(receipt.name, item.bet*2.5, receipt.bankroll)
        elif receipt.bankroll >= item.bet and item.split_it():
            hand1 = Hand(item.card_list()[0], dealer.hit(game_deck), receipt, item.bet)
            print hand1.card_list()
            hand2 = Hand(item.card_list()[0], dealer.hit(game_deck), receipt, item.bet)
            print hand2.card_list()
            receipt.bankroll -= item.bet
            print "{}'s bankroll is now {}\n".format(receipt.name, receipt.bankroll)
            for hand in [hand1, hand2]:
                if hand.hand_value() == 21:
                    (hand.player).bankroll += hand.bet * 2.5
                    print '{} hit Blackjack! You win {}, your bankroll is now: {}\n'.format((hand.player).name, hand.bet*2.5, (hand.player).bankroll)
                else:
                    hands.insert(0, hand)
            for item in [hand1, hand2]:
                if receipt.bankroll >= item.bet and item.split_it():
                    print item.card_list()
                    hand3 = Hand(item.card_list()[0], dealer.hit(game_deck), receipt, item.bet)
                    print hand3.card_list()
                    hand4 = Hand(item.card_list()[0], dealer.hit(game_deck), receipt, item.bet)
                    print hand4.card_list()
                    receipt.bankroll -= item.bet
                    print "{}'s bankroll is now {}\n".format(receipt.name, receipt.bankroll)
                    hands.remove(item)
                    for hand in [hand3, hand4]:
                        if hand.hand_value() == 21:
                            (hand.player).bankroll += hand.bet * 2.5
                            print '{} hit Blackjack! You win {}, your bankroll is now: {}\n'.format((hand.player).name, hand.bet*2.5, (hand.player).bankroll)
                        else:
                            hands.insert(0, hand)
        else:
            hands.append(item)

    dealer_hand = intermediate_list[-1]
    final_hands = []
    for hand in hands:
        if (hand.player).bankroll >= hand.bet and hand.split_it():
            hand1 = Hand(hand.card_list()[0], dealer.hit(game_deck), hand.player, hand.bet)
            hand2 = Hand(hand.card_list()[0], dealer.hit(game_deck), hand.player, hand.bet)
            hands.pop(hands.index(hand))
            if hand1.hand_value() == 21:
                (hand1.player).bankroll += hand1.bet * 2.5
                print '{} hit Blackjack! You win {}, your bankroll is now: {}\n'.format((hand1.player).name, hand1.bet*2.5, (hand1.player).bankroll)
            else:
                hands.append(hand1)
            if hand2.hand_value() == 21:
                (hand2.player).bankroll += hand2.bet * 2.5
                print '{} hit Blackjack! You win {}, your bankroll is now: {}\n'.format((hand2.player).name, hand2.bet*2.5, (hand2.player).bankroll)
            else:
                hands.append(hand2)

    for hand in hands:
        print (hand.player).name, hand.card_list()
        print

    for hand in hands:
        print "Dealer's Top Card: {}\n".format(dealer_hand.card_list()[0])
        move = ''
        print "{}'s' hand is: {}".format((hand.player).name, hand.card_list())
        print "You're at {}".format(hand.hand_value())
        times = 0
        while True:
            if times == 0 and (hand.player).bankroll >= hand.bet:
                double = raw_input("Would you like to double down? (y/n)")
                if double.lower() == 'y':
                    (hand.player).bankroll -= hand.bet
                    hand.bet += hand.bet
                    print "Your bet is now: {}".format(hand.bet)
                    print "Your bankroll is now: {}".format((hand.player).bankroll)
                    hitter(hand, dealer, game_deck)
                    if hand.hand_value() > 21:
                        print "You busted"
                        print "Your bankroll is now: {}\n".format((hand.player).bankroll)
                        break
                    else:
                        final_hands.append(hand)
                        print "You're hand is now {}, for a total of {}".format(hand.card_list(), hand.hand_value())
                        print "Good Luck Cocky Person!\n"
                        break
                elif double.lower() == 'n':
                    times += 1
                else:
                    print "Sorry that wasn't a valid response"
                    continue

            move = raw_input("{} do you want to (h)it or (s)tay?".format((hand.player).name))
            if move == 'h':
                hitter(hand, dealer, game_deck)
                if hand.hand_value() > 21:
                    print "You busted"
                    print "Your bankroll is now: {}\n".format((hand.player).bankroll)
                    break
                else:
                    continue
            elif move == 's':
                final_hands.append(hand)
                print "Stayed\n"
                break
            else:
                print "That wasn't one of the two options."

    insured = []
    if dealer_hand.card_list()[0] == 'A':
        for hand in final_hands:
            while True:
                if (hand.player).bankroll >= (hand.bet/2.0):
                    insurance = raw_input("{} would you like to buy insurance, you bankroll is currently {}? (y/n)".format((hand.player).name, (hand.player).bankroll))
                    if insurance.lower() == 'y':
                        while True:
                            try:
                                amount = float(raw_input("You can bet up to {}. What's your bet?  ".format(hand.bet/2.0)))
                                if amount > (hand.bet/2.0):
                                    print "That's too much!"
                                    continue
                                else:
                                    (hand.player).bankroll -= amount
                                    insured.append(Insurance(hand.player, amount))
                                    print
                                    break
                            except:
                                print "That wasn't a valid amount!"
                                break
                        break
                    elif insurance.lower() == 'n':
                        print "Living dangerously I see\n"
                        break
                    else:
                        print "Sorry that's not a valid response"
                        continue
                else:
                    break

    if final_hands:
        if dealer_hand.hand_value() == 21 and len(dealer_hand.card_list()) == 2:
            print "Dealer hit blackjack!"
            for hand in final_hands:
                print "{} looses!".format((hand.player).name)
                print "Bankroll is now: {}\n".format((hand.player).bankroll)
            for hand in insured:
                print "{} made a good decision buying insurance, you win {}\n".format((hand.player).name, hand.amount*2)
                (hand.player).bankroll += hand.amount * 2
            del final_hands[:]
        while dealer_hand.hand_value() < 17:
            hitter(dealer_hand, dealer, game_deck)
            print "Dealer has {} for a total of {}\n".format(dealer_hand.card_list(), dealer_hand.hand_value())
        if dealer_hand.hand_value() > 21:
            print "Dealer busted\n"
            for hand in final_hands:
                print "{} is a winner!".format((hand.player).name)
                (hand.player).bankroll += hand.bet * 2.0
                print "Bankroll is now: {}\n".format((hand.player).bankroll)
        else:
            for hand in final_hands:
                print "Dealer has {}".format(dealer_hand.hand_value())
                if hand.hand_value() > dealer_hand.hand_value():
                    print "{} is a winner!".format((hand.player).name)
                    (hand.player).bankroll += hand.bet * 2.0
                    print "Bankroll is now: {}\n".format((hand.player).bankroll)
                elif hand.hand_value() == dealer_hand.hand_value():
                    print "{} pushes".format((hand.player).name)
                    (hand.player).bankroll += hand.bet
                    print "Bankroll is now: {}\n".format((hand.player).bankroll)
                else:
                    print "{} looses!".format((hand.player).name)
                    print "Bankroll is now: {}\n".format((hand.player).bankroll)

    while True:
        again = raw_input("Would you like to keep playing? (y/n)")
        if again.lower() == 'y':
            print
            game(players, dealer)
        elif again.lower() == 'n':
            print "Thanks for playing!"
            sys.exit(0)
        else:
            print "I don't understand what you want?"
            continue


def hitter(hand, dealer, game_deck):
    new_card = dealer.hit(game_deck)
    hand.add_a_card(new_card)
    print hand.hand_value()
    print hand.card_list()



class Player(object):

    def __init__(self, name, bankroll = 100.00):
        self.name = name
        self.bankroll = bankroll

    def withdrawal(self, amount):
        self.bankroll += amount

    def make_bet(self, amount):
        self.bankroll -= amount



class Dealer(Player):

    def __init__(self, name = 'dealer'):
        self.name = name

    def hit(self, deck):
        dealt = deck.remover()
        return dealt



class Deck(object):
    deck = ['A', 'A', 'A', 'A', 'K', 'K', 'K', 'K', 'Q', 'Q', 'Q', 'Q',
            'J', 'J', 'J', 'J', 10, 10, 10, 10, 9, 9, 9, 9, 8, 8, 8, 8,
            7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3,
            2, 2, 2, 2]

    def __init__(self, decks = 1):
        self.decks = decks*self.deck

    def remover(self):
        card_index = random.randint(0,len(self.decks)-1)
        card = self.decks[card_index]
        self.decks.pop(card_index)
        return card



class Hand(object):

    def __init__(self, card1, card2, player, bet):
        self.card1 = card1
        self.card2 = card2
        self.player = player
        self.bet = float(bet)
        self.cards = [card1, card2]

    def blackjack(self):
        if self.hand_value() == 21 and len(self.cards) == 2:
            return True
        else:
            return False

    def split_it(self):
        if self.card1 == self.card2:
            print self.cards
            ask = raw_input('{} would you like to split? (y/n)'.format((self.player).name))
            if ask == 'y':
                return self.card1
            else:
                return None
        else:
            return None

    def card_list(self):
        return self.cards

    def make_bet(self, player):
        player.bankroll -= self.bet

    def hand_value(self):
        hand_total = 0
        cards = []
        for item in self.cards:
            if item != 'A':
                cards.insert(0, item)
            else:
                cards.append(item)
        for item in cards:
            if type(item) == int:
                hand_total += item
            elif item in ['J', 'Q', 'K']:
                    hand_total += 10
            else:
                if hand_total < 11 and cards.count('A') < 2:
                    hand_total += 11
                elif cards.count('A') >= 2 and hand_total < 10:
                    hand_total += 11

                else:
                    hand_total += 1
        return hand_total

    def add_a_card(self, new_card):
        self.cards.append(new_card)



class Insurance(object):

    def __init__(self, player, amount):
        self.player = player
        self.amount = amount




set_up()
