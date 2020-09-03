#!/usr/bin/env python3

"""
Program entrypoint, facilitates argument parsing.
"""

import argparse
import sys

from covering.models import PyramidCoveringModel, \
                            TwoDCoveringModel, \
                            ImpossibleToFinishException, \
                            CoveringTimeoutException

from covering.views import TwoDPrintView, PyramidPrintView, PyramidVisualView
from covering.constraints import string_constraint, path_constraint

COVERING_ATTEMPTS = 100


class TooManyAttemptsException(Exception):
    """
    This exception is raised if the covering attempts limit
    was reached
    """


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
        action="store_true"
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

    # three_d_parser = subparsers.add_parser("3d")
    # three_d_parser.set_defaults(model="3d")

    pyramid_parser = subparsers.add_parser("pyramid",
                                           parents=[general_subparser])

    pyramid_parser.add_argument(
        "--size",
        "-s",
        type=int,
        default=4
    )

    pyramid_parser.set_defaults(model="pyramid")

    return parser


def get_model_view(args):
    """
    Return a (model, view) tuple based on args
    """
    if args.model == "pyramid":
        model = PyramidCoveringModel(args.size, args.min_block_size,
                                     args.max_block_size)
        if args.visual:
            view = PyramidVisualView()
        else:
            view = PyramidPrintView()
    elif args.model == "2d":
        model = TwoDCoveringModel(args.width, args.height, args.min_block_size,
                                  args.max_block_size)
        view = TwoDPrintView()

    return (model, view)


def do_covering(model, attempts, args):
    """
    Tries to cover the model `attempts` times
    """
    for i in range(attempts):
        if args.verbose:
            print(f"Attempting to cover ({i + 1}th attempt)... ",
                  end="", flush=True)

        try:
            model.reset()
            model.try_cover()
        except (ImpossibleToFinishException, CoveringTimeoutException):
            if args.verbose:
                print("FAILED")
        else:
            if args.verbose:
                print("SUCCESS")
            return  # Success

    raise TooManyAttemptsException("Too many failed attempts")


def set_constraints(model, args):
    """
    Set model constraints according to args values
    """
    if args.string:
        model.add_constraint(string_constraint)

    if args.path:
        model.add_constraint(path_constraint)


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
