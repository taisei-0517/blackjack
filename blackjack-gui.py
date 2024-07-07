import random
import tkinter as tk
from tkinter import simpledialog

class Table(object):
    def __init__(self, deck, dealer_frame):
        self.players = []
        self.deck = deck
        self.dealer = Dealer(self, dealer_frame)
        self.number = int(number)
        self.number_count = 0
        self.count_player = 0

    def start_play(self, player_frame): #"進行表"
        self.player_frame = player_frame
        if(self.number_count < self.number):
            self.sub_window()
        elif(self.players[0].decide == "T"): #一番最初の処理
            self.distribute_first()
            self.play_hand()
        else: #みんなのカードを引き終わったときの処理
            if(self.players[self.count_player].status in ["burst", "blackjack"] or self.players[self.count_player].decide in ["S", "DD"]): #処理が終わっていたら
                self.players[self.count_player].option_text.set("")
                self.count_player += 1
            # print(f"\nstart_count = {self.count_player}\n")
            self.play_hand()

    def dealer_hand(self):
        print(f"\nDealer has card = {self.dealer.cards[0]} {self.dealer.cards[1]}")
        print(f"total = {self.dealer.sum}")
        if (self.players[len(self.players)-1].status in ["burst", "blackjack"] or self.players[len(self.players)-1].decide in ["S", "DD"]):
            self.play_dealer()
            self.decide_win()
            for player in self.players:
                print(f"name = {player.name} bankroll = {player.bankroll}")

    def sub_window(self):
        text_name = f"player{self.number_count+1}"
        subWindow = tk.Toplevel()
        subWindow.geometry("300x200")
        sub_frame = tk.Label(subWindow)
        sub_frame.pack()
        sub_name_text_frame = tk.Label(sub_frame, text=text_name)
        sub_name_text_frame.pack()
        sub_name_frame = tk.Entry(sub_frame)
        sub_name_frame.pack()
        sub_latch_text_frame = tk.Label(sub_frame, text="掛け金(<1000)")
        sub_latch_text_frame.pack()
        sub_latch_frame = tk.Entry(sub_frame)
        sub_latch_frame.pack()
        sub_botton_frame = tk.Button(sub_frame, text="OK", command=lambda: (self.latch_action(sub_name_frame, sub_latch_frame, subWindow)))
        sub_botton_frame.pack()
        subWindow.geometry("+100+100")

    def latch_action(self, name, latch, sub_window):
        self.sub_name = name.get()
        self.sub_latch = latch.get()
        sub_window.destroy()
        self.players.append(Player(self.sub_name, self.number_count, self.player_frame))
        self.players[self.number_count].input_bankroll = int(self.sub_latch)
        self.players[self.number_count].bet_text.set(f"bet : {self.players[self.number_count].input_bankroll}")
        self.number_count += 1
        self.start_play(self.player_frame)

    def distribute_first(self):
        for i in range(2):
            for player in self.players:
                self.dealer.distribute_card(player = player, deck = self.deck)
                self.calculate_card(player = player)
                # print(f"{player.name} has card = ", end="")
                # for x in player.cards:
                #     print(f"{x} ", end="")
                # print(f"\ntotal = {player.sum}")
                if(player.sum == 21):
                    print(f"{player.name} is blackjack!!!")  #ここら辺はテキストに表示したいね
                    player.result_text.set("blackjack")
                    player.status = "blackjack"
            self.dealer.distribute_card(player = self.dealer, deck = self.deck)
            self.calculate_card(player = self.dealer)
            # print(f"{self.dealer.name} has card = ", end="")
            # for x in self.dealer.cards:
            #     if (x == self.dealer.cards[0]):
            #         print("** ", end="")
            #         continue
            #     print(f"{x} ", end = "")
            # print(f"\ntotal = {self.dealer.sum}")
            if (self.dealer.sum == 21):
                print(f"{self.dealer.name} is blackjack!!!")
                self.dealer.status = "blackjack"
                self.dealer.resutl.set("blackjack")
                print(f"{self.dealer.name} has card = {self.dealer.cards[0]} {self.dealer.cards[1]}")

    def play_hand(self):
        if(self.count_player == len(self.players)):
            self.dealer_hand()
        # print(f"count_player = {self.count_player}, len = {len(self.players)}")
        player = self.players[self.count_player]
        if(self.count_player==0): #一番最初はここの処理
            turn_text.set(f"Turn : {player.name}")
            self.action(player)
        elif(self.players[self.count_player-1].status in ["blackjack", "burst"] or self.players[self.count_player-1].decide in ["S", "DD"]):
            turn_text.set(f"Turn : {player.name}")
            self.action(player)

    def action(self, player):
        print("action")
        print(f"status:{player.status} decide:{player.decide}")
        if(player.status in ["blackjack", "burst"] or player.decide in ["S", "DD"]):
            print("action_final")
            return 
        if(len(player.cards)==2):
            if(player.card_1 == player.card_2):
                print("Stand(S), Hit(H), DoubleDown(DD), Split(SP)")
                player.option_button = tk.Button(player.option_frame, text="Stand(S)", command=lambda: self.stand(player = player))
                player.option_button.pack(side="left")
                player.option_button = tk.Button(player.option_frame, text="Hit(H)", command=lambda: self.hit(player = player))
                player.option_button.pack(side="left")
                player.option_button = tk.Button(player.option_frame, text="DoubleDown(DD)", command=lambda: self.doubledown(player = player))
                player.option_button.pack(side="left")
                player.option_button = tk.Button(player.option_frame, text="Split(SP)", command=lambda: self.split(player = player))
                player.option_button.pack(side="left")
            else:
                print("Stand(S), Hit(H), DoubleDown(DD)")
                player.option_button = tk.Button(player.option_frame, text="Stand(S)", command=lambda: self.stand(player = player))
                player.option_button.pack(side="left")
                player.option_button = tk.Button(player.option_frame, text="Hit(H)", command=lambda: self.hit(player = player))
                player.option_button.pack(side="left")
                player.option_button = tk.Button(player.option_frame, text="DoubleDown(DD)", command=lambda: self.doubledown(player = player))
                player.option_button.pack(side="left")
        else:
            print("Stand(S), Hit(H)")
            player.option_button = tk.Button(player.option_frame, text="Stand(S)", command=lambda: self.stand(player = player))
            player.option_button.pack(side="left")
            player.option_button = tk.Button(player.option_frame, text="Hit(H)", command=lambda: self.hit(player = player))
            player.option_button.pack(side="left")

    def split_action(self, player):
        if(player.split_status in ["blackjack", "burst"]):
            return 

        if(len(player.split_cards)==2):
            print("Stand(S), Hit(H), DoubleDown(DD)")
            player.split_option_button = tk.Button(player.split_option_frame, text="Stand(S)", command=lambda: self.split_stand(player = player))
            player.split_option_button.pack(side="left")
            player.split_option_button = tk.Button(player.split_option_frame, text="Hit(H)", command=lambda: self.split_hit(player = player))
            player.split_option_button.pack(side="left")
            player.split_option_button = tk.Button(player.split_option_frame, text="DoubleDown(DD)", command=lambda: self.split_doubledown(player = player))
            player.split_option_button.pack(side="left")
        else:
            print("Stand(S), Hit(H)")
            player.split_option_button = tk.Button(player.split_option_frame, text="Stand(S)", command=lambda: self.split_stand(player = player))
            player.split_option_button.pack(side="left")
            player.split_option_button = tk.Button(player.split_option_frame, text="Hit(H)", command=lambda: self.split_hit(player = player))
            player.split_option_button.pack(side="left")
    
    def stand(self, player):
        player.decide = "S"
        # a = player.option_frame.winfo_children()
        # print(f"chlidren = {a}")
        # player.option_frame内のすべての子ウィジェットを削除
        for widget in player.option_frame.winfo_children():
            widget.destroy()
        self.action(player)
        self.start_play(self.player_frame)
    
    def split_stand(self, player):
        player.split_decide = "S"
        for widget in player.split_option_frame.winfo_children():
            widget.destroy()
        self.action(player)
        self.split(player)

    def hit(self, player):
        player.decide = "H"
        self.dealer.distribute_card(player = player, deck = self.deck, status_split = False)
        self.calculate_card(player = player)
        for widget in player.option_frame.winfo_children():
            widget.destroy()
        self.action(player)
        if(player.status_split):
            self.split(player)
        else:
            self.start_play(self.player_frame)
    
    def split_hit(self, player):
        player.split_decide = "H"
        self.dealer.distribute_card(player = player, deck = self.deck, status_split = True)
        self.calculate_card(player = player, status_split = True)
        for widget in player.split_option_frame.winfo_children():
            widget.destroy()
        self.split_action(player)
        self.split(player)

    def doubledown(self, player):
        player_decide = "DD"
        self.dealer.distribute_card(player = player, deck = self.deck, status_split = False)
        self.calculate_card(player = player)
        player.input_bankroll = player.input_bankroll * 2
        player.bet_text.set(f"bet : {player.input_bankroll}")
        for widget in player.option_frame.winfo_children():
            widget.destroy()
        if(player.status_split):
            self.split(player)
        else:
            self.start_play(self.player_frame)

    def split_doubledown(self, player):        
        player_split_decide = "DD"
        self.dealer.distribute_card(player = player, deck = self.deck, status_split = True)
        self.calculate_card(player = player, status_split = True)
        player.split_input_bankroll = player.split_input_bankroll * 2
        player.split_bet_text.set(f"bet : {player.split_input_bankroll}")
        for widget in player.split_option_frame.winfo_children():
            widget.destroy()
        self.split(player)

    def split(self, player):
        player.split_name_text.set("split")
        player_decide = "SP"
        player_status_split = True
        if len(player.split_cards)==0:
            self.dealer.split_bankroll(player=player)
            self.dealer.split_card(player = player)
            self.dealer.distribute_card(player = player, deck = self.deck)
            self.calculate_card(player = player)
            self.dealer.distribute_card(player = player, deck = self.deck, status_split = True)
            self.calculate_card(player = player, status_split = True)
        elif not(player.status in ["blackjack", "burst"] or player.decide in ["S","DD"]):
            for widget in player.option_frame.winfo_children():
                widget.destroy()
                self.action(player)
        elif not(player.split_status in ["blackjack", "burst"] or player.split_decide in ["S","DD"]):
            if not(player.split_cards == 2):
                for widget in player.split_option_frame.winfo_children():
                    widget.destroy()
            self.split_action(player)
        else:
            for widget in player.option_frame.winfo_children():
                widget.destroy()
            for widget in player.split_option_frame.winfo_children():
                widget.destroy()
            self.action(player)

    def play_dealer(self):
        if (self.dealer.status == "blackjack"):
            return 
        while True:
            if self.dealer.sum > 21:
                print("dealer is burst!!!")
                self.dealer.result.set("burst")
                self.dealer.status = "burst"
                break
            elif self.dealer.sum > 17:
                break
            else:
                self.dealer.distribute_card(player = self.dealer, deck = self.deck)
                self.calculate_card(player = self.dealer)
                # print(f"{self.dealer.name} has card = ", end="")
                # for x in self.dealer.cards:
                #     print(f"{x} ", end="")
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
            rank = player.split_cards[len(player.split_cards) - 1][0]
        else:
            # print(player.cards)
            rank = player.cards[len(player.cards) - 1][0]
        
        if rank == "1":
            if(status_split):
                player.split_count_A += 1
                player_split_sum += 11
                if(player_split_sum > 21):
                    player.split_A -= 0
                    player.split_sum -= 10
            else:
                player.count_A += 1
                player.sum += 11
                if(player_sum > 21):
                    player.count_A -= 1
                    player.sum -= 10
                if(len(player.cards) == 1):
                    player.card_1 = 1
                elif(len(player.cards) == 2):
                    player.card_2 = 1
        else:
            if(status_split):
                player.split_sum += int(rank)
            else:
                player.sum += int(rank)
                if(len(player.cards) == 1):
                    player.card_1 = int(rank)
                elif(len(player.cards) == 2):
                    player.card_2 = int(rank)
        if(player.count_A > 0 and player.sum > 21):
            player.count_A -= 1
            player.sum -= 10
        elif (status_split == False):
            player.sum_text.set(f"sum : {player.sum}")
        elif(player.split_count_A > 0 and player.split_sum > 21):
            player.split_count_A = -1
            player.split_sum -= 10
        else:
            player.split_sume_text.set(f"split_sum : {player.split_sum}")
        if status_split == True:
            if player.split_sum == 21 and len(player.split_cards) == 2:
                player.split_status = "blackjack"
            elif player.split_sum > 21:
                player.split_status = "burst"
        else:
            if player.sum == 21 and len(player.cards) == 2:
                player.status_text.set("blackjack")
                player.status = "blackjack"
            elif player.sum > 21:
                player.status_text.set("burst")
                player.status = "burst"
        
class Deck(object):
    ranks = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
    suits = ["♠", "♥", "♦", "♣"]

    def __init__(self):
        self.create_deck()

    def create_deck(self):
        for suit in self.suits:
            if(suit == "♠"):
                suit = "s"
            elif(suit == "♥"):
                suit = "h"
            elif(suit == "♦"):
                suit = "d"
            elif(suit == "♣"):
                suit = "c"
            for rank in self.ranks:
                if(rank == "A"):
                    rank = 1
                elif(rank == "K"):
                    rank = 13
                elif(rank == "Q"):
                    rank = 12
                elif(rank == "J"):
                    rank = 11
                else:
                    rank = int(rank)
                name = f"cards/{str(suit)}_{rank}.png"
                image = tk.PhotoImage(file=name)
                image = image.subsample(2)
                if(rank in [13, 12, 11]):
                    deck_cards.append((10, image))
                else:
                    deck_cards.append((rank, image))
                
        random.shuffle(deck_cards)
        # print(decks)

class Player:
    def __init__(self, name, id_i, player_frame):
        self.name = name
        self.cards = []
        self.card_1 = 0
        self.card_2 = 0
        self.sum = 0
        self.split_sum = 0
        self.split_cards = []
        self.split_decide = "T"
        self.split_count_A = 0
        self.bankroll = 1000
        self.input_bankroll = 0
        self.split_input_bankroll = 0
        self.split_status = "default"
        self.status_split = False
        self.count_A = False
        self.status = "default"
        self.decide = "T"
        self.status_code = 1
        self.split_status_code = 1
        self.action_count = 0
        self.sum_text = tk.StringVar()
        self.sum_text.set("")
        self.option_text = tk.StringVar()
        self.option_text.set("")
        self.bet_text = tk.StringVar()
        self.bet_text.set("")
        self.status_text = tk.StringVar()
        self.status_text.set("")
        self.bankroll_text = tk.StringVar()
        self.bankroll_text.set("money : 1000")
        self.split_sum_text = tk.StringVar()
        self.split_sum_text.set("")
        self.split_option_text = tk.StringVar()
        self.split_option_text.set("")
        self.split_bet_text = tk.StringVar()
        self.split_bet_text.set("")
        self.split_status_text = tk.StringVar()
        self.split_status_text.set("")
        self.result_text = tk.StringVar()
        self.result_text.set("")
        self.split_result_text = tk.StringVar()
        self.split_result_text.set("")
        self.split_name_text = tk.StringVar()
        self.split_name_text.set("")
        self.player_each_frame = tk.Frame(player_frame, relief=tk.SOLID, padx=3, bd=2, bg="blue", )
        self.player_each_frame.grid(column=id_i, row=0)
        self.standard_frame = tk.Frame(self.player_each_frame, bg="blue")
        self.standard_frame.pack(fill="x", anchor=tk.E)
        self.option_frame = tk.Label(self.player_each_frame, textvariable=self.option_text, bg="blue", fg="white")
        self.option_frame.pack(after=self.standard_frame)
        self.split_frame = tk.Frame(self.player_each_frame, bg="blue")
        self.split_frame.pack(fill="both")
        self.split_option_frame = tk.Label(self.player_each_frame, textvariable=self.split_option_text, bg="blue", fg="white")
        self.split_option_frame.pack(after=self.split_frame)
        self.bet_win_frame = tk.Frame(self.player_each_frame, bg="blue")
        self.bet_win_frame.pack(fill="both")
        self.standard_card_frame = tk.Frame(self.standard_frame, bg="blue")
        self.standard_card_frame.pack(side="left", fill="x")
        self.standard_total_frame = tk.Frame(self.standard_frame, bg="blue")
        self.standard_total_frame.pack(side="left", fill="x")
        self.standard_name_frame = tk.Label(self.standard_card_frame, width=5, height=5, text=self.name, bg="blue", fg="white")
        self.standard_name_frame.pack(side="left", fill="x")
        self.standard_bet_frame = tk.Label(self.standard_total_frame, textvariable=self.bet_text, bg="blue", fg="white")
        self.standard_bet_frame.pack()
        self.standard_sum_frame = tk.Label(self.standard_total_frame,textvariable=self.sum_text, bg="blue", fg="white")
        self.standard_sum_frame.pack()
        self.standard_status_frame = tk.Label(self.standard_total_frame,textvariable=self.status_text, bg="blue", fg="white")
        self.standard_status_frame.pack()
        self.split_card_frame = tk.Frame(self.split_frame, bg="blue")
        self.split_card_frame.pack(side="left", fill="x")
        self.split_total_frame = tk.Frame(self.split_frame, bg="blue")
        self.split_total_frame.pack(side="left", fill="x")
        self.split_name_frame = tk.Label(self.split_card_frame, width=5, height=5, textvariable=self.split_name_text, bg="blue", fg="white")
        self.split_name_frame.pack(side="left", fill="x")
        self.split_bet_frame = tk.Label(self.split_total_frame, textvariable=self.split_bet_text, bg="blue", fg="white")
        self.split_bet_frame.pack()
        self.split_sum_frame = tk.Label(self.split_total_frame,textvariable=self.split_sum_text, bg="blue", fg="white")
        self.split_sum_frame.pack() 
        self.split_status_frame = tk.Label(self.split_total_frame,textvariable=self.split_status_text , bg="blue", fg="white")
        self.split_status_frame.pack()          
        self.bet_frame = tk.Label(self.bet_win_frame,textvariable=self.bankroll_text, bg="blue", fg="white")
        self.bet_frame.pack(side="left")
        self.win_frame = tk.Label(self.bet_win_frame, textvariable=self.result_text, padx=15, bg="blue", fg="white")
        self.win_frame.pack(side="left")
        self.win_frame1 = tk.Label(self.bet_win_frame, textvariable=self.split_result_text,bg="blue", fg="white")
        self.win_frame1.pack(side="left")

    # def decide_card(self, player):
    #     decide = input(":")
    #     if((player.decide == "S" or player.status == "burst") and player.status_split):
    #         player.split_decide = decide
    #     else:
    #         player.decide = decide

class Dealer(object): #勝利の判定やplayerのチップを管理するところはここ
    def __init__(self, table, dealer_frame):
        self.name = "Dealer"
        self.cards = []
        self.status = "default"
        self.count_A = 0
        self.sum = 0
        self.table = table
        self.sum_text = tk.StringVar()
        self.sum_text.set("")
        self.dealer_each_frame = tk.Frame(dealer_frame, bg="green")
        self.dealer_each_frame.pack()
        self.standard_card_frame = tk.Frame(self.dealer_each_frame, bg="green")
        self.standard_card_frame.pack(side="left", fill="both")
        self.standard_name_frame  = tk.Label(self.standard_card_frame, width=5, height=5, text="Dealer", bg="green", fg="white")
        self.standard_name_frame.pack(side="left")
        self.standard_total_frame = tk.Frame(dealer_frame, bg="green")
        self.standard_total_frame.pack(side="left", fill="x")
        self.standard_sum_frame = tk.Label(self.dealer_each_frame, textvariable=self.sum_text, bg="green", fg="white")
        self.standard_sum_frame.pack(after=self.standard_card_frame,side="left", fill="x")

    def distribute_card(self, player, deck, status_split = False):
        next_card = self.draw_card()
        if status_split:
            tk.Label(player.split_card_frame, image=next_card[1]).pack(side="left")
            player.split_cards.append(next_card)
        else:
            tk.Label(player.standard_card_frame, image=next_card[1]).pack(side="left")
            player.cards.append(next_card)
            # print(player.cards)

    def draw_card(self):
        if len(deck_cards) > 0:
            return deck_cards.pop()
        else:
            print("Deck is empty")

    def split_bankroll(self, player):
        player.split_input_bankroll = player.input_bankroll
        player.split_bet_text.set(f"bet : {player.split_input_bankroll}")
    
    def value_bankroll(self, player, win = False, split_status = False):
        if (win):
            if (split_status):
                if (player.status == "blackjack"):
                    player.bankroll = player.bankroll + player.split_input_bankroll * 0.25
                    player.split_input_bankroll = 0
                    player.bankroll_text.set(f"money : {player.bankroll}")
                    player.split_result_text.set("win")
                else:
                    player.bankroll = player.bankroll + player.split_input_bankroll
                    player.input_bankroll = 0
                    player.bankroll_text.set(f"money : {player.bankroll}")
                    player.split_result_text.set("win")
            else:
                if (player.status == "blackjack"):
                    player.bankroll = player.bankroll + player.input_bankroll * 0.25
                    player.split_input_bankroll = 0
                    player.bankroll_text.set(f"money : {player.bankroll}")
                    player.result_text.set("win")
                else:
                    player.bankroll = player.bankroll + player.input_bankroll
                    player.input_bankroll = 0
                    player.bankroll_text.set(f"money : {player.bankroll}")
                    player.result_text.set("win")
        else:
            if (split_status):
                player.bankroll = player.bankroll - player.split_input_bankroll
                player.split_input_bankroll = 0
                player.bankroll_text.set(f"money : {player.bankroll}")
                player.result_text.set("lose")
            else:
                player.bankroll = player.bankroll - player.input_bankroll
                player.input_bankroll = 0
                player.bankroll_text.set(f"money : {player.bankroll}")
                player.result_text.set("lose")

def Start_Game(player_frame, dealer_frame):
    deck = Deck()
    table = Table(deck = deck, dealer_frame = dealer_frame)
    table.start_play(player_frame = player_frame)

mainWindow = tk.Tk()
mainWindow.withdraw()
turn_text = tk.StringVar()
turn_text.set("")
number = simpledialog.askstring("Let's play blackjack", "how many player? : ", parent=mainWindow)
if number:
    mainWindow.deiconify()
mainWindow.title("Blackjack")
mainWindow.geometry("800x755")
mainWindow.configure(bg="green")
mainWindow.resizable(width=None, height=None)
menu = tk.LabelFrame(mainWindow, bd=2, relief="ridge", text="menu")
menu.pack(fill="x")
card = tk.Frame(mainWindow, relief="ridge")
card.pack(fill="x")
dealer_boad = tk.Canvas(card, width=800, height=200, bg="green")
dealer_boad.pack(fill="x")
player_boad = tk.Canvas(card, width=800, height=500, bg="blue")
player_boad.pack(fill="x")
Start_button = tk.Button(menu, text="Start Game", command=lambda: (Start_Game(player_boad, dealer_boad)))
Start_button.pack(anchor="nw", side="left")
Turn_label = tk.Label(menu, textvariable=turn_text)
Turn_label.pack(anchor="ne")
deck_cards=[]
mainWindow.geometry("+200+200")
mainWindow.mainloop()