import sys
import webbrowser

from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QActionGroup
from ui_main import Ui_MainWindow
from ui_about import Ui_Dialog

class AboutDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)

class MainWindow(QMainWindow, Ui_MainWindow):
    HELP_URL = "https://www.github.com/jakoma02/covering"

    def __init__(self):
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.create_action_groups()

        self.actionAbout_2.triggered.connect(self.show_dialog)
        self.actionDocumentation.triggered.connect(self.show_help)

    def show_dialog(self):
        dialog = AboutDialog(self)
        dialog.open()

    def show_help(self):
        webbrowser.open(self.HELP_URL)

    def create_action_groups(self):
        self.action2D_Rectangle.setCheckable(True)
        self.actionPyramid.setCheckable(True)

        self.model_type_group = QActionGroup(self)
        self.model_type_group.addAction(self.action2D_Rectangle)
        self.model_type_group.addAction(self.actionPyramid)


if __name__ == "__main__":
    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
