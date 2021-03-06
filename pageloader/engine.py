#!/usr/bin/env python


import os
import logging
from urllib.parse import urlparse
import urllib3
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from progress.bar import FillingSquaresBar


TAGS = {"img": "src", "script": "src", "link": "href"}


def make_dirs(save_dir, url_adress):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        logging.info('download directory created')
    assets_dir = make_assets_dirpath(save_dir, url_adress)
    if not os.path.exists(assets_dir):
        os.mkdir(assets_dir)
        logging.info('assets directory created')
    return assets_dir


def loader_changer(tag, download_data):
    bs_data, _, _, _ = download_data
    tag_list = bs_data.find_all(tag)
    if not tag_list:
        return logging.info(f"no tag <{tag}> for download")

    download_list = make_download_list(tag_list, tag, download_data)
    download_resourse(download_list, download_data)
    change_html(tag_list, tag, download_data)


def make_download_list(list_, tag, download_data):
    _, _, _, host = download_data

    if tag == "img":
        download_list = filter(isAllowed,
                               [link.get(TAGS[tag]) for link in list_])
    if tag == "script" or tag == "link":
        download_list = filter(lambda item: isLocal(item, host),
                               [link.get(TAGS[tag]) for link in list_])
    return download_list


def download_resourse(download_list, download_data):
    _, assets_dir, session_, _ = download_data
    dl = list(download_list)
    bar = FillingSquaresBar(' Download: ', max=len(dl))
    with bar:
        for link in dl:
            if os.path.splitext(link)[1]:
                filename = f"{assets_dir}/{os.path.split(link)[1]}"
                logging.debug(f'start download {os.path.split(filename)[1]}'
                              f' in {os.path.split(filename)[0][1:]}')
                resp = session_.get(url=link)
                if resp.status_code == 200:
                    with open(filename, "wb") as wbf:
                        wbf.write(resp.content)
                else:
                    logging.error(f'download {os.path.split(filename)[1]}'
                                  f' FAIL! Error - {resp.status_code}')
            bar.next()
        logging.debug('download successfully')


def change_html(list_, tag, download_data):
    _, assets_dir, _, host = download_data

    for src in list_:
        tag_data = src.get(TAGS[tag])
        if tag == "img" and isAllowed(tag_data):
            src[TAGS[tag]] = os.path.join(assets_dir[1:],
                                          os.path.split(tag_data)[1])
        if (tag == "script" or tag == "link") and isLocal(tag_data, host):
            h, p = parse_url_adress(tag_data)
            ext = os.path.splitext(p)[1]
            filename = f"{h}{p}.html" if ext == "" \
                else os.path.split(tag_data)[1]
            src[TAGS[tag]] = os.path.join(assets_dir[1:],
                                          filename)


def isAllowed(link):
    file_ext = os.path.splitext(os.path.split(link)[1])
    if file_ext[1] in [".jpg", ".png"]:
        return True


def isLocal(link, host):
    if urlparse(link).hostname == host:
        return True


def parse_url_adress(url_adress):
    host = (urlparse(url_adress).hostname).replace(".", "-")
    path = (urlparse(url_adress).path).replace("/", "-")
    return (host, path if path[-1] != "-" else path[:-1])


def make_filename(save_dir, url_adress):
    h, p = parse_url_adress(url_adress)
    return os.path.join(save_dir, f"{h}{p}.html")


def make_assets_dirpath(save_dir, url_adress):
    h, p = parse_url_adress(url_adress)
    return os.path.join(save_dir, f"{h}{p}_files")


def get_url_host(url_adress):
    try:
        url_host = urlparse(url_adress).hostname
        return url_host
    except urllib3.connectionpool.ConnectionError:
        raise urllib3.connectionpool.ConnectionError('Connection Error')


def get_bs_data(url_adress):
    try:
        session_ = requests.Session()
        resp = session_.get(url_adress)
        # ???? ?????? ?????????? request ???????????????? ?????????? ??????????????????,
        # ???????? ?????????????? ???????????????? ?? ?????????????? ???????????????? curl ?????? wget
        if resp.status_code == 200:
            bs_data = BeautifulSoup(resp.content, 'html.parser')
            return bs_data, session_
        else:
            logging.error(f'FAIL! Error - {resp.status_code}')
    except HTTPError as http_err:
        logging.error(f'HTTP error: {http_err}')
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError('Connection Error')
    except requests.exceptions.InvalidSchema:
        raise requests.exceptions.InvalidSchema('Invalid Schema Error')
