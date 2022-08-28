#!/usr/bin/env python


import os
import logging
from urllib.parse import urlparse
import urllib3
from progress.bar import FillingSquaresBar
from page_loader.pathwork import make_filename


ATTRIBUTE_MAPPING = {"img": "src", "script": "src", "link": "href"}


def download_data(tag, data):
    bs_data, _, _, _, _ = data
    tag_list = bs_data.find_all(tag)

    if not tag_list:
        return logging.info(f"no tag <{tag}> for download")

    download_list = make_download_list(tag_list, tag, data)
    if not download_list:
        return logging.info("nothing to download")

    get_resourse(download_list, data)


def change_html(tag, data):
    bs_data, _, _, _, _ = data
    tag_list = bs_data.find_all(tag)
    make_change(tag_list, tag, data)


def make_download_list(tag_list, tag, data):
    _, _, host, _, _ = data

    if tag == "img":
        download_list = filter(
            isAllowed,
            [link.get(ATTRIBUTE_MAPPING[tag]) for link in tag_list]
        )
    if tag == "script" or tag == "link":
        download_list = filter(
            lambda item: isLocal(item, host),
            [link.get(ATTRIBUTE_MAPPING[tag]) for link in tag_list])
    return list(download_list)


def get_resourse(download_list, data):
    _, session_, _, base_dir, assets_dir = data

    bar = FillingSquaresBar(' Download: ', max=len(download_list))
    dir = os.path.join(base_dir, assets_dir)
    with bar:
        for link in download_list:
            if os.path.splitext(link):  # [1]:
                filename = make_filename(dir, link)
                logging.debug(f'start download {filename}')
                resp = session_.get(url=link)
                if resp.status_code == 200:
                    with open(filename, "wb") as wbf:
                        wbf.write(resp.content)
                else:
                    logging.error(f'download {filename}'
                                  f' FAIL! Error - {resp.status_code}')
            bar.next()
        logging.debug('download successfully')


def make_change(list_, tag, data):
    _, _, host, _, assets_dir = data

    for src in list_:
        tag_url = src.get(ATTRIBUTE_MAPPING[tag])
        if tag == "img" and isAllowed(tag_url):
            src[ATTRIBUTE_MAPPING[tag]] = make_filename(
                assets_dir,
                tag_url
            )
        if (tag == "script" or tag == "link") and isLocal(tag_url, host):
            src[ATTRIBUTE_MAPPING[tag]] = make_filename(
                assets_dir,
                tag_url
            )


def isAllowed(link):
    file_ext = os.path.splitext(os.path.split(link)[1])
    if file_ext[1] in [".jpg", ".png"]:
        return True


def isLocal(link, host):
    if not urlparse(link).hostname and urlparse(link).path:
        return True
    if host and urlparse(link).hostname == host:
        return True


def get_url_host(url_adress):
    try:
        url_host = urlparse(url_adress).hostname
        return url_host
    except urllib3.connectionpool.ConnectionError:
        raise urllib3.connectionpool.ConnectionError('Connection Error')
