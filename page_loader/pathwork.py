#!/usr/bin/env python


import os
import logging
from urllib.parse import urlparse


def make_dirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        logging.info(f'directories "{dir}" created')


def make_assets_path(url):
    h, p = parse_url_adress(url)
    assets_dir = f"{h}{p}_files"
    return assets_dir


def parse_url_adress(url_adress):
    host = (urlparse(url_adress).hostname).replace(".", "-")
    path = (urlparse(url_adress).path).replace("/", "-")
    if path == "":
        return (host, "")
    return (host, path if path[-1] != "-" else path[:-1])


def make_filename(dir, url_adress):
    h, p = parse_url_adress(url_adress)
    if os.path.splitext(p)[1]:
        return os.path.join(dir, f"{h}{p}")
    return os.path.join(dir, f"{h}{p}.html")
