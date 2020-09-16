#!/usr/bin/env python3

"""
Gui interface for the application
"""

import sys
import webbrowser

from contextlib import redirect_stdout
from io import StringIO

from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, \
                              QActionGroup, QMessageBox, \
                              QAction, QPlainTextEdit

from PySide2.QtCore import Signal, QThread, Qt
from PySide2.QtGui import QFont, QStandardItemModel, QStandardItem, QIcon, \
                          QPixmap, QColor

from pycovering.qt_gui.ui_main import Ui_MainWindow
from pycovering.qt_gui.ui_about import Ui_Dialog
from pycovering.qt_gui.ui_2d_dimensions import Ui_TwoDDimensionsDialog
from pycovering.qt_gui.ui_pyramid_dimensions import Ui_PyramidDimensionsDialog
from pycovering.qt_gui.ui_block_size_dialog import Ui_BlockSizeDialog
from pycovering.qt_gui.ui_covering_dialog import Ui_CoveringDialog
from pycovering.qt_gui.ui_text_view import Ui_TextViewDialog

from pycovering.models import GeneralCoveringModel, TwoDCoveringModel, \
                              PyramidCoveringModel, CoveringTimeoutException, \
                              ImpossibleToFinishException, \
                              CoveringStoppedException, Block

from pycovering.views import GeneralView, TwoDPrintView, PyramidPrintView, \
                             PyramidVisualView, TwoDVisualView

from pycovering.constraints import PathConstraintWatcher, \
                                   PlanarConstraintWatcher


def parented_decorator(cls, parent):
    """
    This function takes (typically) a QDialog subclass
    and implicitly passes `parent` as the dialog parent
    in constructor
    """
    class Wrapper(cls):
        """
        This is the new class `cls` is turned into.
        """
        def __init__(self):
            super().__init__(parent)

    return Wrapper


def text_view_decorator(cls, parent):
    """
    This function takes a view class that prints to stdout
    and turns it into a function that shows the output in a dialog

    `cls` is the class to be decorated, `parent` is the main GUI
    window, so that it will be set as parent of the created dialog
    """
    class Wrapper(QDialog, Ui_TextViewDialog, cls):
        """
        This is the new class `cls` is turned into.

        We're subclassing `cls` so that `isinstance(view, cls)` is True.
        """
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
    """
    A thread in which the `model.try_cover` function
    is run (asynchronously)
    """
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
            self.model.reset()
            self.stopped.emit()
            self.done.emit()
        except (CoveringTimeoutException, ImpossibleToFinishException):
            self.model.reset()  # Don't keep a half-covered model
            self.failed.emit()
            self.done.emit()


class BlockListModel(QStandardItemModel):
    """
    Qt MVC model for the block list view (QListView)
    """
    BLOCK_ROLE = Qt.UserRole
    ICON_SIZE = 100

    checkedChanged = Signal(Block, bool)

    def __init__(self):
        super().__init__()
        self.itemChanged.connect(self._emit_checked_changed)

    @classmethod
    def color_icon(cls, color):
        """
        Creates a one-color QIcon from (R, G, B) tuple
        """
        r, g, b = color

        qcolor = QColor(r, g, b)
        pixmap = QPixmap(cls.ICON_SIZE, cls.ICON_SIZE)
        pixmap.fill(qcolor)
        icon = QIcon(pixmap)
        return icon

    def update_data(self, covering_model):
        """
        Reinserts all covering model blocks
        in the MVC model
        """
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
                color = block.color
                icon = self.color_icon(color)

                item.setCheckState(checkstate)
                item.setData(block, self.BLOCK_ROLE)
                item.setData(icon, Qt.DecorationRole)

                self.appendRow(item)

    def _emit_checked_changed(self, item):
        checked = item.checkState() == Qt.Checked
        block = item.data(self.BLOCK_ROLE)

        self.checkedChanged.emit(block, checked)


class AboutDialog(QDialog, Ui_Dialog):
    """
    Dialog with info about app
    """
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)


class CoveringDialog(QDialog, Ui_CoveringDialog):
    """
    Dialog showing during covering
    """
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)


class TwoDDimensionsDialog(QDialog, Ui_TwoDDimensionsDialog):
    """
    Dimension (height/width) selection dialog for TwoDCoveringModel
    """
    dimensionsAccepted = Signal(int, int)

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)
        self.accepted.connect(self.emit_data)

    def set_values(self, width, height):
        """
        This is used to set dialog initial values
        """
        self.widthSpinBox.setValue(width)
        self.heightSpinBox.setValue(height)

    def emit_data(self):
        """
        Emit `dimensionsAccepted(width, height)` signal
        """
        width = self.widthSpinBox.value()
        height = self.heightSpinBox.value()

        self.dimensionsAccepted.emit(width, height)


class PyramidDimensionsDialog(QDialog, Ui_PyramidDimensionsDialog):
    """
    Dimensions (size) selection dialog for PyramidCoveringModel
    """
    dimensionsAccepted = Signal(int)

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)
        self.accepted.connect(self.emit_data)

    def set_value(self, size):
        """
        This is used to set dialog initial values
        """
        self.sizeSpinBox.setValue(size)

    def emit_data(self):
        """
        Emit `dimensionsAccepted(size)` signal
        """
        size = self.sizeSpinBox.value()

        self.dimensionsAccepted.emit(size)


class BlockSizeDialog(QDialog, Ui_BlockSizeDialog):
    """
    A block size choosing dialog (common for all models)
    """
    sizesAccepted = Signal(int, int)

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setupUi(self)

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
        """
        This is used to set dialog initial values
        """
        self.minBlockSizeSpinBox.setValue(min_val)
        self.maxBlockSizeSpinBox.setValue(max_val)

    def emit_data(self):
        """
        Emit `sizesAccepted(minBlockSize, maxBlockSize)` signal
        """
        min_val = self.minBlockSizeSpinBox.value()
        max_val = self.maxBlockSizeSpinBox.value()

        self.sizesAccepted.emit(min_val, max_val)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    The main GUI window
    """
    HELP_URL = "https://www.github.com/jakoma02/pyCovering"

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
            self.start_covering)

        self.model_type_changed.connect(self.update_model_type)
        self.model_type_changed.connect(self.update_view_type_menu)
        self.model_type_changed.connect(self.update_constraints_menu)
        self.model_type_changed.connect(self.enable_model_menu_buttons)

        self.model_changed.connect(
            lambda _: self.info_updated.emit(self.model, self.view))

        self.view_type_changed.connect(self.update_view_type)

        self.view_changed.connect(
            lambda _: self.info_updated.emit(self.model, self.view))
        self.info_updated.connect(self.infoText.update)
        self.info_updated.connect(self.update_view)

        self.tiles_list_model = BlockListModel()
        self.tilesList.setModel(self.tiles_list_model)

        self.model_changed.connect(self.tiles_list_model.update_data)
        self.tiles_list_model.checkedChanged.connect(self.set_block_visibility)

        self.model_changed.emit(self.model)
        self.update_view_type_menu()

    def set_block_visibility(self, block, visible):
        """
        Update model visibility based on block list checkbox change
        """
        block.visible = visible
        self.model_changed.emit(self.model)

    def show_about_dialog(self):
        """
        Shows the "About" dialog
        """
        dialog = AboutDialog(self)
        dialog.open()

    def start_covering(self):
        """
        Starts covering, shows the corresponding dialog
        """
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
        """
        Shows "Change block size" dialog
        """
        if self.model is None:
            QMessageBox.warning(self, "No model", "No model selected!")
            return

        curr_min = self.model.min_block_size
        curr_max = self.model.max_block_size

        dialog = BlockSizeDialog(self)
        dialog.sizesAccepted.connect(self.block_sizes_accepted)
        dialog.set_values(curr_min, curr_max)
        dialog.open()

    def show_dimensions_dialog(self):
        """
        Shows "Change dimensions" dialog
        """
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

    def two_d_dimensions_accepted(self, width, height):
        """
        Updates TwoDCoveringModel dimensions (after dialog confirmation)
        """
        assert isinstance(self.model, TwoDCoveringModel)

        self.model.set_size(width, height)
        self.model_changed.emit(self.model)

        self.message("Size updated")

    def pyramid_dimensions_accepted(self, size):
        """
        Updates PyramidCoveringModel dimensions (after dialog confirmation)
        """
        assert isinstance(self.model, PyramidCoveringModel)

        # PyLint doesn't know that this is a `PyramidCoveringModel`
        # and not a `TwoDCoveringModel`
        # pylint: disable=no-value-for-parameter
        self.model.set_size(size)
        self.model_changed.emit(self.model)

        self.message("Size updated")

    def block_sizes_accepted(self, min_val, max_val):
        """
        Updates covering model block size (after dialog confirmation)
        """
        assert self.model is not None

        self.model.set_block_size(min_val, max_val)
        self.model_changed.emit(self.model)

        self.message("Block size updated")

    @staticmethod
    def update_view(model, view):
        """
        Refreshes contents of given view
        """
        if view is None:
            return
        if model is not None and model.is_filled():
            view.show(model)
        else:
            view.close()

    def message(self, msg):
        """
        Shows a log message in the "Messages" window
        """
        self.messagesText.add_message(msg)

    def show_help(self):
        """
        Opens a webpage with help
        """
        webbrowser.open(self.HELP_URL)

    def create_action_groups(self):
        """
        Groups exclusive choice menu buttons in action groups.

        This should ideally be done in UI files, but Qt designer
        doesn't support it.
        """
        self.model_type_group = QActionGroup(self)
        self.model_type_group.addAction(self.action2D_Rectangle_2)
        self.model_type_group.addAction(self.actionPyramid_2)

        self.view_type_group = QActionGroup(self)

        self.model_type_group.triggered.connect(self.model_type_changed)
        self.view_type_group.triggered.connect(self.view_type_changed)

    def update_model_type(self):
        """
        Sets the current model after model type changed in menu
        """
        selected_model = self.model_type_group.checkedAction()

        if selected_model == self.action2D_Rectangle_2:
            model = TwoDCoveringModel(10, 10, 4, 4)
        elif selected_model == self.actionPyramid_2:
            model = PyramidCoveringModel(10, 4, 4)
        else:
            model = None

        self.model = model
        self.model_changed.emit(model)
        self.message("Model type updated")

    def enable_model_menu_buttons(self):
        """
        Enable menu buttons that are disabled at program start
        """
        self.actionChange_dimensions.setEnabled(True)
        self.actionChange_tile_size.setEnabled(True)
        self.actionGenerate.setEnabled(True)

    def update_view_type(self):
        """
        Sets the current view after view type changed in menu
        """
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
        """
        Stops ongoing covering
        """
        if self.thread.isRunning():
            # The thread is being terminated
            self.model.stop_covering()
            self.message("Covering terminated")

    def covering_success(self):
        """
        Prints a success log message (for now)
        """
        self.message("Covering successful")

    def covering_failed(self):
        """
        Prints a fail log message and shows an error window (for now)
        """
        self.message("Covering failed")
        QMessageBox.critical(self, "Failed", "Covering failed")

    def model_views(self, model):
        """
        Returns a list of tuples for all views
        for given mode as  (name, class)
        """

        if isinstance(model, TwoDCoveringModel):
            return [
                ("2D Print view", text_view_decorator(TwoDPrintView, self)),
                ("2D Visual view", parented_decorator(TwoDVisualView, self))
            ]

        if isinstance(model, PyramidCoveringModel):
            return [
                ("Pyramid Print view",
                 text_view_decorator(PyramidPrintView, self)),
                ("Pyramid Visual view", PyramidVisualView)
            ]

        return []

    @staticmethod
    def model_constraints(model):
        """
        Returns a list of tuples for all constraint watchers
        for given mode as  (name, class)
        """

        if isinstance(model, TwoDCoveringModel):
            return [
                ("Path blocks", PathConstraintWatcher)
            ]

        if isinstance(model, PyramidCoveringModel):
            return [
                ("Path blocks", PathConstraintWatcher),
                ("Planar blocks", PlanarConstraintWatcher)
            ]

        return []

    def update_view_type_menu(self):
        """
        Updates options for view type menu afted model type change
        """
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

    def watcher_set_active(self, constraint, value):
        """
        A slot, activate/deactivate constraint depending on value (True/False)
        """

        if value is True:
            self.model.add_constraint(constraint)
        else:
            self.model.remove_constraint(constraint)

        self.model_changed.emit(self.model)
        self.message("Constraint settings changed")

    def update_constraints_menu(self):
        """
        Updates options for model constraints after model type change
        """

        cstr_menu = self.menuConstraints
        cstr_menu.clear()

        all_constraints = self.model_constraints(self.model)

        for name, watcher in all_constraints:
            action = QAction(self)
            action.setText(name)
            action.setCheckable(True)

            action.toggled.connect(lambda val, watcher=watcher:
                                   self.watcher_set_active(watcher, val))

            cstr_menu.addAction(action)

        cstr_menu.setEnabled(True)

    def close(self):
        """
        While closing the window also closes the view
        """
        if self.view is not None:
            self.view.close()

        super().close()


def main():
    """
    This is the app entrypoint.
    """
    app = QApplication()
    main_window = MainWindow()
    app.lastWindowClosed.connect(main_window.close)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
