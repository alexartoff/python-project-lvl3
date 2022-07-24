#!/usr/bin/env python


import logging
from pageloader.engine import make_dirs, loader_changer, make_filename
from pageloader.engine import get_url_host, get_bs_data


def download(save_dir, url_adress):
    assets_dir = make_dirs(save_dir, url_adress)
    bs_data, session_ = get_bs_data(url_adress)
    download_data = (bs_data,
                     assets_dir,
                     session_,
                     get_url_host(url_adress))

    for tag in ["img", "script", "link"]:
        logging.info(f'start download data with tag <{tag}>:')
        loader_changer(tag, download_data)

    logging.info('writing finaly edited html page')
    filename = make_filename(assets_dir, url_adress)
    with open(filename, "w") as wf:
        wf.write(bs_data.prettify())
