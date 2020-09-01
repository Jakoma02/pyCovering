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

COVERING_ATTEMPTS = 100


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


def get_parser():
    """
    Return a configured parser
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    general_subparser = argparse.ArgumentParser(add_help=False)
    general_subparser.add_argument(
        "--block",
        "-b",
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


def main():
    """
    The program entrypoint
    """
    parser = get_parser()

    args = parser.parse_args()
    check_args(args, parser)

    if args.model == "pyramid":
        model = PyramidCoveringModel(args.size, args.block)
        if args.visual:
            view = PyramidVisualView()
        else:
            view = PyramidPrintView()
    elif args.model == "2d":
        model = TwoDCoveringModel(args.width, args.height, args.block)
        view = TwoDPrintView()

    if args.verbose:
        print(args)

    for i in range(COVERING_ATTEMPTS):
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
            view.show(model)
            break
    else:
        if args.verbose:
            print("Covering failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
