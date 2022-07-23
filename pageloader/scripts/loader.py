#!/usr/bin/env python


import logging
from pageloader.cli import parse_args
from pageloader.page_loader import download


def main():
    logging.basicConfig(format='[ %(asctime)s ] - %(levelname)s: %(message)s',
                        filename='loader_main.log',
                        level=logging.DEBUG)
    logging.info(f'{"=" * 10} SRART {"=" * 10}')
    args = parse_args()
    logging.info('start download module')
    filepath = download(args.output, args.url_adress)
    logging.info(f'{"=" * 10} DONE! {"=" * 10}')
    print(filepath)


if __name__ == "__main__":
    main()
