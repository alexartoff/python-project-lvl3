#!/usr/bin/env python


import logging
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pageloader.engine import make_dirs, loader_changer, make_filename


def download(save_dir, url_adress):
    url_host, assets_dir = make_dirs(save_dir, url_adress)
    try:
        session_ = requests.Session()
        resp = session_.get(url_adress)
        # то как видит request страницу можно проверить,
        # если скачать страницу с помощью программ curl или wget
        if resp.status_code == 200:
            bs_data = BeautifulSoup(resp.content, 'html.parser')
            download_data = bs_data, assets_dir, session_, url_host

            for tag in ["img", "script", "link"]:
                logging.info(f'start download data from <{tag}>:')
                loader_changer(tag, download_data)

            logging.info('download finaly edited html page')
            filename = make_filename(assets_dir, url_adress)
            with open(filename, "w") as wf:
                wf.write(bs_data.prettify())
        else:
            logging.error(f'FAIL! Error - {resp.status_code}')

    except HTTPError as http_err:
        logging.error(f'HTTP error: {http_err}')
    except Exception as err:
        logging.error(f'Other error: {err}')
