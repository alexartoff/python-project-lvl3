#!/usr/bin/env python


import os
import logging
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def download(save_dir, url_adress):
    url_host, assets_dir = make_dirs(save_dir, url_adress)
    try:
        session_ = requests.Session()
        resp = session_.get(url_adress)
        # то как видит request страницу можно проверить,
        # если скачать страницу с помощью программ curl или wget
        if resp.status_code == 200:
            bs_data = BeautifulSoup(resp.content, 'html.parser')
            download_data = bs_data, assets_dir, session_, url_host

            logging.info('start download images:')
            download_images(download_data)

            logging.info('start download scrips:')
            download_scripts(download_data)

            logging.info('start download links:')
            download_links(download_data)

            logging.info('download finaly edited html page')
            filename = make_filename(assets_dir, url_adress)
            with open(filename, "w") as wf:
                wf.write(bs_data.prettify())

    except HTTPError as http_err:
        logging.error(f'HTTP error: {http_err}')
    except Exception as err:
        logging.error(f'Other error: {err}')

    return "Done"


def make_dirs(save_dir, url_adress):
    url_host = (urlparse(url_adress).hostname)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        logging.info('download directory created')
    assets_dir = make_assets_dirpath(save_dir, url_adress)
    if not os.path.exists(assets_dir):
        os.mkdir(assets_dir)
        logging.info('assets directory created')
    return url_host, assets_dir


def download_images(download_data):
    bs_data, assets_dir, session_, _ = download_data

    images_list = bs_data.find_all("img")
    if not images_list:
        return logging.debug("no images on page")

    make_download_list(images_list, "image", download_data)
    # download_list = filter(isAllowed,
    #                        [link.get("src") for link in images_list])
    # for link in download_list:
    #     filename = f"{assets_dir}/{os.path.split(link)[1]}"
    #     download_resourse(filename, link, session_)

    for src in images_list:
        if isAllowed(src.get("src")):
            src["src"] = os.path.join(assets_dir[1:],
                                      os.path.split(src.get("src"))[1])


def download_scripts(download_data):
    bs_data, assets_dir, session_, host = download_data

    scripts_list = bs_data.find_all("script")   # type="text/javascript")
    if not scripts_list:
        return logging.debug("no scripts to download")

    make_download_list(scripts_list, "script", download_data)
    # download_list = filter(lambda item: isLocal(item, host),
    #                        [link.get("src") for link in scripts_list])
    # for link in download_list:
    #     filename = f"{assets_dir}/{os.path.split(link)[1]}"
    #     download_resourse(filename, link, session_)

    for src in scripts_list:
        if isLocal(src.get("src"), host):
            filename = os.path.split(src.get("src"))[1]
            src["src"] = os.path.join(assets_dir[1:],
                                      filename)


def download_links(download_data):
    bs_data, assets_dir, session_, host = download_data

    links_list = bs_data.find_all("link")
    if not links_list:
        return logging.debug("unbelievable! no links to download")

    make_download_list(links_list, "link", download_data)
    # download_list = filter(lambda item: isLocal(item, host),
    #                        [link.get("href") for link in links_list])
    # for link in download_list:
    #     if os.path.splitext(link)[1]:
    #         filename = f"{assets_dir}/{os.path.split(link)[1]}"
    #         download_resourse(filename, link, session_)

    for src in links_list:
        if isLocal(src.get("href"), host):
            h, p = parse_url_adress(src.get("href"))
            if os.path.splitext(p)[1] == "":
                filename = f"{h}{p}.html"
                # logging.debug(f">>> isdir {filename}")
            else:
                filename = os.path.split(src.get("href"))[1]
                # logging.debug(f">>> is file {filename}")
            src["href"] = os.path.join(assets_dir[1:],
                                       filename)


def download_resourse(filename, link, session_):
    logging.debug(f'start download {os.path.split(filename)[1]} '
                  f'in {os.path.split(filename)[0][1:]}')
    resp = session_.get(url=link)
    if resp.status_code == 200:
        with open(filename, "wb") as wbf:
            wbf.write(resp.content)
        logging.debug('downloaded successfully')
    else:
        logging.error(f'download {os.path.split(filename)[1]} '
                      f'FAIL! Error - {resp.status_code}')


def make_download_list(list_, type_, download_data):
    _, assets_dir, session_, host = download_data
    if type_ == "image":
        download_list = filter(isAllowed,
                               [link.get("src") for link in list_])
    if type_ == "script":
        download_list = filter(lambda item: isLocal(item, host),
                               [link.get("src") for link in list_])
    if type_ == "link":
        download_list = filter(lambda item: isLocal(item, host),
                               [link.get("href") for link in list_])
    for link in download_list:
        if os.path.splitext(link)[1]:
            filename = f"{assets_dir}/{os.path.split(link)[1]}"
            download_resourse(filename, link, session_)


def isAllowed(link):
    file_ext = os.path.splitext(os.path.split(link)[1])
    if file_ext[1] in [".jpg", ".png"]:
        return True


def isLocal(link, host):
    if urlparse(link).hostname == host:  # "ru.hexlet.io":
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
