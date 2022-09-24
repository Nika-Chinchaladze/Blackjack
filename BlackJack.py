from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sqlite3
from random import choice
from Cards import card_list
from Score import score_dict
from Outcome import IronMan

# connect database or create if not exist:
conn = sqlite3.connect("chincharito.db")
curr = conn.cursor()
curr.execute('''CREATE TABLE IF NOT EXISTS outcome(player text, wins text, loses text)''')
conn.commit()
conn.close()

class Muhammad_Ali(QMainWindow):
    def __init__(self):
        super(Muhammad_Ali, self).__init__()
        uic.loadUi("game.ui", self)

        # define content:
        self.head_label = self.findChild(QLabel, "head_label")
        self.table_label = self.findChild(QLabel, "table_label")
        self.card_1 = self.findChild(QLabel, "card_1")
        self.card_2 = self.findChild(QLabel, "card_2")
        self.card_3 = self.findChild(QLabel, "card_3")
        self.card_4 = self.findChild(QLabel, "card_4")
        self.card_5 = self.findChild(QLabel, "card_5")
        self.card_6 = self.findChild(QLabel, "card_6")
        self.card_7 = self.findChild(QLabel, "card_7")
        self.card_8 = self.findChild(QLabel, "card_8")
        self.card_9 = self.findChild(QLabel, "card_9")
        self.card_10 = self.findChild(QLabel, "card_10")
        self.player_label = self.findChild(QLabel, "player_label")
        self.dealer_label = self.findChild(QLabel, "dealer_label")
        self.result_label = self.findChild(QLabel, "result_label")
        self.p_label = self.findChild(QLabel, "p_label")
        self.d_label = self.findChild(QLabel, "d_label")
        self.ps_label = self.findChild(QLabel, "ps_label")
        self.ds_label = self.findChild(QLabel, "ds_label")
        
        self.open_button = self.findChild(QPushButton, "open_button")
        self.take_button = self.findChild(QPushButton, "take_button")
        self.end_button = self.findChild(QPushButton, "end_button")
        self.see_button = self.findChild(QPushButton, "see_button")
        self.save_button = self.findChild(QPushButton, "save_button")
        self.start_button = self.findChild(QPushButton, "start_button")
        self.again_button = self.findChild(QPushButton, "again_button")
        self.take_button.setEnabled(False)
        self.open_button.setEnabled(False)

        # variables:
        self.count_scores = score_dict
        self.all_cards = [item for item in card_list]
        self.player_cards = []
        self.dealer_cards = []
        self.player_score = 0
        self.dealer_score = 0
        self.player_winnings = 0
        self.dealer_winnings = 0

        # for take operation:
        self.boom = 3
        self.big = 8
        self.ace = ['a_square.jpg', 'a_cross.jpg', 'a_black.jpg', 'a_heart.jpg']

        # call defined method from here:
        self.end_button.clicked.connect(lambda: self.close())
        self.start_button.clicked.connect(self.Start_game)
        self.take_button.clicked.connect(self.Take_card)
        self.open_button.clicked.connect(self.Open_cards)
        self.again_button.clicked.connect(self.Play_Again)
        self.save_button.clicked.connect(self.Save_results)
        self.see_button.clicked.connect(self.See_Statistics)

        self.show()

# ------------------------------------------- logic ---------------------------------------- #
    # define calculate method:
    def Calculate_score(self):
        for card in self.player_cards:
                for key, val in self.count_scores.items():
                    if card == key:
                        self.player_score += val
            
        for item in self.dealer_cards:
            for first, second in self.count_scores.items():
                if item == first:
                    self.dealer_score += second
        
        self.player_label.setText(f"{self.player_score}")
        self.dealer_label.setText(f"{self.dealer_score}")
    
    # define method for game records:
    def Track_records(self):
        outcome = self.result_label.text()
        if outcome == "Dealer Won the Game, with BlackJack!" or outcome == "Dealer Won the Game!":
            self.dealer_winnings += 1
        elif outcome == "Player Won the Game, with BlackJack!" or outcome == "Player Won the Game!":
            self.player_winnings += 1
        self.ds_label.setText(f"{self.dealer_winnings}")
        self.ps_label.setText(f"{self.player_winnings}")
    
    # define winner:
    def Winner(self):
        if self.player_score == self.dealer_score:
            self.result_label.setText("It's Draw!")
        elif self.dealer_score == 21:
            self.result_label.setText("Dealer Won the Game, with BlackJack!")
        elif self.player_score == 21:
            self.result_label.setText("Player Won the Game, with BlackJack!")
        elif self.player_score > 21 and self.dealer_score > 21:
            if self.player_score > self.dealer_score:
                self.result_label.setText("Dealer Won the Game!")
            elif self.player_score < self.dealer_score:
                self.result_label.setText("Player Won the Game!")
            else:
                self.result_label.setText("It's Draw!")
        elif self.player_score > 21:
            self.result_label.setText("Dealer Won the Game!")
        elif self.dealer_score > 21:
            self.result_label.setText("Player Won the Game!")
        elif self.player_score > self.dealer_score:
            self.result_label.setText("Player Won the Game!")
        else:
            self.result_label.setText("Dealer Won the Game!")

    # define method for start button:
    def Start_game(self):
        for i in range(2):
            self.player_cards.append(choice(self.all_cards))
            self.dealer_cards.append(choice(self.all_cards))
        
        for card in self.player_cards:
            if card in self.all_cards:
                self.all_cards.remove(f"{card}")
        for item in self.dealer_cards:
            if item in self.all_cards:
                self.all_cards.remove(f"{item}")
        
        self.card_1.setPixmap(QPixmap(self.player_cards[0]))
        self.card_2.setPixmap(QPixmap(self.player_cards[1]))

        self.card_6.setPixmap(QPixmap(self.dealer_cards[0]))
        self.card_7.setPixmap(QPixmap("instead.jpg"))

        self.Calculate_score()
        if self.dealer_score != 21 and (self.player_score > 21 or self.dealer_score > 21):
            self.Winner()
        elif self.player_score == 21 or self.dealer_score == 21:
            self.Winner()

        if len(self.result_label.text()) > 0:
            self.Track_records()

        self.start_button.setEnabled(False)
        self.take_button.setEnabled(True)
        self.open_button.setEnabled(True)
    
    # define method for take button:
    def Take_card(self):
        # for player perspective:
        self.player_cards.append(choice(self.all_cards))
        self.all_cards.remove(f"{self.player_cards[-1]}")

        if self.boom == 3:
            self.card_3.setPixmap(QPixmap(self.player_cards[-1]))
        elif self.boom == 4:
            self.card_4.setPixmap(QPixmap(self.player_cards[-1]))
        elif self.boom == 5:
            self.card_5.setPixmap(QPixmap(self.player_cards[-1]))

        for key, val in self.count_scores.items():
            if key == self.player_cards[-1]:
                if self.player_score >= 11 and (self.player_cards[-1] in self.ace):
                    self.player_score += 1
                else:
                    self.player_score += val
        self.player_label.setText(f"{self.player_score}")
        self.boom += 1

        # for dealer perspective:
        if self.dealer_score < 17:
            self.dealer_cards.append(choice(self.all_cards))
            self.all_cards.remove(f"{self.dealer_cards[-1]}")

            if self.big == 8:
                self.card_8.setPixmap(QPixmap("instead.jpg"))
            elif self.big == 9:
                self.card_9.setPixmap(QPixmap("instead.jpg"))
            elif self.big == 10:
                self.card_10.setPixmap(QPixmap("instead.jpg"))
            self.big += 1
        
            for key, val in self.count_scores.items():
                if key == self.dealer_cards[-1]:
                    self.dealer_score += val
            self.dealer_label.setText(f"{self.dealer_score}")

        if self.dealer_score != 21 and (self.player_score > 21 or self.dealer_score > 21):
            self.Winner()
        elif self.player_score == 21 or self.dealer_score == 21:
            self.Winner()
        

    # define method for open button:
    def Open_cards(self):
        length = len(self.dealer_cards)
        if length == 2:
            self.card_7.setPixmap(QPixmap(self.dealer_cards[1]))
        elif length == 3:
            self.card_7.setPixmap(QPixmap(self.dealer_cards[1]))
            self.card_8.setPixmap(QPixmap(self.dealer_cards[2]))
        elif length == 4:
            self.card_7.setPixmap(QPixmap(self.dealer_cards[1]))
            self.card_8.setPixmap(QPixmap(self.dealer_cards[2]))
            self.card_9.setPixmap(QPixmap(self.dealer_cards[3]))
        elif length == 5:
            self.card_7.setPixmap(QPixmap(self.dealer_cards[1]))
            self.card_8.setPixmap(QPixmap(self.dealer_cards[2]))
            self.card_9.setPixmap(QPixmap(self.dealer_cards[3]))
            self.card_10.setPixmap(QPixmap(self.dealer_cards[4]))
        self.Winner()
        self.Track_records()
    
    # define method for again button:
    def Play_Again(self):
        self.card_1.setPixmap(QPixmap("back.jpg"))
        self.card_2.setPixmap(QPixmap("back.jpg"))
        self.card_3.setPixmap(QPixmap("back.jpg"))
        self.card_4.setPixmap(QPixmap("back.jpg"))
        self.card_5.setPixmap(QPixmap("back.jpg"))
        self.card_6.setPixmap(QPixmap("back.jpg"))
        self.card_7.setPixmap(QPixmap("back.jpg"))
        self.card_8.setPixmap(QPixmap("back.jpg"))
        self.card_9.setPixmap(QPixmap("back.jpg"))
        self.card_10.setPixmap(QPixmap("back.jpg"))

        self.all_cards = [item for item in card_list]
        self.player_cards = []
        self.dealer_cards = []
        self.player_score = 0
        self.dealer_score = 0
        self.boom = 3
        self.big = 8

        self.start_button.setEnabled(True)
        self.take_button.setEnabled(False)
        self.result_label.setText("")
        self.player_label.setText("")
        self.dealer_label.setText("")

    # define method for save button:
    def Save_results(self):
        # player name:
        teqsti = self.head_label.text()
        player_name = teqsti.split(" ")
        pl_score = self.ps_label.text()
        dl_score = self.ds_label.text()

        conn = sqlite3.connect("chincharito.db")
        curr = conn.cursor()
        curr.execute(f'''INSERT INTO outcome VALUES('{player_name[-1]}','{pl_score}','{dl_score}')''')
        conn.commit()
        conn.close()
    
    # define method for see button:
    def See_Statistics(self):
        secret = self.head_label.text()
        self.window_outcome = QMainWindow()
        self.iron = IronMan()
        self.iron.secret_label.setText(f"{secret}")
        self.close()

# -------------------------------------------- end- ---------------------------------------- #

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ali = Muhammad_Ali()
    sys.exit(app.exec_())