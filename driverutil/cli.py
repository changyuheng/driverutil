import argparse
import os
import pathlib

from .inf import get_bundled_files


def do_source_dist_files(args: argparse.Namespace) -> int:
    p: pathlib.Path
    for p in get_bundled_files(pathlib.Path(args.inf_path)):
        print(p)
    return os.EX_OK


def get_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='driverutil',
        description='A Windows driver utility',
        allow_abbrev=True)

    parser.add_argument('-v', '--verbose', action='count', default=0, help='show more information')

    sub_parsers: argparse._SubParsersAction = parser.add_subparsers(metavar='COMMAND')
    source_disk_files_parser = sub_parsers.add_parser(name='source-disk-files', help='show SourceDiskFiles')
    source_disk_files_parser.add_argument('inf_path', help='path to the INF file', metavar='INF')
    source_disk_files_parser.set_defaults(func=do_source_dist_files)

    return parser.parse_args()


def main() -> int:
    args: argparse.Namespace = get_args()
    return args.func(args)
