"""Argparse CLI Functions"""

import sys
import os
import argparse
from aws_control_tower_manifest_builder import aws_control_tower_manifest_builder
from aws_control_tower_manifest_builder import logger

log = logger.get_logger(__name__)

# TODO: Add verification for inputs
# TODO: Fix Tox. Add
# TODO: adding final schema validation
# TODO: Read me and Docs. connect github and read the docs account.


def dir_path(string):
    """
    Determine if string is a path

    Parameter:
    string(string): string representation of a path

    Return:
    string(string): string representation of a path
    """
    if os.path.isdir(string):
        return string
    raise NotADirectoryError(f"Directory '{string}' does not exist")


def str2bool(input_bool):
    """
    Determine if input is True or False

    Parameter:
    string(string): string representation of a bool

    Return:
    string(string): string representation of a bool
    """
    if isinstance(input_bool, bool):
        return input_bool
    if input_bool.lower() == "true":
        return True
    if input_bool.lower() == "false":
        return False
    raise argparse.ArgumentTypeError(
        f"Boolean value expected. Received -> {input_bool}"
    )


def main():
    """Console script for aws_control_tower_manifest_builder."""
    parser = argparse.ArgumentParser(
        description="Produces the manifest.yaml file that works as input \
            for AWS Control Tower"
    )

    parser.add_argument(
        "--abort-if-error",
        "-a",
        default=False,
        type=str2bool,
        help="If set, does not produce the manifest file if any of the input \
            files could not be processed",
    )
    parser.add_argument(
        "--default-region",
        "-r",
        type=str,
        help="Default region for templates with no regio. Default us-east-1",
        default="us-east-1",
    )

    parser.add_argument(
        "--input-cf",
        "-c",
        metavar="/path/",
        type=dir_path,
        required=True,
        help="the path to the directory containing the cloud formation input \
            files",
    )

    parser.add_argument(
        "--input-scp",
        "-s",
        metavar="/path/",
        type=dir_path,
        required=True,
        help="the path to the directory containing the service control policy \
            input files",
    )

    parser.add_argument(
        "--output",
        "-o",
        metavar="/path/",
        type=dir_path,
        help="the path to store the output manifest.yaml file",
    )

    try:
        args = parser.parse_args()
    except NotADirectoryError as error:
        log.error(error)
        sys.exit()
    except argparse.ArgumentTypeError as error:
        log.error(error)
        sys.exit()

    aws_control_tower_manifest_builder.main(args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
