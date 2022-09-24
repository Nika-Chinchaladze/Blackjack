from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QFrame, QRadioButton
from PyQt5 import uic
from BlackJack import Muhammad_Ali

class SpiderMan(QMainWindow):
    def __init__(self):
        super(SpiderMan, self).__init__()
        uic.loadUi("enter.ui", self)

        # define content:
        self.hello_label = self.findChild(QLabel, "hello_label")
        self.app_label = self.findChild(QLabel, "app_label")
        self.against_label = self.findChild(QLabel, "against_label")
        self.name_label = self.findChild(QLabel, "name_label")

        self.line_1 = self.findChild(QFrame, "line_1")
        self.line_2 = self.findChild(QFrame, "line_2")
        self.frame_1 = self.findChild(QFrame, "frame_1")
        self.frame_2 = self.findChild(QFrame, "frame_2")
        self.frame_3 = self.findChild(QFrame, "frame_3")

        self.team_button = self.findChild(QRadioButton, "team_button")
        self.ind_button = self.findChild(QRadioButton, "ind_button")
        self.other_button = self.findChild(QRadioButton, "other_button")
        self.dealer_button = self.findChild(QRadioButton, "dealer_button")

        self.go_button = self.findChild(QPushButton, "go_button")
        self.name_line = self.findChild(QLineEdit, "name_line")

        # call defined method from here:
        self.go_button.clicked.connect(self.Go_Game)


        self.show()

# -------------------------------------- logic ---------------------------------------- #
    # define method for go button:
    def Go_Game(self):
        user_name = self.name_line.text()
        if len(user_name) > 0:
            self.window_game = QMainWindow()
            self.ali = Muhammad_Ali()
            self.ali.head_label.setText(f"BlackJack: Dealer VS {user_name}")
            self.close()
        else:
            None

# --------------------------------------- end ----------------------------------------- #

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    man = SpiderMan()
    sys.exit(app.exec_())