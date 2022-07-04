#!/usr/bin/env python


import os
import requests
from urllib.parse import urlparse


def download(save_path, url_adress):
    # print(f"WORK {save_path} {url_adress}\n{os.getcwd()}")
    r = requests.get(url_adress)
    if r.status_code == 200 and is_dir_exist(save_path):
        return make_path(save_path, url_adress)
    # with open(path, "w") as wf:
    #     wf.write(r.text)
    # print(r.headers)
    return None


def parse_url_adress(url_adress):
    host = (urlparse(url_adress).hostname).replace(".", "-")
    path = (urlparse(url_adress).path).replace("/", "-")
    return (host, path)


def make_path(save_path, url_adress):
    h, p = parse_url_adress(url_adress)
    return f"{save_path}/{h}{p}.html"


def is_dir_exist(save_path):
    return os.path.exists(save_path)
