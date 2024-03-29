import logging
from bs4 import BeautifulSoup
import requests
import os
from page_loader.url_modifier import make_assets_path, make_full_link
from page_loader.url_modifier import isAllowed, isLocal, html_tag_path


ATTRIBUTE_MAPPING = {
    "img": "src",
    "script": "src",
    "link": "href"
}


def get_data(url_adress):
    session_ = requests.Session()
    if session_:
        resp = session_.get(url_adress)
        if resp.status_code == 200:
            bs_data = BeautifulSoup(resp.content, 'html.parser')
            return bs_data, session_
        raise ConnectionError(
            logging.error(f'HTTP error: {url_adress} - {resp.status_code}')
        )
    raise ConnectionError(
        logging.error("Can't perform request")
    )


def prepare_data(data, url):
    tags = []
    # filter tags by ATTRIBUTE_MAPPING, locality
    for html_tag in ATTRIBUTE_MAPPING.keys():
        filtered_by_tag = list(filter(
            lambda tag: _attr_mapping(html_tag, tag),
            data.find_all(html_tag)
        ))

        tag_link = ATTRIBUTE_MAPPING[html_tag]
        filtered_is_local = list(filter(
            lambda tag: isLocal(tag[tag_link], url),
            filtered_by_tag
        ))
        tags.extend(filtered_is_local)

    # filter tags by allowed file extension
    filtered_by_extension = list(filter(
        lambda tag: _allowed_file_ext(tag, url),
        tags
    ))
    return _get_pretty_and_assets(data, filtered_by_extension, url)


def _attr_mapping(html_tag, tag_data):
    if ATTRIBUTE_MAPPING[html_tag] in tag_data.attrs.keys():
        return True


def _allowed_file_ext(tag, url):
    src = ATTRIBUTE_MAPPING.get(tag.name)
    if tag.name != 'img' or \
            (tag.name == 'img' and isAllowed(tag.attrs[src], url)):
        return True


def _get_pretty_and_assets(data, tags, url):
    assets_path = make_assets_path(url)
    # make links and change html in source html data
    assets = []
    for tag in tags:
        link = make_full_link(
            tag[ATTRIBUTE_MAPPING.get(tag.name)],
            url
        )
        full_assets_path = os.path.join(
            assets_path,
            html_tag_path(link, url)
        )
        tag[ATTRIBUTE_MAPPING.get(tag.name)] = os.path.join(full_assets_path)
        to_list = (link, full_assets_path)
        assets.append(to_list)
    return data.prettify(), assets
