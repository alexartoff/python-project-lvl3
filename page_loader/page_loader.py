#!/usr/bin/env python


import logging
import os
from page_loader.engine import download_data, change_html
from page_loader.pathwork import make_assets_path, make_filename, make_dirs
from page_loader.data import get_data, check_url


def download(url_adress, base_dir_path):
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
        logging.info(f'start download data with tag <{tag}>:')
        download_data(tag, data)
        change_html(tag, data)

    logging.info(f'writing finaly edited html page to "{base_dir_path}/"')
    filename = make_filename(base_dir_path, url_adress)
    bs_data, _, _, _, _ = data
    with open(filename, "w") as wf:
        wf.write(bs_data.prettify())

    count_dl_files = len(os.listdir(os.path.join(base_dir_path,
                                                 assets_dir_path)))
    return count_dl_files
