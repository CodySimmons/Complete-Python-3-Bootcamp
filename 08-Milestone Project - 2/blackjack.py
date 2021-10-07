import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
            'Queen':10, 'King':10, 'Ace':11}
playing = True
#card class
class Card():

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self) -> str:
        return self.rank + " of " + self.suit
# deck class
class Deck:

    def __init__(self) -> None:

        self.deck = []

        for suit in suits:
            for rank in ranks:
                #Create the Card Object
                self.deck.append(Card(suit, rank))

    def __str__(self) -> str:
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return("The deck has:" + deck_comp)


    def shuffle(self):
        random.shuffle(self.deck)


    def deal(self):
        return self.deck.pop()


# hand class
class Hand:

    def __init__(self) -> None:
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        #from Deck.deal() -- single Card(suit, rank)
        self.cards.append(card)
        self.value += values[card.rank]
        #track aces
        if card.suit == 'Ace':
            self.aces += 1




    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# chip class
class Chips:
    def __init__(self) -> None:
        self.total = 100
        self.bet = 0

    def __str__(self) -> str:
        return("Total chips: " + str(self.total))

    def win_bet(self):
        self.total += self.bet

    def lost_bet(self):
        self.total -= self.bet

#betting method
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Please place you bet: "))
            if chips.bet < 0:
                #neg_error = TypeError("Bet must be greater than 0")
                raise TypeError
        except ValueError:
            print('Please enter integers only.')
        except TypeError:
            print("Bet must be greater than 0")
        else:
            if chips.total < chips.bet:
                print(f"You don't have enough chips to place that bet! (Total chips: {chips.total})")
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing
    
    while True:
        user_choice = input("Would you like to (h)it or (s)tand? Enter 'h' or 's': ")
        if user_choice[0].lower() == 'h':
            hit(deck, hand)
        elif user_choice[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        break


#hit_or_stand(test_deck, player_hand)

#card revealing
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print("!CARD HIDDEN!")
    print('', dealer.cards[1])
    print("Player's Hand: ", *player.cards, sep='\n ')
    print("Player total: ", player.value)

def show_all(player, dealer):
    print("Dealer's Hand: ", *dealer.cards, sep='\n ')
    print("Dealer total: ", dealer.value)
    print("Player's Hand: ", *player.cards, sep='\n ')
    print("Player total: ", player.value)


# End of round scenarios
# player busts
def player_busts(player, dealer, bet):
    print("Player busts!")
    bet.lost_bet()
# player wins
def player_wins(player, dealer, bet):
    print("Player wins!")
    bet.win_bet()
# dealer busts
def dealer_busts(player, dealer, bet):
    print("Dealer busts!")
    bet.win_bet()
# dealer wins
def dealer_wins(player, dealer, bet):
    print("Dealer wins!")
    bet.lost_bet()
# tie (called a push)
def push(player, dealer, bet):
    print("Player and dealer tie! It's a push!")


'''test_deck = Deck()
test_deck.shuffle()
test_chips = Chips ()
player_hand = Hand()
dealer_hand = Hand()
player_hand.add_card(test_deck.deal())
player_hand.add_card(test_deck.deal())
dealer_hand.add_card(test_deck.deal())
dealer_hand.add_card(test_deck.deal())

show_some(player_hand, dealer_hand)
show_all(player_hand, dealer_hand)'''


#game logic
while True:
    print("Welcome to Blackjack! Get as close to 21 without going over!\n\
        The Dealer hits until they reach 17. Aces count as 1 or 11.")
    #create deck & play objects
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #create player chips and take bet
    player_chips = Chips()
    take_bet(player_chips)

    #show starting cards
    show_some(player_hand, dealer_hand)

    while playing:
        # player hits or stands
        hit_or_stand(deck, player_hand)

        # shows result of last action
        show_some(player_hand, dealer_hand)

        # bust check
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    
    # if player hasn't bust, play dealer's hand until over 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            dealer_hand.add_card(deck.deal())
        
        #final hands, no more cards incoming
        show_all(player_hand, dealer_hand)

        #win/lose scenario checks
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand, player_chips)
    
    # Player current chips
    print("Player's current chips: ", player_chips.total)

    # play again check
    play_again = input("Would you like to play again? Y or N: ")
    if play_again[0].upper() == 'Y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break


        # game loop



