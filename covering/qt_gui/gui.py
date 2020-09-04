import sys
import webbrowser

from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, \
                              QActionGroup, QTextEdit
from PySide2.QtCore import Signal
from ui_main import Ui_MainWindow
from ui_about import Ui_Dialog

from covering.models import GeneralCoveringModel, TwoDCoveringModel, \
                            PyramidCoveringModel

class AboutDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)


class MainWindow(QMainWindow, Ui_MainWindow):
    HELP_URL = "https://www.github.com/jakoma02/covering"

    model_type_changed = Signal()
    model_changed = Signal(GeneralCoveringModel)
    settings_changed = Signal()

    def __init__(self):
        QMainWindow.__init__(self)

        self.model = None
        self.view = None

        self.setupUi(self)
        self.create_action_groups()

        self.actionAbout_2.triggered.connect(self.show_dialog)
        self.actionDocumentation.triggered.connect(self.show_help)

        self.model_type_changed.connect(self.update_model_type)
        self.model_changed.connect(self.infoText.update)

        self.model_changed.emit(self.model)

    def show_dialog(self):
        dialog = AboutDialog(self)
        dialog.open()

    def show_help(self):
        webbrowser.open(self.HELP_URL)

    def create_action_groups(self):
        self.model_type_group = QActionGroup(self)
        self.model_type_group.addAction(self.action2D_Rectangle_2)
        self.model_type_group.addAction(self.actionPyramid_2)

        self.model_type_group.triggered.connect(self.model_type_changed)

    def update_model_type(self):
        selected_model = self.model_type_group.checkedAction()

        if selected_model == self.action2D_Rectangle_2:
            model = TwoDCoveringModel(10, 10, 4, 4)
        elif selected_model == self.actionPyramid_2:
            model = PyramidCoveringModel(10, 4, 4)
        else:
            model = None

        self.model = model
        self.model_changed.emit(model)


if __name__ == "__main__":
    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
