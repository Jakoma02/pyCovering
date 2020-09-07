import sys
import webbrowser

from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, \
                              QActionGroup, QTextEdit, QMessageBox
from PySide2.QtCore import Signal, QThread

from ui_main import Ui_MainWindow
from ui_about import Ui_Dialog
from ui_2d_dimensions import Ui_TwoDDimensionsDialog
from ui_pyramid_dimensions import Ui_PyramidDimensionsDialog
from ui_block_size_dialog import Ui_BlockSizeDialog
from ui_covering_dialog import Ui_CoveringDialog

from covering.models import GeneralCoveringModel, TwoDCoveringModel, \
                            PyramidCoveringModel, CoveringTimeoutException, \
                            ImpossibleToFinishException, \
                            CoveringStoppedException


class GenerateModelThread(QThread):
    success = Signal()
    failed = Signal()

    def __init__(self, model):
        self.model = model

        super().__init__()

    def run(self):
        self.model.reset()
        try:
            self.model.try_cover()
            self.success.emit()
        except (CoveringTimeoutException, ImpossibleToFinishException,
                CoveringStoppedException):
            self.failed.emit()


class AboutDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)


class CoveringDialog(QDialog, Ui_CoveringDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)


class TwoDDimensionsDialog(QDialog, Ui_TwoDDimensionsDialog):
    dimensionsAccepted = Signal(int, int)

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)
        self.accepted.connect(self.emit_data)

    def set_values(self, width, height):
        self.widthSpinBox.setValue(width)
        self.heightSpinBox.setValue(height)

    def emit_data(self):
        width = self.widthSpinBox.value()
        height = self.heightSpinBox.value()

        self.dimensionsAccepted.emit(width, height)


class PyramidDimensionsDialog(QDialog, Ui_PyramidDimensionsDialog):
    dimensionsAccepted = Signal(int)

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)
        self.accepted.connect(self.emit_data)

    def set_value(self, size):
        self.sizeSpinBox.setValue(size)

    def emit_data(self):
        size = self.sizeSpinBox.value()

        self.dimensionsAccepted.emit(size)


class BlockSizeDialog(QDialog, Ui_BlockSizeDialog):
    sizesAccepted = Signal(int, int)

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)

        # TODO: Fix box width change

        self.minBlockSizeSpinBox.valueChanged.connect(
                self.maxBlockSizeSpinBox.setMinimum)
        self.maxBlockSizeSpinBox.valueChanged.connect(
                self.minBlockSizeSpinBox.setMaximum)

        min_val = self.minBlockSizeSpinBox.value()
        max_val = self.maxBlockSizeSpinBox.value()

        # Update bounds
        self.minBlockSizeSpinBox.valueChanged.emit(min_val)
        self.maxBlockSizeSpinBox.valueChanged.emit(max_val)

        self.accepted.connect(self.emit_data)

    def set_values(self, min_val, max_val):
        self.minBlockSizeSpinBox.setValue(min_val)
        self.maxBlockSizeSpinBox.setValue(max_val)

    def emit_data(self):
        min_val = self.minBlockSizeSpinBox.value()
        max_val = self.maxBlockSizeSpinBox.value()

        self.sizesAccepted.emit(min_val, max_val)


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

        self.actionAbout_2.triggered.connect(self.show_about_dialog)
        self.actionDocumentation.triggered.connect(self.show_help)
        self.actionChange_dimensions.triggered.connect(
                self.show_dimensions_dialog)
        self.actionChange_tile_size.triggered.connect(
                self.show_block_size_dialog)

        self.actionGenerate.triggered.connect(
                self.show_covering_dialog)

        self.model_type_changed.connect(self.update_model_type)
        self.model_changed.connect(self.infoText.update)

        self.model_changed.emit(self.model)

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.open()

    def show_covering_dialog(self):
        if self.model is None:
            QMessageBox.warning(self, "No model", "No model selected!")
            return

        self.thread = GenerateModelThread(self.model)
        dialog = CoveringDialog(self)

        dialog.finished.connect(self.cancel_covering)

        self.thread.success.connect(dialog.close)
        self.thread.failed.connect(dialog.close)

        self.thread.start()
        dialog.open()


    def show_block_size_dialog(self):
        if self.model is None:
            QMessageBox.warning(self, "No model", "No model selected!")
            return

        curr_min = self.model.min_block_size
        curr_max = self.model.max_block_size

        dialog = BlockSizeDialog(self)
        dialog.sizesAccepted.connect(self.block_sizes_accepted)
        dialog.set_values(curr_min, curr_max)
        dialog.open()

    def two_d_dimensions_accepted(self, width, height):
        assert isinstance(self.model, TwoDCoveringModel)

        self.model.set_size(width, height)
        self.model_changed.emit(self.model)

    def pyramid_dimensions_accepted(self, size):
        assert isinstance(self.model, PyramidCoveringModel)

        self.model.set_size(size)
        self.model_changed.emit(self.model)

    def block_sizes_accepted(self, min_val, max_val):
        assert self.model is not None

        self.model.set_block_size(min_val, max_val)
        self.model_changed.emit(self.model)

    def show_dimensions_dialog(self):
        if self.model is None:
            QMessageBox.warning(self, "No model", "No model selected!")
            return

        if isinstance(self.model, TwoDCoveringModel):
            curr_width = self.model.width
            curr_height = self.model.height

            dialog = TwoDDimensionsDialog(self)
            dialog.set_values(curr_width, curr_height)

            dialog.dimensionsAccepted.connect(self.two_d_dimensions_accepted)
            dialog.show()

        elif isinstance(self.model, PyramidCoveringModel):
            curr_size = self.model.size

            dialog = PyramidDimensionsDialog(self)
            dialog.set_value(curr_size)

            dialog.dimensionsAccepted.connect(self.pyramid_dimensions_accepted)
            dialog.show()


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

    def cancel_covering(self):
        self.model.stop_covering()


if __name__ == "__main__":
    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
