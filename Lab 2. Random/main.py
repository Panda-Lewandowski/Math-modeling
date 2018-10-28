from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import scipy.stats as stats
import random
import math 
from itertools import islice

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.fill_alg.clicked.connect(lambda: on_fill_alg_click(self))
        self.fill_table.clicked.connect(lambda: on_fill_table_click(self))
        self.manual_input.returnPressed.connect(lambda: on_manual_input_enter(self))
        self.meas_alg_1.setReadOnly(True)
        self.meas_alg_2.setReadOnly(True)
        self.meas_alg_3.setReadOnly(True)
        self.meas_table_1.setReadOnly(True)
        self.meas_table_2.setReadOnly(True)
        self.meas_table_3.setReadOnly(True)
        self.meas_manual.setReadOnly(True)
        self.alg_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.line_num = 0

        for i in range(10):
            self.alg_table.insertRow(i)

        for i in range(10):
            self.table_table.insertRow(i)

def calculate_entropy(sequence):
    count = len(sequence) 
    if count == 0:
        return 0
    
    hist = dict()
    for el in sequence:
        if el not in hist.keys():
            hist.update({el: 1})
        else:
            hist[el] += 1
    
    entropy = 0
    for el in hist.keys():
        p = hist[el] / count
        entropy -= p * math.log(p, count)
    
    return entropy


def on_fill_alg_click(win):
    table = win.alg_table
    random.seed()
    one_digit = [random.randint(0, 9) for i in range(1000)]
    two_digits = [random.randint(10, 99) for i in range(1000)]
    three_digits = [random.randint(100, 999) for i in range(1000)]
    for i in range(10):
        item = QTableWidgetItem(str(one_digit[i]))
        table.setItem(i, 0, item)

    for i in range(10):
        item = QTableWidgetItem(str(two_digits[i]))
        table.setItem(i, 1, item)

    for i in range(10):
        item = QTableWidgetItem(str(three_digits[i]))
        table.setItem(i, 2, item)

    #table.resizeColumnsToContents()
    entropy_one = calculate_entropy(one_digit)
    entropy_two = calculate_entropy(two_digits) 
    entropy_three = calculate_entropy(three_digits)
    win.meas_alg_1.setText('{:.4%}'.format(entropy_one))
    win.meas_alg_2.setText('{:.4%}'.format(entropy_two))
    win.meas_alg_3.setText('{:.4%}'.format(entropy_three))
    

def on_fill_table_click(win):
    table = win.table_table
    numbers = set()
    with open('digits.txt') as file: 
        lines = islice(file, win.line_num, None)
        for l in lines:
            numbers.update(set(l.split(" ")[1:-1]))
            win.line_num += 1
            if len(numbers) >= 3001:
                break
        numbers.remove("") 
        numbers = list(numbers)[:3000]
    one_digit = [int(i)%9 + 1 for i in numbers[:1000]]
    two_digits = [int(i)%90 + 10 for i in numbers[1000:2000]]
    three_digits = [int(i)%900 + 100 for i in numbers[2000:3000]]
    
    for i in range(10):
        item = QTableWidgetItem(str(one_digit[i]))
        table.setItem(i, 0, item)

    for i in range(10):
        item = QTableWidgetItem(str(two_digits[i]))
        table.setItem(i, 1, item)

    for i in range(10):
        item = QTableWidgetItem(str(three_digits[i]))
        table.setItem(i, 2, item)

    entropy_one = calculate_entropy(one_digit)
    entropy_two = calculate_entropy(two_digits) 
    entropy_three = calculate_entropy(three_digits)
    win.meas_table_1.setText(' {:.4%}'.format(entropy_one))
    win.meas_table_2.setText(' {:.4%}'.format(entropy_two))
    win.meas_table_3.setText(' {:.4%}'.format(entropy_three))

def on_manual_input_enter(win):
    input = win.manual_input
    measure = win.meas_manual
    sequence = input.text().split(" ")
    filtered_sequence = []
    for i in sequence:
        try:
            int(i)
        except ValueError:
            continue
        else:
            filtered_sequence.append(i)

    entropy = calculate_entropy(list(map(lambda x: int(x), filtered_sequence)))
    win.meas_manual.setText(' {:.4%}'.format(entropy))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())