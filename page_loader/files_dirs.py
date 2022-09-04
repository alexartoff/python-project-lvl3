#!/usr/bin/env python


import os
import logging
from progress.bar import FillingSquaresBar
from page_loader.url_modifier import make_path


def make_assets_dir(base, assets):
    if not os.path.exists(base):
        raise Exception("download directory does't exist")
    os.makedirs(os.path.join(base, assets))
    logging.info(f'directory "{assets}" created')


def download_resources(dict_, base_dir, session_):
    bar = FillingSquaresBar(' Download: ', max=len(dict_.keys()))
    bar.suffix = '%(index)d | (total %(max)d)'
    bar.width = 3 * len(dict_.keys())
    logging.info('start download resources')
    with bar:
        for link, path in dict_.items():
            file_path = make_path(os.path.join(base_dir, path), link)
            resp = session_.get(url=link)
            if resp.status_code == 200:
                with open(file_path, "wb") as wbf:
                    wbf.write(resp.content)
                    bar.next()
            else:
                logging.error(f'download {file_path}'
                              f' FAIL! Error - {resp.status_code}')
    logging.info('download successfully')
