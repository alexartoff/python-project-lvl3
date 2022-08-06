#!/usr/bin/env python


import logging
import sys
from page_loader.log import log_on
from page_loader.cli import parse_args
from page_loader.page_loader import download


def main():
    log_on()

    try:
        logging.info('page-loader started!')
        args = parse_args()
        logging.info(f'getting data from url {args.url_adress}')
        download(args.url_adress, args.output)
        logging.info('done. all ok. exit')
        sys.exit(0)
    except Exception as err:
        logging.error(f'oops! {err}. Stop running...')
        sys.exit(1)


if __name__ == "__main__":
    main()
