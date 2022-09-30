import os
from urllib.parse import urlparse


ATTRIBUTE_MAPPING = {
    "img": "src",
    "script": "src",
    "link": "href"
}
ALLOWED_EXTENSIONS = [".jpg", ".png"]


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
    host, path = _parse_url_adress(url)
    return f"{host}{path}_files"


def make_path(dir_, url_adress):
    host, path = _parse_url_adress(url_adress)
    if os.path.splitext(path)[1]:
        return os.path.join(dir_, f"{host}{path}")
    return os.path.join(dir_, f"{host}{path}.html")


def isAllowed(link, url):
    file_ext = os.path.splitext(os.path.split(link)[1])
    if file_ext[1] in ALLOWED_EXTENSIONS and isLocal(link, url):
        return True


def isLocal(link, url):
    if not urlparse(link).hostname and urlparse(link).path:
        return True
    if urlparse(link).hostname == urlparse(url).hostname:
        return True


def _get_host_url(url):
    return f"{urlparse(url).scheme}://{urlparse(url).hostname}"


def make_full_link(link, url):
    if not urlparse(link).hostname and urlparse(link).path:
        link = _get_host_url(url) + link
    return link
