#!/usr/bin/env python


import sys
import logging
from itertools import zip_longest
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from page_loader.url_modifier import make_filename, make_assets_path
from page_loader.url_modifier import isAllowed, isLocal


ATTRIBUTE_MAPPING = {"img": "src", "script": "src", "link": "href"}


def get_data(resp):
    bs_data = BeautifulSoup(resp.content, 'html.parser')
    return bs_data


def check_url(url_adress):
    try:
        session_ = requests.Session()
        resp = session_.get(url_adress)
        # то как видит request страницу можно проверить,
        # если скачать страницу с помощью программ curl или wget
        if resp.status_code == 200:
            logging.info(f'url "{url_adress}" response with status'
                         f' code {resp.status_code}. continue...')
            return True, session_, resp
        else:
            logging.error(f'FAIL! Error - {resp.status_code}')
            return False, session_, resp
    except HTTPError as http_err:
        logging.error(f'HTTP error: {http_err}')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError('Connection Error')
    except requests.exceptions.InvalidSchema:
        raise requests.exceptions.InvalidSchema('Invalid Schema Error')


def prepare_data(data, url):
    download_dict = {}

    for tag in ["img", "script", "link"]:
        tag_list = data.find_all(tag)
        # print(f">>>prepare_data {tag}\n{tag_list}")
        if not tag_list:
            logging.debug(f"no tag <{tag}> for download")
            continue

        # add in dict key-value for downloading
        download_dict.update(make_dict(tag_list, tag, url))

        # change html for current tag
        change_html(tag_list, tag, url)
    return download_dict


def change_html(tag_list, tag, url):
    assets_path = make_assets_path(url)

    for src in tag_list:
        tag_url = src.get(ATTRIBUTE_MAPPING[tag])

        if (tag == "img" and isAllowed(tag_url, url)) or \
           ((tag == "script" or tag == "link") and isLocal(tag_url, url)):
            src[ATTRIBUTE_MAPPING[tag]] = make_filename(
                assets_path,
                tag_url
            )


def make_dict(tag_list, tag, url):
    func_dict = {
        "img": lambda item: isAllowed(item, url),
        "link": lambda item: isLocal(item, url),
        "script": lambda item: isLocal(item, url),
    }
    link_list = list(filter(
        func_dict.get(tag),
        [link.get(ATTRIBUTE_MAPPING[tag]) for link in tag_list]
    ))
    # print(f">>>make_dict {link_list}")
    return dict(
        zip_longest(
            link_list,
            [],
            fillvalue=make_assets_path(url)
        )
    )
