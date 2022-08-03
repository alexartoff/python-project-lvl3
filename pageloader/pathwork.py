#!/usr/bin/env python


import os
import logging
from urllib.parse import urlparse


def make_save_dir(dir):
    """
    from cli argument '--output'
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
        logging.info('download directory created')
    return dir


def make_assets_dir(dir, url):
    h, p = parse_url_adress(url)
    assets_dir = os.path.join(make_save_dir(dir),
                              f"{h}{p}_files")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        logging.info('assets directory created')
    return assets_dir


def parse_url_adress(url_adress):
    host = (urlparse(url_adress).hostname).replace(".", "-")
    path = (urlparse(url_adress).path).replace("/", "-")
    if path == "":
        return (host, "")
    return (host, path if path[-1] != "-" else path[:-1])


def make_filename(save_dir, url_adress):
    h, p = parse_url_adress(url_adress)
    if os.path.splitext(p)[1]:
        return os.path.join(save_dir, f"{h}{p}")
    return os.path.join(save_dir, f"{h}{p}.html")
