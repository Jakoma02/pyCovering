"""
One-class module, see `TwoDVisualWidget`
"""

from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QRect, Qt
from PySide2.QtGui import QPainter, QBrush, QColor

from pycovering.models import Block


class TwoDVisualWidget(QWidget):
    """
    A widget visually showing the state of TwoDCoveringModule,
    being the core of TwoDVisualView
    """
    START_X, START_Y = 0, 0

    def __init__(self, parent=None):
        self.model = None
        QWidget.__init__(self, parent)

    def show(self, model):
        self.model = model
        self.repaint()

    # pylint: disable=too-many-locals
    def paintEvent(self, _):
        """
        Paints the widget contents
        """
        painter = QPainter(self)

        device = painter.device()

        optimal_vertical_tile_size = device.height() // self.model.height
        optimal_horizontal_tile_size = device.width() // self.model.width

        tile_size = min(optimal_vertical_tile_size,
                        optimal_horizontal_tile_size)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        for pos in self.model.all_positions():
            block = self.model.state[pos]

            if block is Block.EMPTY:
                continue
            if not block.visible:
                continue

            r, g, b = block.color
            q_color = QColor(r, g, b)
            brush.setColor(q_color)

            x, y = pos
            canvas_x = self.START_X + tile_size * x
            canvas_y = self.START_Y + tile_size * y

            rect = QRect(canvas_x, canvas_y, tile_size, tile_size)
            painter.fillRect(rect, brush)

        painter.end()
