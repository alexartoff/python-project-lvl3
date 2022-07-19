#!/usr/bin/env python


import os
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup


# https://ru.hexlet.io/courses/python-basics
def download(save_dir, url_adress):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    try:
        request = requests.get(url_adress)
        if request.status_code == 200:
            bs_data = BeautifulSoup(request.content, 'html.parser')
            # with open("out.html", "wb") as wf:
            #     wf.write(request.content)
            assets_dir = make_assets_dirpath(save_dir, url_adress)
            if not os.path.exists(assets_dir):
                os.mkdir(assets_dir)
            download_images(bs_data, assets_dir)
            download_scripts(bs_data, assets_dir)
            download_links(bs_data, assets_dir)
    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Other error: {err}')

    return None


def download_images(bs_data, assets_dir):
    images_list = bs_data.find_all("img")
    if images_list:
        # print(image_list, assets_dir)
        image_link_list = [img_link.get("src") for img_link in images_list]
        for src in images_list:
            src["src"] = os.path.join(assets_dir,
                                      os.path.split(src.get("src"))[1])
    # print(image_list)
    for link in image_link_list:
        filename = f"{assets_dir}/{os.path.split(link)[1]}"
        if not os.path.exists(filename):
            request = requests.get(url=link)
            if request.status_code == 200:
                with open(filename, "wb") as wbf:
                    wbf.write(request.content)


def download_scripts(bs_data, assets_dir):
    scripts_list = bs_data.find_all("script", type="text/javascript")
    print(scripts_list)
    if scripts_list:
        download_list = filter(isLocal,
                               [link.get("src") for link in scripts_list])
        # for src in scripts_list:
        #     print(src.get("src"))
        #     # if isLocal(src.get("src")):
        #     filename = os.path.split(src.get("src"))[1]
        #     src["src"] = os.path.join(assets_dir,
        #                               filename)
        for link in download_list:
            print(link)
            filename = f"{assets_dir}/{os.path.split(link)[1]}"
            print(filename)
            # if not os.path.exists(filename):
            request = requests.get(url=link)
            if request.status_code == 200:
                with open(filename, "wb") as wbf:
                    wbf.write(request.content)


def download_links(bs_data, assets_dir):
    links_list = bs_data.find_all("link")
    if links_list:
        download_list = filter(isLocal,
                               [link.get("href") for link in links_list])
        for src in links_list:
            # print(src.get("href"), os.path.split(src.get("href")))
            if isLocal(src.get("href")):
                h, p = parse_url_adress(src.get("href"))
                if isDir(src.get("href")):
                    filename = f"{h}{p}.html"
                else:
                    filename = os.path.split(src.get("href"))[1]
                src["href"] = os.path.join(assets_dir,
                                           filename)
        for link in download_list:
            if isDir(link):
                filename = make_filename(assets_dir, link)
                with open(filename, "w") as wf:
                    wf.write(bs_data.prettify())
            else:
                filename = f"{assets_dir}/{os.path.split(link)[1]}"
                # if not os.path.exists(filename):
                request = requests.get(url=link)
                if request.status_code == 200:
                    with open(filename, "wb") as wbf:
                        wbf.write(request.content)


def isLocal(link):
    if urlparse(link).hostname == "ru.hexlet.io":
        return True
    return False


def isDir(path):
    splt = os.path.splitext(os.path.split(path)[1])
    if splt[1] == "":
        return True
    return False


def parse_url_adress(url_adress):
    host = (urlparse(url_adress).hostname).replace(".", "-")
    path = (urlparse(url_adress).path).replace("/", "-")
    return (host, path)


def make_filename(save_dir, url_adress):
    h, p = parse_url_adress(url_adress)
    return os.path.join(save_dir, f"{h}{p}.html")


def make_assets_dirpath(save_dir, url_adress):
    h, p = parse_url_adress(url_adress)
    return os.path.join(save_dir, f"{h}{p}_files")
