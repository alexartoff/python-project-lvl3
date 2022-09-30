import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        prog='page-loader',
        description='Page download utility from websites')

    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default=f'{os.path.relpath(os.getcwd())}/',
        metavar='save_path',
        help=(f'set OUTPUT path for save page '
              f'or leave DEFAULT (current) path: '
              f'{os.path.relpath(os.getcwd())[1:]}/'))

    parser.add_argument(
        'url_adress',
        type=str,
        metavar='url_adress')

    return parser.parse_args()
