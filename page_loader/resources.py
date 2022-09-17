#!/usr/bin/env python


import logging
from bs4 import BeautifulSoup
import requests
import os
from page_loader.url_modifier import make_assets_path, make_full_link
from page_loader.url_modifier import isAllowed, isLocal, html_tag_path


ATTRIBUTE_MAPPING = {
    "img": "src",
    "script": "src",
    "link": "href"
}


def get_data(url_adress):
    session_ = requests.Session()
    resp = session_.get(url_adress)
    if resp.status_code == 200:
        bs_data = BeautifulSoup(resp.content, 'html.parser')
        return bs_data, session_
    raise Exception(
        logging.error(f'HTTP error: {url_adress} - {resp.status_code}')
    )


def prepare_data(data, url):
    tags = []
    # filter tags by ATTRIBUTE_MAPPING, locality, allowed file extension
    for tag in ATTRIBUTE_MAPPING.keys():
        _ = []
        for tag_item in data.find_all(tag):
            tag_value = ATTRIBUTE_MAPPING[tag]
            if tag_value in tag_item.attrs.keys() and\
                    isLocal(tag_item[tag_value], url):
                _.append(tag_item)
        tags.extend(_)
    f1 = []
    for t in tags:
        if t.name != 'img' or\
                (t.name == 'img' and isAllowed(t.attrs['src'], url)):
            f1.append(t)
    # print(f1)
    return _get_pretty_and_assets(data, tags, url)


def _get_pretty_and_assets(data, tags, url):
    assets_path = make_assets_path(url)
    # make links and change html in source html data
    assets = []
    for tag in tags:
        link, full_assets_path = '', ''
        if 'src' in tag.attrs.keys():
            link = make_full_link(tag['src'], url)
            full_assets_path = os.path.join(
                assets_path,
                html_tag_path(link, url)
            )
            tag['src'] = os.path.join(full_assets_path)
        if 'href' in tag.attrs.keys():
            link = make_full_link(tag['href'], url)
            full_assets_path = os.path.join(
                assets_path,
                html_tag_path(link, url)
            )
            tag['href'] = os.path.join(full_assets_path)

        to_list = (link, full_assets_path)
        assets.append(to_list)
    return data.prettify(), assets


# def prepare_data(data, url):
#     download_dict = {}
#
#     for tag in ["img", "script", "link"]:
#         tag_full_link_list = make_full_link(tag, data.find_all(tag), url)
#         if not tag_full_link_list:
#             logging.debug(f"no tag <{tag}> for download")
#             continue
#
#         # add in dict key-value for downloading
#         download_dict.update(_make_dict(tag_full_link_list, tag, url))
#
#         # change html for current tag
#         change_html(data.find_all(tag), tag, url)
#     return download_dict


# def change_html(tag_list, tag, url):
#     assets_path = make_assets_path(url)
#
#     for item in tag_list:
#         link = item[ATTRIBUTE_MAPPING[tag]]
#         if (tag == "img" and isAllowed(link, url)) or \
#            ((tag == "script" or tag == "link") and isLocal(link, url)):
#             item[ATTRIBUTE_MAPPING[tag]] = os.path.join(
#                 assets_path,
#                 html_tag_path(link, url)
#             )


# def _make_dict(tag_list, tag, url):
#     func_dict = {
#         "img": lambda item: isAllowed(item, url),
#         # "link": lambda item: isLocal(item, url),
#         # "script": lambda item: isLocal(item, url),
#     }
#     link_list = list(filter(
#         func_dict.get(tag),
#         tag_list
#     ))
#     return dict(
#         zip_longest(
#             link_list,
#             [],
#             fillvalue=make_assets_path(url)
#         )
#     )
