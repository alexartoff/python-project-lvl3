#!/usr/bin/env python


import sys
import logging
from itertools import zip_longest
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from page_loader.url_modifier import make_assets_path, make_full_link
from page_loader.url_modifier import isAllowed, isLocal, html_tag_path
import os


ATTRIBUTE_MAPPING = {"img": "src", "script": "src", "link": "href"}


def get_data(url_adress):
    session_ = requests.Session()
    try:
        resp = session_.get(url_adress)
        bs_data = BeautifulSoup(resp.content, 'html.parser')
        return bs_data, session_
    except HTTPError as http_err:
        logging.error(f'HTTP error: {http_err}')
        sys.exit(1)


# def check_url(url_adress):
#     try:
#         session_ = requests.Session()
#         resp = session_.get(url_adress)
#         if resp.status_code == 200:
#             logging.info(f'url "{url_adress}" response with status'
#                          f' code {resp.status_code}. continue...')
#             return True
#     except HTTPError as http_err:
#         logging.error(f'HTTP error: {http_err}')
#         sys.exit(1)
#     except requests.exceptions.ConnectionError:
#         raise requests.exceptions.ConnectionError('Connection Error')
#     except requests.exceptions.InvalidSchema:
#         raise requests.exceptions.InvalidSchema('Invalid Schema Error')


def prepare_data(data, url):
    download_dict = {}

    for tag in ["img", "script", "link"]:
        tag_full_link_list = make_full_link(tag, data.find_all(tag), url)
        if not tag_full_link_list:
            logging.debug(f"no tag <{tag}> for download")
            continue

        # add in dict key-value for downloading
        download_dict.update(_make_dict(tag_full_link_list, tag, url))

        # change html for current tag
        change_html(data.find_all(tag), tag, url)
    return download_dict


def change_html(tag_list, tag, url):
    assets_path = make_assets_path(url)

    for item in tag_list:
        link = item[ATTRIBUTE_MAPPING[tag]]
        if (tag == "img" and isAllowed(link, url)) or \
           ((tag == "script" or tag == "link") and isLocal(link, url)):
            item[ATTRIBUTE_MAPPING[tag]] = os.path.join(
                assets_path,
                html_tag_path(link, url)
            )


def _make_dict(tag_list, tag, url):
    func_dict = {
        "img": lambda item: isAllowed(item, url),
        # "link": lambda item: isLocal(item, url),
        # "script": lambda item: isLocal(item, url),
    }
    link_list = list(filter(
        func_dict.get(tag),
        tag_list
    ))
    return dict(
        zip_longest(
            link_list,
            [],
            fillvalue=make_assets_path(url)
        )
    )
