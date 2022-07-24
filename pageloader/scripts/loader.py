#!/usr/bin/env python


import logging
import sys
from pageloader.log import log_on
from pageloader.cli import parse_args
from pageloader.page_loader import download


def main():
    log_on()

    try:
        logging.info('get started!')
        args = parse_args()
        logging.info(f'run download module for url {args.url_adress}')
        download(args.output, args.url_adress)
        logging.info('done. all ok. exit')
        sys.exit(0)
    except Exception as err:
        logging.error(f'oops! {err}. Stop running...')
        sys.exit(1)


if __name__ == "__main__":
    main()
