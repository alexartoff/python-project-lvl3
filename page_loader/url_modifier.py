#!/usr/bin/env python


import os
from urllib.parse import urlparse
import urllib3


def parse_url_adress(url):
    host = (urlparse(url).hostname).replace(".", "-")
    path = (urlparse(url).path).replace("/", "-")
    if path == "":
        return (host, "")
    return (host, path if path[-1] != "-" else path[:-1])


def make_assets_path(url):
    h, p = parse_url_adress(url)
    assets_dir = f"{h}{p}_files"
    return assets_dir


def make_filename(dir, url_adress):
    h, p = parse_url_adress(url_adress)
    if os.path.splitext(p)[1]:
        return os.path.join(dir, f"{h}{p}")
    return os.path.join(dir, f"{h}{p}.html")


def isAllowed(link, url):
    file_ext = os.path.splitext(os.path.split(link)[1])
    if file_ext[1] in [".jpg", ".png"] and isLocal(link, url):
        return True


def isLocal(link, url):
    host = get_url_host(url)
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
