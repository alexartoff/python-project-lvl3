#!/usr/bin/env python


import logging
from page_loader.engine import download_data, change_html
from page_loader.pathwork import make_assets_dir, make_filename
from page_loader.data import get_data


def download(url_adress, save_dir):
    assets_dir = make_assets_dir(save_dir, url_adress)
    data = get_data(url_adress, assets_dir)

    for tag in ["img", "script", "link"]:
        logging.info(f'start download data with tag <{tag}>:')
        download_data(tag, data)
        change_html(tag, data)

    logging.info('writing finaly edited html page')
    filename = make_filename(assets_dir, url_adress)
    bs_data, _, _, _ = data
    with open(filename, "w") as wf:
        wf.write(bs_data.prettify())
