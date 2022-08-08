#!/usr/bin/env python


import logging
import sys
from page_loader.log import log_on
from page_loader.cli import parse_args
from page_loader.page_loader import download


def main():
    log_on()

    try:
        args = parse_args()
        files_path = download(args.url_adress, args.output)
        logging.info(f'html file downloaded and modified "{files_path}"')
        logging.info('done. exit')
        sys.exit(0)
    except Exception as err:
        logging.error(f'oops! {err}. Stop running...')
        sys.exit(1)
    except BaseException:
        logging.error('CLI error! Stop running...')
        sys.exit(2)


if __name__ == "__main__":
    main()
