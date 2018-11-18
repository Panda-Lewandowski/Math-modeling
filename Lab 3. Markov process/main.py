import sys
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QListWidgetItem
import markov

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("window.ui", self)
        self.ui.tableWidgetMatrix.horizontalHeader().setDefaultSectionSize(30)
        self.tableWidgetMatrix.itemChanged.connect(lambda x: self._item_changed(x))
        self.spinBoxStatesCount.setValue(3)

    def _item_changed(self, value):
        try:
            if value.text() != "":
                float(value.text())
        except ValueError:
            QtWidgets.QMessageBox.critical(None, "Invalid input", "Please, enter a float number!")
            value.setText("")

    @pyqtSlot()
    def on_pushButtonSolve_clicked(self):
        table = self._get_matrix_from_table()
        self.ui.listWidgetSolution.clear()
        i = 1
        result = markov.get_system_times(table)
        print(result)
        if len(result) == 0:
            QtWidgets.QMessageBox.critical(None, "Invalid input", "Please, enter correct intensities!")
        else:
            for state in result:
                QListWidgetItem("{n}: {time:0.5f}".format(n = i, time = round(state, 5)), self.ui.listWidgetSolution)
                i += 1

    @pyqtSlot('int')
    def on_spinBoxStatesCount_valueChanged(self, value):
        self.ui.tableWidgetMatrix.setRowCount(value)
        self.ui.tableWidgetMatrix.setColumnCount(value)
        self.ui.tableWidgetMatrix.clearContents()

    def _get_matrix_from_table(self):
        res = []
        try:
            for i in range(self.ui.tableWidgetMatrix.rowCount()):
                row = []
                for j in range(self.ui.tableWidgetMatrix.columnCount()):
                    val = self.ui.tableWidgetMatrix.item(i, j).text() if self.ui.tableWidgetMatrix.item(i, j) else "0"
                    row.append(float(val))
                res.append(row)
        except ValueError:
            QtWidgets.QMessageBox.critical(None, "Invalid input", "Please, enter a float number!")
        return res

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
