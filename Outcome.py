from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import pandas as pd
import sqlite3


# connect database or create if not exist:
conn = sqlite3.connect("chincharito.db")
curr = conn.cursor()
curr.execute('''CREATE TABLE IF NOT EXISTS outcome(player text, wins text, loses text)''')
conn.commit()
conn.close()

class IronMan(QMainWindow):
    def __init__(self):
        super(IronMan, self).__init__()
        uic.loadUi("outcome.ui", self)

        # define content:
        self.back_button = self.findChild(QPushButton, "back_button")
        self.display_button = self.findChild(QPushButton, "display_button")
        self.exit_button = self.findChild(QPushButton, "exit_button")
        self.table_widget = self.findChild(QTableWidget, "table_widget")
        self.secret_label = self.findChild(QLabel, "secret_label")


        # call defined method from here:
        self.exit_button.clicked.connect(lambda: self.close())
        self.back_button.clicked.connect(self.Return_Back)
        self.display_button.clicked.connect(self.Show_outcome)

        self.show()

# -------------------------------------- logic ---------------------------------------- #
    # define method for back button:
    def Return_Back(self):
        quiet = self.secret_label.text()
        from BlackJack import Muhammad_Ali

        self.window_black = QMainWindow()
        self.ali = Muhammad_Ali()
        self.ali.head_label.setText(f"{quiet}")
        self.close()
    
    # define method for display_button:
    def Show_outcome(self):
        conn = sqlite3.connect("chincharito.db")
        curr = conn.cursor()
        basic_list = []
        for item in curr.execute('''SELECT * FROM outcome;'''):
            basic_list.append(list(item))
        conn.commit()
        conn.close()

        magic_frame = pd.DataFrame(basic_list, columns = ["Player", "Wins", "Loses"])
        RowNumber = len(magic_frame.index)
        ColumnNumber = len(magic_frame.columns)

        self.table_widget.setColumnCount(ColumnNumber)
        self.table_widget.setRowCount(RowNumber)
        self.table_widget.setHorizontalHeaderLabels(magic_frame.columns)

        for rows in range(RowNumber):
            for columns in range(ColumnNumber):
                self.table_widget.setItem(rows, columns, QTableWidgetItem(str(magic_frame.iat[rows, columns])))
                
# --------------------------------------- end ----------------------------------------- #

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    iron = IronMan()
    sys.exit(app.exec_())