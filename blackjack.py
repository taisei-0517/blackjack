import random

class Table(object):
    def __init__(self, deck ):
        self.players = []
        self.deck = deck
        self.dealer = Dealer(self)

    def start_play(self): #"進行表"
        paticipate = int(input("how many people?(<4): "))
        self.latch_action(number = paticipate)
        self.distribute_first()
        self.play_hand()
        print(f"\nDealer has card = {self.dealer.cards[0]} {self.dealer.cards[1]}")
        print(f"total = {self.dealer.sum}")
        self.play_dealer()
        self.decide_win()
        for player in self.players:
            print(f"name = {player.name} bankroll = {player.bankroll}")

    def latch_action(self, number):
        for i in range(number):
            self.players.append(Player(input(f"player{i+1}: ")))
            while True:
                latch = int(input("latch(<1000): "))
                if (latch > 1000):
                    print("under 1000")
                    continue
                self.players[i].input_bankroll = latch
                break

    def distribute_first(self):
        for i in range(2):
            for player in self.players:
                self.dealer.distribute_card(player = player, deck = self.deck)
                self.calculate_card(player = player)
                print(f"{player.name} has card = ", end="")
                for x in player.cards:
                    print(f"{x} ", end="")
                print(f"\ntotal = {player.sum}")
                if(player.sum == 21):
                    print(f"{player.name} is blackjack!!!")
                    player.status = "blackjack"
            self.dealer.distribute_card(player = self.dealer, deck = self.deck)
            self.calculate_card(player = self.dealer)
            print(f"{self.dealer.name} has card = ", end="")
            for x in self.dealer.cards:
                if (x == self.dealer.cards[0]):
                    print("** ", end="")
                    continue
                print(f"{x} ", end = "")
            print("")
            if (self.dealer.sum == 21):
                print(f"{self.dealer.name} is blackjack!!!")
                self.dealer.status = "blackjack"
                print(f"{self.dealer.name} has card = {self.dealer.cards[0]} {self.dealer.cards[1]}")

    def play_hand(self):
        for player in self.players:
            while True:
                if(player.status == "blackjack"):
                    break
                status_code = self.dealer.action(player = player)
                if status_code == 0:
                    break

    def play_dealer(self):
        if (self.dealer.status == "blackjack"):
            return 
        while True:
            if self.dealer.sum > 21:
                print("dealer is burst!!!")
                self.dealer.status = "burst"
                break
            elif self.dealer.sum > 17:
                break
            else:
                self.dealer.distribute_card(player = self.dealer, deck = self.deck)
                self.calculate_card(player = self.dealer)
                print(f"{self.dealer.name} has card = ", end="")
                for x in self.dealer.cards:
                    print(f"{x} ", end="")
                print(f"\ntotal = {self.dealer.sum}")

    def decide_win(self):
        if (self.dealer.status == "blackjack"):
            for player in self.players:
                if (player.status == "blackjack"):
                    print(f"{player.name} win ")
                else:
                    self.dealer.balue_bankroll(player = player, win = False)
        elif (self.dealer.sum > 21): #dealerがバーストしたとき
            for player in self.players:
                if (len(player.split_cards) != 0): #splitしたとき
                    if (player.sum <= 21):
                        print(f"{player.name}(1): win ")
                        self.dealer.value_bankroll(player = player, win = True)
                    elif (player.split_sum <= 21):
                        print(f"{player.name}(2): win ")
                        self.dealer.value_bankroll(player = player, win = True, split_status = True)
                    else:
                        if(player.input_bankroll == 0):
                            self.dealer.value_bankroll(player = player, win =False, split_status = True)
                        else:
                            self.dealer.value_bankroll(player = player, win = False, split_staus = False)
                elif(player.sum <= 21):
                    print(f"{player.name} win ")
                    self.dealer.value_bankroll(player = player, win = True)
                else:
                    self.dealer.value_bankroll(player = player, win = False)
        else: #dealerがバーストしていないとき
            for player in self.players:
                if(len(player.split_cards) != 0):
                    if(player.sum <= 21 and player.sum > self.dealer.sum):
                        print(f"{player.name}(1): win")
                        self.dealer.value_vankroll(player = player, win = True)
                    elif (player.split_sum <= 21 and player.split_sum > self.dealer.sum):
                        print(f"{player.name}(2): win")
                        self.dealer.value_bankroll(player = player, win = True, split_status = True)
                    else:
                        if(player.input_bankroll == 0):
                            self.dealer.value_bankroll(player = player, win =False, split_status = True)
                        else:
                            self.dealer.value_bankroll(player = player, win = False, split_staus = False)
                elif(player.sum <= 21 and player.sum > self.dealer.sum):
                    print(f"{player.name} win")
                    self.dealer.value_bankroll(player = player, win = True, split_status = False)
                else:
                    self.dealer.value_bankroll(player = player, win = False, split_status = False)

    def calculate_card(self, player,status_split = False):
        if status_split == True:
            rank = player.split_cards[len(player.split_cards) - 1][1]
        else:
            # print(player.cards)
            rank = player.cards[len(player.cards) - 1][1]
        if rank in ["2","3","4","5","6","7","8","9","10"]:
            if(status_split):
                player.split_sum += int(rank)
            else:
                player.sum += int(rank)
                if (len(player.cards) == 1):
                    player.card_1 = int(rank)
                elif (len(player.cards) == 2):
                    player.card_2 = int(rank)
        elif rank in ["K", "Q", "J"]:
            if(status_split):
                player.split_sum += 10
            else:
                player.sum += 10
                if (len(player.cards) == 1):
                    player.card_1 = 10
                elif (len(player.cards) == 2):
                    player.card_2 = 10
        else: #Aの処理
            if(status_split):
                player.split_A = True
                player.split_sum += 11
                if(player.split_sum > 21):
                    player.split_A = False
                    player.split_sum -= 10
            else:
                player.status_A = True
                player.sum += 11
                if(player.sum > 21):
                    player.status_A = False
                    player.sum -= 10
                if (len(player.cards) == 1):
                    player.card_1 = 1
                elif (len(player.cards) == 2):
                    player.card_2 = 1
        if(player.status_A and player.sum > 21):
            player.status_A = False
            player.sum -= 10
        elif (status_split == False):
            return 
        elif(player.split_A and player.split_sum > 21):
            player.split_A = False
            player.split_sum -= 10

class Deck(object):
    rank1 = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
    suite1 = ["♠", "♥", "♦", "♣"]

    def __init__(self, name = "default"):
        self.decks = self.create_deck()
        self.name = name

    def create_deck(self):
        decks = []
        for x in self.suite1:
            for y in self.rank1:
                decks.append((x,y))
                
        random.shuffle(decks)
        # print(decks)
        return decks

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.card_1 = 0
        self.card_2 = 0
        self.sum = 0
        self.split_sum = 0
        self.split_cards = []
        self.split_decide = "T"
        self.split_A = False
        self.bankroll = 1000
        self.input_bankroll = 0
        self.split_input_bankroll = 0
        self.split_status = "default"
        self.status_split = False
        self.status_A = False
        self.status = "default"
        self.decide = "T"

    def add_card(self, card, is_split = False):
        if is_split:
            self.split_cards.append(card)
        else:
            self.cards.append(card)

    def decide_card(self, player):
        decide = input(":")
        if((player.decide == "S" or player.status == "burst") and player.status_split):
            player.split_decide = decide
        else:
            player.decide = decide

class Dealer(object): #勝利の判定やplayerのチップを管理するところはここ
    def __init__(self, table):
        self.name = "Dealer"
        self.cards = []
        self.status = "default"
        self.status_A = False
        self.sum = 0
        self.table = table

    def distribute_card(self, player, deck, status_split = False):
        if status_split:
            player.split_cards.append(self.draw_card(deck = deck))
        else:
            player.cards.append(self.draw_card(deck = deck))
            # print(player.cards)

    def draw_card(self, deck):
        if len(deck.decks) > 0:
            return deck.decks.pop()
        else:
            print("Deck is empty")

    def split_bankroll(self, player):
        player.split_input_bankroll = player.input_bankroll
    
    def split_card(self, player):
        player.split_cards.append(player.cards.pop())
        player.sum = int(player.sum / 2)
        player.split_sum = player.sum

    def split_card_number(self, rank):
        if rank in ["2","3","4","5","6","7","8","9","10"]:
            number = int(rank)
        elif rank in ["K", "Q", "J"]:
            number = 10
        else:
            number = 11
        return number 

    def action(self, player):
        if(self.status == "blackjack"):
            return 0
        if(player.status_split):
            if(player.decide in ["SP", "H"] and not(player.status == "burst")):
                print(f"1: Stand(S), Hit(H)", end="")
            elif(player.split_decide in ["T", "H"] and not(player.split_status == "burst")):
                print(f"2: Stand(S), Hit(H)", end="")
            if (player.decide == "SP" and player.input_bankroll * 2 < player.bankroll ) or ((player.decide == "S" or player.status == "burst") and player.split_decide == "T" and player.split_input_bankroll * 2 < player.bankroll):
                print(", DoubleDown(DD)", end="")
        else:
            print(f"{player.name}: Stand(S), Hit(H)", end="")
            if (len(player.cards) == 2 and player.bankroll >= player.input_bankroll * 2):
                print(", DoubleDown(DD)", end="")
            if (player.card_1 == player.card_2 and player.bankroll >= player.input_bankroll * 2 and not(self.status == "blackjack")):
                print(", Split(SP)", end="")
        player.decide_card(player = player)
        if player.decide == "SP":
            self.split(player=player)
            return 0
        elif (player.decide == 'H'and player.split_decide == "T") or player.split_decide == "H":
            self.hit(player = player)
        elif (player.decide == 'DD'and player.split_decide == "T") or player.split_decide == "DD":
            self.doubledown(player = player)
        if(not(player.status_split)):
            print(f"\n{player.name} has card = ", end = "")
            for x in player.cards:
                print(f"{x} ", end="")
            print("")
            if (player.sum > 21):
                print(f"total = {player.sum}")
                print(f"{player.name} is burst!!!\n")
                player.status = "burst"
                return 0
            print(f"total = {player.sum}")
        if((player.sum == 21 and player.split_decide == "T") or player.split_sum == 21):
            if (player.split_status):
                return 1
            else:
                return 0
        elif(player.decide == 'DD'and player.split_decide == "T") or player.split_decide == "DD":
            return 0
        elif(player.decide == 'S'and player.split_decide == "T") or player.split_decide == "S":
            return 0

    def hit(self, player):
        if(player.split_decide == "H"): #splitのとき
            self.distribute_card(player = player, deck = self.table.deck, status_split = True)
            self.table.calculate_card(player = player, status_split = True)
        else:
            self.distribute_card(player = player, deck = self.table.deck, status_split = False)
            self.table.calculate_card(player = player)

    def doubledown(self, player):
        if(player.split_decide == "DD"):
            self.distribute_card(player = player, deck = self.table.deck, status_split = True)
            self.table.calculate_card(player = player, status_split = True)
            player.split_input_bankroll = player.split_input_bankroll * 2
        else:
            self.distribute_card(player = player, deck = self.table.deck, status_split = False)
            self.table.calculate_card(player = player)
            player.input_bankroll = player.input_bankroll * 2

    def split(self, player):
        self.split_bankroll(player = player)
        player.status_split = True
        self.split_card(player = player)
        print(f"{player.name} has card = ")
        print(f"1: {player.cards[0]}")
        print(f"2: {player.split_cards[0]}")
        self.distribute_card(player = player, deck = self.table.deck)
        self.table.calculate_card(player = player)
        self.distribute_card(player = player, deck = self.table.deck, status_split = True)
        self.table.calculate_card(player = player, status_split = True)
        for i in range(2):
            status_code = 1
            while True:
                # print(f"player.sum = {player.sum} i = {i}")
                # print(f"player.split_sum = {player.split_sum}")
                print(f"{player.name} has card = ")
                print(f"1: ", end="")
                for x in player.cards:
                    print(f"{x} ", end="")
                print(f"\ntotal = {player.sum}")
                print(f"2: ", end="")
                for x in player.split_cards:
                    print(f"{x} ", end="")
                print(f"\ntotal = {player.split_sum}")
                if(player.sum > 21 and i == 0):
                    print(f"{player.name}(1) is burst!!!")
                    player.status = "burst"
                    break
                elif (player.split_sum > 21 and i == 1):
                    print(f"{player.name}(2) is burst!!!")
                    player.split_status = "burst"
                    break
                elif (player.sum == 21 and i == 0):
                    if(len(player.cards) == 2):
                        print(f"{player.name}(1) is blackjack!!!")
                        player.status = "blackjack"
                    break
                elif (player.split_sum == 21 and i == 1):
                    if (len(player.cards) == 2):
                        print(f"{player.name}(2) is blackjack!!!")
                        player.split_status = "blackjack"
                    break
                if (status_code == 0):
                    break                
                status_code = self.action(player = player)

    def value_bankroll(self, player, win = False, split_status = False):
        if (win):
            if (split_status):
                if (player.status == "blackjack"):
                    player.bankroll = player.bankroll + player.split_input_bankroll * 0.25
                    player.split_input_bankroll = 0
                else:
                    player.bankroll = player.bankroll + player.split_input_bankroll
                    player.input_bankroll = 0
            else:
                if (player.status == "blackjack"):
                    player.bankroll = player.bankroll + player.input_bankroll * 0.25
                    player.split_input_bankroll = 0
                else:
                    player.bankroll = player.bankroll + player.input_bankroll
                    player.input_bankroll = 0
        else:
            if (split_status):
                player.bankroll = player.bankroll - player.split_input_bankroll
                player.split_input_bankroll = 0
            else:
                player.bankroll = player.bankroll - player.input_bankroll
                player.input_bankroll = 0
            
def main():
    deck = Deck()
    table = Table(deck = deck)
    table.start_play()

if __name__ == "__main__":
    main()