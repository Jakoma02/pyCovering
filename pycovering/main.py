#!/usr/bin/env python3

"""
Program entrypoint, facilitates argument parsing.
"""

import argparse
import sys

from PySide2.QtWidgets import QApplication

from pycovering.models import PyramidCoveringModel, \
                              TwoDCoveringModel, \
                              ImpossibleToFinishException, \
                              CoveringTimeoutException

from pycovering.views import TwoDPrintView, PyramidPrintView, \
                             PyramidVisualView, TwoDVisualView

from pycovering.constraints import PathConstraintWatcher,  \
                                   PlanarConstraintWatcher

COVERING_ATTEMPTS = 100


class TooManyAttemptsException(Exception):
    """
    This exception is raised if the covering attempts limit
    was reached
    """


def qapp_decorator(cls):
    """
    This function takes a view using QWidgets
    and creates a QApplication for it
    """
    class Wrapped(cls):
        """
        The new, modified class
        """
        def __init__(self):
            self.app = QApplication()
            cls.__init__(self)

        def show(self, model):
            """
            Shows the view, starts the QApplication
            """
            cls.show(self, model)
            self.app.exec_()

    return Wrapped


def check_args(args, parser):
    """
    Verify argument validity
    """
    if "model" not in args:
        parser.error("No model specified")
    if "size" in args and args.size <= 0:
        parser.error("Size must be positive")
    if "width" in args and args.width <= 0:
        parser.error("Width must be positive")
    if "height" in args and args.height <= 0:
        parser.error("Height must be positive")
    if "min_block_size" in args:
        mib = args.min_block_size
        if mib <= 0:
            parser.error("Block sizes must be positive")
        if "max_block_size" in args:
            mab = args.max_block_size
            if mab < mib:
                parser.error("Upper block size bound must not be smaller " +
                             "than lower block size bound")


def get_parser():
    """
    Return a configured parser
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    general_subparser = argparse.ArgumentParser(add_help=False)

    general_subparser.add_argument(
        "--min-block-size",
        "-mib",
        type=int,
        default=4
    )

    general_subparser.add_argument(
        "--max-block-size",
        "-mab",
        type=int,
        default=4
    )

    general_subparser.add_argument(
        "--visual",
        action="store_true"
    )

    general_subparser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0
    )

    general_subparser.add_argument(
        "--string",
        action="store_true"
    )

    general_subparser.add_argument(
        "--path",
        action="store_true"
    )

    two_d_parser = subparsers.add_parser("2d", parents=[general_subparser])
    two_d_parser.set_defaults(model="2d")

    two_d_parser.add_argument(
        "--width",
        type=int,
        default=10
    )

    two_d_parser.add_argument(
        "--height",
        type=int,
        default=10
    )

    pyramid_parser = subparsers.add_parser("pyramid",
                                           parents=[general_subparser])

    pyramid_parser.add_argument(
        "--size",
        "-s",
        type=int,
        default=4
    )

    pyramid_parser.add_argument(
        "--planar",
        action="store_true"
    )

    pyramid_parser.set_defaults(model="pyramid")

    return parser


def get_model_view(args):
    """
    Return a (model, view) tuple based on args
    """
    if args.model == "pyramid":
        model = PyramidCoveringModel(args.size, args.min_block_size,
                                     args.max_block_size,
                                     args.verbose)
        if args.visual:
            view = PyramidVisualView()
        else:
            view = PyramidPrintView()
    elif args.model == "2d":
        model = TwoDCoveringModel(args.width, args.height, args.min_block_size,
                                  args.max_block_size, args.verbose)

        if args.visual:
            view = qapp_decorator(TwoDVisualView)()
        else:
            view = TwoDPrintView()

    return (model, view)


def do_covering(model, attempts, args):
    """
    Tries to cover the model `attempts` times
    """
    for i in range(attempts):
        if args.verbose >= 1:
            print(f"Attempting to cover ({i + 1}th attempt)... ",
                  flush=True)

        try:
            model.reset()
            model.try_cover()
        except (ImpossibleToFinishException, CoveringTimeoutException):
            if args.verbose >= 1:
                print("\tFAILED")
        else:
            if args.verbose >= 1:
                print("\tSUCCESS")
            return  # Success

    raise TooManyAttemptsException("Too many failed attempts")


def set_constraints(model, args):
    """
    Set model constraints according to args values
    """
    if args.path:
        model.add_constraint(PathConstraintWatcher)

    if "planar" in args and args.planar:
        model.add_constraint(PlanarConstraintWatcher)


def main():
    """
    The program entrypoint
    """
    parser = get_parser()

    args = parser.parse_args()
    check_args(args, parser)

    if args.verbose:
        print(f"Used arguments: {args}")

    model, view = get_model_view(args)

    set_constraints(model, args)

    try:
        do_covering(model, COVERING_ATTEMPTS, args)
        view.show(model)
    except TooManyAttemptsException:
        print("Attempt limit reached")
        sys.exit(1)


if __name__ == "__main__":
    main()
