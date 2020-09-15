"""
A single-class module, see the MessageBox class
"""

from collections import deque
from datetime import datetime

from PySide2.QtWidgets import QTextEdit


class MessageBox(QTextEdit):
    """
    A QTextEdit subclass for displaying log messages.

    It is designed to automatically scroll down only if
    it is already scrolled down
    """
    # This helped with auto scrolling down: https://stackoverflow.com/questions
    # /14550146/textedit-scroll-down-automatically-only-if-the-scrollbar-is-at-the-bottom

    MAX_MESSAGES = 100
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, parent):
        super().__init__(parent)

        self._messages = deque()
        self._update_text()

    def add_message(self, msg):
        """
        Prints a new message in the message area
        """
        if len(self._messages) == self.MAX_MESSAGES:
            self._messages.popleft()

        now = datetime.now()
        time_str = now.strftime(self.TIME_FORMAT)

        complete_msg = f"[{time_str}] {msg}"

        self._messages.append(complete_msg)
        self._update_text()

    def is_scrolled_down(self):
        """
        Returns True if the scrollbar is at the lowest possible position
        """
        scrollbar = self.verticalScrollBar()
        return scrollbar.value() == scrollbar.maximum()

    def scroll_down(self):
        """
        Move the scrollbar to lowest possible position
        """
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _update_text(self):
        was_scrolled_down = self.is_scrolled_down()
        scrollbar = self.verticalScrollBar()
        old_scroll_value = scrollbar.value()

        text = "\n".join(self._messages)
        self.setPlainText(text)

        if was_scrolled_down:
            self.scroll_down()
        else:
            # Don't scroll up
            scrollbar.setValue(old_scroll_value)
