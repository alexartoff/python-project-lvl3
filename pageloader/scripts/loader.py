#!/usr/bin/env python


import logging
import sys
from pageloader.cli import parse_args
from pageloader.page_loader import download


def main():
    logging.basicConfig(format='[ %(asctime)s ] - %(levelname)s: %(message)s',
                        filename='loader_main.log',
                        level=logging.DEBUG)
    logging.info(f'{"=" * 10} SRART {"=" * 10}')
    args = parse_args()
    logging.info('start download module')
    download(args.output, args.url_adress)
    logging.info(f'{"=" * 10} DONE! {"=" * 10}')


if __name__ == "__main__":
    try:
        main()
        # logging.StreamHandler(sys.stdout)
        # sys.exit(0)
        logging.info(sys.exit(0))
    except Exception as err:
        logging.StreamHandler(sys.stderr)
        logging.exception(f'something broke, sorry {err} {sys.exit(err)}')
        # sys.exit(1)
