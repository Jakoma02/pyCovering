#!/usr/bin/env python3

import argparse
from covering.models import PyramidCoveringModel, TwoDCoveringModel
from covering.views import TwoDPrintView, PyramidPrintView, PyramidVisualView

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(
    metavar="model"
)

def check_args(args):
    if "model" not in args:
        parser.error("No model specified")
    if "size" in args and args.size <= 0:
        parser.error("Size must be positive")
    if "width" in args and args.width <= 0:
        parser.error("Width must be positive")
    if "height" in args and args.height <= 0:
        parser.error("Height must be positive")


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

pyramid_parser = subparsers.add_parser("pyramid", parents=[general_subparser])

pyramid_parser.add_argument(
        "--size",
        "-s",
        type=int,
        default=4
)

pyramid_parser.set_defaults(model="pyramid")

args = parser.parse_args()
check_args(args)

if args.model == "pyramid":
    model = PyramidCoveringModel(args.size, args.block)
    if args.visual:
        view = PyramidVisualView()
    else:
        view = PyramidPrintView()
elif args.model == "2d":
    model = TwoDCoveringModel(args.width, args.height, args.block)
    view = TwoDPrintView()

print(args)
model.try_cover()
view.show(model)
