#!/usr/bin/env python


import logging
import os
from page_loader.engine import download_data, change_html
from page_loader.pathwork import make_assets_path, make_filename
from page_loader.pathwork import make_dirs
from page_loader.data import get_data, check_url


def download(url_adress, base_dir_path):
    logging.info('page-loader started!')
    logging.info(f'checking url - {url_adress}')
    check_result, session_, resp = check_url(url_adress)
    if check_result:
        assets_dir_path = make_assets_path(url_adress)
        dirs_path = os.path.join(base_dir_path, assets_dir_path)
        make_dirs(dirs_path)
        data = get_data(url_adress,
                        base_dir_path,
                        assets_dir_path,
                        session_,
                        resp)

    for tag in ["img", "script", "link"]:
        logging.info(f'searching data with tag <{tag}>...')
        download_data(tag, data)
        change_html(tag, data)

    logging.info(f'writing finaly edited html page to "{base_dir_path}/"')
    filename = make_filename(base_dir_path, url_adress)
    bs_data, _, _, _, _ = data
    with open(filename, "w") as wf:
        wf.write(bs_data.prettify())

    if os.path.exists(filename):
        return filename
