"""
This module contains the InfoBox and classes
responsible for formatting its output
"""

from PySide2.QtWidgets import QTextEdit
from covering import models, views


class Formatter:
    """
    An abstract class converting models/views
    to HTML markup
    """

    @classmethod
    def get_properties(cls, obj):
        """
        Returns a list of properties as [(name, val), (name, val), ...]

        This is used by the `format` method, each subclass needs
        to reimplement it
        """
        raise NotImplementedError

    @classmethod
    def format(cls, obj):
        """
        Formats an object (model/view), using its `get_properties` method
        """
        result_list = []

        properties = cls.get_properties(obj)

        first = True
        for name, val in properties:
            # First property is the title one
            offset = "&emsp;" if not first else ""
            first = False

            if val is None:
                val = "<span style='color:#aa0000'>none</span>"

            line = f"{offset}<b>{name}:</b> {val}"
            result_list.append(line)

        return "<br>".join(result_list)


class ModelFormatter(Formatter):
    """
    A Formatter abstract subclass for formatting models
    """
    MODEL_NAME = ""

    # pylint: disable=arguments-differ
    @classmethod
    def get_properties(cls, model):
        covered = model.is_filled()
        state = "Covered" if covered else "Not covered"

        return [
            ("Model name", cls.MODEL_NAME),
            ("Min block size", model.min_block_size),
            ("Max block size", model.max_block_size),
            ("State", state)
        ]


class RectangleModelFormatter(ModelFormatter):
    """
    A ModelFormatter subclass for formatting TwoDCoveringModel
    """
    MODEL_NAME = "2D Rectangle model"

    @classmethod
    def get_properties(cls, model):
        super_props = super().get_properties(model)
        new_props = [
            ("Width", model.width),
            ("Height", model.height)
        ]

        return super_props + new_props


class PyramidModelFormatter(ModelFormatter):
    """
    A ModelFormatter subclass for formatting PyramidCoveringModel
    """
    MODEL_NAME = "3D Pyramid model"

    @classmethod
    def get_properties(cls, model):
        super_props = super().get_properties(model)
        new_props = [
            ("Size", model.size),
        ]

        return super_props + new_props


class NoModelFormatter(Formatter):
    """
    A ModelFormatter subclass for formatting model=None
    """
    # pylint: disable=arguments-differ
    @classmethod
    def get_properties(cls, model):
        return [
            ("Model name", None)
        ]


class UnknownModelFormatter(Formatter):
    """
    A ModelFormatter subclass for formatting a model
    that is not an instance of any of the known types
    (should not happen)
    """
    # pylint: disable=arguments-differ
    @classmethod
    def get_properties(cls, model):
        return [
            ("Model name", "Unknown")
        ]


class ViewFormatter(Formatter):
    """
    A Formatter subclass for formatting views
    """
    @staticmethod
    def view_name(view):
        """
        Gets a view name from a view instance
        """
        if view is None:
            return None

        if isinstance(view, views.TwoDPrintView):
            return "2D Print view"
        if isinstance(view, views.TwoDVisualView):
            return "2D Visual view"
        if isinstance(view, views.PyramidPrintView):
            return "Pyramid Print view"
        if isinstance(view, views.PyramidVisualView):
            return "Pyramid Visual view"

        return "Unknown"

    # pylint: disable=arguments-differ
    @classmethod
    def get_properties(cls, view):
        v_name = ViewFormatter.view_name(view)
        return [
            ("View name", v_name)
        ]


def get_formatter(model):
    """
    Returns a formatter for a given model (according to its type)
    """
    if model is None:
        return NoModelFormatter

    if isinstance(model, models.TwoDCoveringModel):
        return RectangleModelFormatter
    if isinstance(model, models.PyramidCoveringModel):
        return PyramidModelFormatter

    return UnknownModelFormatter


class InfoBox(QTextEdit):
    """
    A specialized QTextEdit showing information about
    a given model and view (updated using the `update(model, view)`
    method
    """
    def __init__(self, parent):
        super().__init__(parent)

    def update(self, model, view):
        model_formatter = get_formatter(model)
        model_info = model_formatter.format(model)
        view_info = ViewFormatter.format(view)

        html = f"<html><head><meta name='qrichtext' content='1' /></head>" \
               f"<body><p>{model_info}</p><p>{view_info}</p></body></html>"

        self.setHtml(html)
