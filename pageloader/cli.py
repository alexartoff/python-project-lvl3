#!/usr/bin/env python


import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        prog='page-loader',
        description='Page download utility from websites')

    parser.add_argument(
        '--output',
        type=str,
        default=os.getcwd(),
        metavar='save_path',
        help=(f'set OUTPUT path for save page '
              f'or leave DEFAULT path: {os.getcwd()}'))

    parser.add_argument(
        'url_adress',
        type=str,
        metavar='url_adress')

    return parser.parse_args()
