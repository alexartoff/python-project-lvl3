#!/usr/bin/env python


import logging
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_loader.engine import get_url_host, TAGS


def get_data(url_adress, assets_dir, session_, resp):
    # bs_data, session_ = get_bs_data(url_adress)
    bs_data = BeautifulSoup(resp.content, 'html.parser')
    host = get_url_host(url_adress)
    make_full_link(bs_data, url_adress)
    return (bs_data, session_, host, assets_dir)


# def get_bs_data(url_adress):
#     check_result, session_, resp = check_url(url_adress)
#     if check_result:
#         bs_data = BeautifulSoup(resp.content, 'html.parser')
#         return bs_data, session_


def check_url(url_adress):
    try:
        session_ = requests.Session()
        resp = session_.get(url_adress)
        # то как видит request страницу можно проверить,
        # если скачать страницу с помощью программ curl или wget
        if resp.status_code == 200:
            return True, session_, resp
        else:
            logging.error(f'FAIL! Error - {resp.status_code}')
            return False, session_, resp
    except HTTPError as http_err:
        logging.error(f'HTTP error: {http_err}')
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError('Connection Error')
    except requests.exceptions.InvalidSchema:
        raise requests.exceptions.InvalidSchema('Invalid Schema Error')


def make_full_link(bs_data, url):
    mod_url = f"{urlparse(url).scheme}://{urlparse(url).hostname}"
    list_ = []
    for tag in TAGS.keys():
        list_.extend(bs_data.find_all(tag))

    for tag in TAGS.keys():
        for item in list_:
            url_tag = item.get(TAGS[tag])
            if url_tag and not urlparse(url_tag).hostname:
                item[TAGS[tag]] = f"{mod_url}{url_tag}"
