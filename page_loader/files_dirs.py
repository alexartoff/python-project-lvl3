#!/usr/bin/env python


import os
import logging
from progress.bar import FillingSquaresBar


def make_assets_dir(base, assets):
    if not os.path.exists(base):
        raise Exception("download directory does't exist")
    os.makedirs(os.path.join(base, assets))
    logging.info(f'directory "{assets}" created')


def download_resources(base, assets_list, session_):
    bar = FillingSquaresBar(' Download: ', max=len(assets_list))
    bar.suffix = '%(index)d | (total %(max)d)'
    bar.width = 3 * len(assets_list)
    logging.info('start download resources')

    with bar:
        for item in assets_list:
            item_link, item_path = item
            resp = session_.get(url=item_link)
            if resp.status_code == 200:
                with open(os.path.join(base, item_path), "wb") as wbf:
                    wbf.write(resp.content)
                    bar.next()
            else:
                logging.error(f'download {item_path}'
                              f' FAIL! Error - {resp.status_code}')
    logging.info('download successfully')
