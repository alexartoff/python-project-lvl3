#!/usr/bin/env python


import os
from urllib.parse import urlparse


ATTRIBUTE_MAPPING = {"img": "src", "script": "src", "link": "href"}


def _parse_url_adress(url):
    host = str(urlparse(url).hostname).replace(".", "-")
    path = str(urlparse(url).path).replace("/", "-")
    if path == "":
        return host, ""
    return host, path if path[-1] != "-" else path[:-1]


def html_tag_path(adr, url):
    for_parse = url
    path_str = str(urlparse(adr).path)
    if urlparse(adr).hostname:
        for_parse = adr
    if not os.path.splitext(urlparse(adr).path)[1]:
        _ = urlparse(adr).path if \
            urlparse(adr).path[-1] != '/' else\
            urlparse(adr).path[:-1]
        path_str = f"{_}.html"
    host = str(urlparse(for_parse).hostname).replace(".", "-")
    path = path_str.replace("/", "-")
    return f"{host}{path}"


def make_assets_path(url):
    h, p = _parse_url_adress(url)
    return f"{h}{p}_files"


def make_path(dir_, url_adress):
    h, p = _parse_url_adress(url_adress)
    if os.path.splitext(p)[1]:
        return os.path.join(dir_, f"{h}{p}")
    return os.path.join(dir_, f"{h}{p}.html")


def isAllowed(link, url):
    file_ext = os.path.splitext(os.path.split(link)[1])
    if file_ext[1] in [".jpg", ".png"] and isLocal(link, url):
        return True


def isLocal(link, url):
    if not urlparse(link).hostname and urlparse(link).path:
        return True
    if urlparse(link).hostname == urlparse(url).hostname:
        return True


def _get_host_url(url):
    return f"{urlparse(url).scheme}://{urlparse(url).hostname}"


# def make_full_link(tag, list_, url):
#     output = []
#
#     for item in list_:
#         tag_url = item.get(ATTRIBUTE_MAPPING[tag])
#         if not urlparse(tag_url).hostname and urlparse(tag_url).path:
#             output.append(_get_host_url(url) + tag_url)
#         if urlparse(tag_url).hostname == urlparse(url).hostname:
#             output.append(tag_url)
#     return output


def make_full_link(link, url):
    if not urlparse(link).hostname and urlparse(link).path:
        link = _get_host_url(url) + link
    return link
