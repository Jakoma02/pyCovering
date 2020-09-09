import sys
import webbrowser

from contextlib import redirect_stdout
from io import StringIO

from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, \
                              QActionGroup, QTextEdit, QMessageBox, \
                              QAction, QPlainTextEdit

from PySide2.QtCore import Signal, QThread, Qt
from PySide2.QtGui import QFont, QStandardItemModel, QStandardItem

from ui_main import Ui_MainWindow
from ui_about import Ui_Dialog
from ui_2d_dimensions import Ui_TwoDDimensionsDialog
from ui_pyramid_dimensions import Ui_PyramidDimensionsDialog
from ui_block_size_dialog import Ui_BlockSizeDialog
from ui_covering_dialog import Ui_CoveringDialog
from ui_text_view import Ui_TextViewDialog

from covering.models import GeneralCoveringModel, TwoDCoveringModel, \
                            PyramidCoveringModel, CoveringTimeoutException, \
                            ImpossibleToFinishException, \
                            CoveringStoppedException, Block

from covering.views import GeneralView, TwoDPrintView, PyramidPrintView, \
                           PyramidVisualView

def text_view_decorator(cls, parent):
    class Wrapper(QDialog, Ui_TextViewDialog, cls):
        # We're subclassing `cls` so that isinstance(view, cls) is True
        _show = QDialog.show
        _close = QDialog.close

        def __init__(self):
            QDialog.__init__(self, parent)
            self.setupUi(self)

            self.showing = False

            font = QFont("Courier")
            self.setFont(font)
            self.outputText.setLineWrapMode(QPlainTextEdit.NoWrap)

            self.wrapped = cls()
            self.accepted.connect(self.close)

        def show(self, model):
            if not self.showing:
                self._show()
                self.showing = True

            output_io = StringIO()

            with redirect_stdout(output_io):
                self.wrapped.show(model)

            out_str = output_io.getvalue()
            self.outputText.setPlainText(out_str)
            output_io.close()

        def close(self):
            self.wrapped.close()
            self._close()
            self.showing = False

    return Wrapper


class GenerateModelThread(QThread):
    success = Signal()
    failed = Signal()
    stopped = Signal()
    done = Signal()

    def __init__(self, model):
        self.model = model

        super().__init__()

    def run(self):
        try:
            self.model.try_cover()
            self.success.emit()
            self.done.emit()
        except CoveringStoppedException:
            self.stopped.emit()
            self.done.emit()
        except (CoveringTimeoutException, ImpossibleToFinishException):
            self.failed.emit()
            self.done.emit()


class BlockListModel(QStandardItemModel):
    BLOCK_ROLE = Qt.UserRole

    checkedChanged = Signal(Block, bool)

    def __init__(self):
        super().__init__()
        self.itemChanged.connect(self._emit_checked_changed)

    def update_data(self, covering_model):
        self.clear()

        if covering_model is not None:
            for block in covering_model.blocks:
                block_str = f"Block {block.number}"
                item = QStandardItem(block_str)
                item.setFlags(
                        Qt.ItemIsUserCheckable |
                        Qt.ItemIsSelectable |
                        Qt.ItemIsEnabled
                )
                checkstate = Qt.Checked if block.visible else Qt.Unchecked
                item.setCheckState(checkstate)
                item.setData(block, self.BLOCK_ROLE)
                self.appendRow(item)

    def _emit_checked_changed(self, item):
        checked = item.checkState() == Qt.Checked
        block = item.data(self.BLOCK_ROLE)

        self.checkedChanged.emit(block, checked)


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
    view_type_changed = Signal()
    model_changed = Signal(GeneralCoveringModel)
    view_changed = Signal(GeneralView)
    info_updated = Signal(GeneralCoveringModel, GeneralView)
    settings_changed = Signal()

    def __init__(self):
        QMainWindow.__init__(self)

        self.model = None
        self.view = None

        self.setupUi(self)
        self.create_action_groups()

        # A dict Action name -> GeneralView, so that we can set the
        # correct view upon view type action trigger
        self.action_views = dict()

        self.actionAbout_2.triggered.connect(self.show_about_dialog)
        self.actionDocumentation.triggered.connect(self.show_help)
        self.actionChange_dimensions.triggered.connect(
                self.show_dimensions_dialog)
        self.actionChange_tile_size.triggered.connect(
                self.show_block_size_dialog)

        self.actionGenerate.triggered.connect(
                self.show_covering_dialog)

        self.model_type_changed.connect(self.update_model_type)
        self.model_type_changed.connect(self.update_view_type_menu)
        self.model_changed.connect(
                lambda _: self.info_updated.emit(self.model, self.view))

        self.view_type_changed.connect(self.update_view_type)

        self.view_changed.connect(
                lambda _: self.info_updated.emit(self.model, self.view))
        self.info_updated.connect(self.infoText.update)
        self.info_updated.connect(self.update_view)

        self.tilesListModel = BlockListModel()
        self.tilesList.setModel(self.tilesListModel)

        self.model_changed.connect(self.tilesListModel.update_data)
        self.tilesListModel.checkedChanged.connect(self.set_block_visibility)

        self.model_changed.emit(self.model)
        self.update_view_type_menu()

    def set_block_visibility(self, block, visible):
        block.visible = visible
        self.model_changed.emit(self.model)

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.open()

    def show_covering_dialog(self):
        if self.model is None:
            QMessageBox.warning(self, "No model", "No model selected!")
            return

        self.model.reset()

        self.thread = GenerateModelThread(self.model)
        dialog = CoveringDialog(self)

        dialog.rejected.connect(self.cancel_covering)

        self.thread.success.connect(dialog.accept)
        self.thread.success.connect(self.covering_success)
        self.thread.failed.connect(dialog.reject)
        self.thread.failed.connect(self.covering_failed)

        self.thread.done.connect(
                lambda: self.model_changed.emit(self.model))

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

        self.message("Size updated")

    def pyramid_dimensions_accepted(self, size):
        assert isinstance(self.model, PyramidCoveringModel)

        self.model.set_size(size)
        self.model_changed.emit(self.model)

        self.message("Size updated")

    def update_view(self, model, view):
        if view is None:
            return
        if model is not None and model.is_filled():
            view.show(model)
        else:
            view.close()

    def block_sizes_accepted(self, min_val, max_val):
        assert self.model is not None

        self.model.set_block_size(min_val, max_val)
        self.model_changed.emit(self.model)

        self.message("Block size updated")

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

    def message(self, msg):
        self.messagesText.add_message(msg)

    def show_help(self):
        webbrowser.open(self.HELP_URL)

    def create_action_groups(self):
        self.model_type_group = QActionGroup(self)
        self.model_type_group.addAction(self.action2D_Rectangle_2)
        self.model_type_group.addAction(self.actionPyramid_2)

        self.view_type_group = QActionGroup(self)

        self.model_type_group.triggered.connect(self.model_type_changed)
        self.view_type_group.triggered.connect(self.view_type_changed)

    def update_model_type(self):
        selected_model = self.model_type_group.checkedAction()

        if selected_model == self.action2D_Rectangle_2:
            model = TwoDCoveringModel(10, 10, 4, 4)
        elif selected_model == self.actionPyramid_2:
            model = PyramidCoveringModel(10, 4, 4)
        else:
            model = None

        # TODO: Fix that GUI doesn't show view is none immediately
        self.model = model

        self.model_changed.emit(model)

        self.message("Model type updated")

    def update_view_type(self):
        if self.view is not None:
            self.view.close()

        selected_action = self.view_type_group.checkedAction()
        
        if selected_action is None:
            # Model was probably changed
            self.view = None
        else:
            action_name = selected_action.objectName()
            selected_view = self.action_views[action_name]

            self.view = selected_view()  # New instance of that view

            self.message("View type updated")

        self.view_changed.emit(self.view)

    def cancel_covering(self):
        if self.thread.isRunning():
            # The thread is being terminated
            self.model.stop_covering()
            self.message("Covering terminated")

    def covering_success(self):
        self.message("Covering successful")

    def covering_failed(self):
        self.message("Covering failed")
        QMessageBox.critical(self, "Failed", "Covering failed")

    def model_views(self, model):
        """
        Returns a list of tuples for all views
        for given mode as  (name, class)
        """

        if isinstance(model, TwoDCoveringModel):
            return [
                ("Print view", text_view_decorator(TwoDPrintView, self)),
            ]

        if isinstance(model, PyramidCoveringModel):
            return [
                    ("Print view",
                        text_view_decorator(PyramidPrintView, self)),
                    ("Visual view", PyramidVisualView)
            ]

        return []


    def update_view_type_menu(self):
        view_type_menu = self.menuType_2
        view_type_menu.clear()

        for action in self.view_type_group.actions():
            self.view_type_group.removeAction(action)

        all_views = self.model_views(self.model)

        if not all_views:
            # Likely no model selected
            view_type_menu.setEnabled(False)
            return

        view_type_menu.setEnabled(True)

        self.action_views.clear()

        for i, view_tuple in enumerate(all_views):
            name, view = view_tuple

            # As good as any, we just need to distinguish the actions
            action_name = f"Action{i}"

            action = QAction(self)
            action.setText(name)
            action.setCheckable(True)
            action.setObjectName(action_name)

            # So that we can later see which view should be activated
            self.action_views[action_name] = view
            view_type_menu.addAction(action)
            self.view_type_group.addAction(action)

        self.update_view_type()

    def close(self):
        if self.view is not None:
            self.view.close()


if __name__ == "__main__":
    app = QApplication()
    mainWindow = MainWindow()
    app.lastWindowClosed.connect(mainWindow.close)
    mainWindow.show()
    sys.exit(app.exec_())
