#!/usr/bin/env python


import logging
from page_loader.url_modifier import make_assets_path, make_path
from page_loader.resources import get_data, prepare_data
from page_loader.files_dirs import download_resources, make_assets_dir


# def download(url, base):
#     # check url.
#     if check_url(url):
#         # load original html page.
#         data, session_ = get_data(url)
#
#         # parse html --> make dict, change data
#         resource_dict = prepare_data(data, url)
#
#         # make file_path for parsed html page and save it
#         file_path = make_path(base, url)
#         with open(file_path, "w") as wf:
#             wf.write(data.prettify())
#             logging.info(f'html file downloaded and modified "{file_path}"')
#
#         # create assets directory if dict is exists
#         if resource_dict:
#             make_assets_dir(base, make_assets_path(url))
#             # download resources (from dict)
#             download_resources(resource_dict, base, session_)
#         else:
#             logging.info('nothing to download')
#
#         # done, return file_path
#         return file_path
#     raise Exception('URL error')


def download(url, base_dir):

    data, session_ = get_data(url)

    pretty, assets = prepare_data(data, url)
    if assets:
        make_assets_dir(base_dir, make_assets_path(url))
        download_resources(base_dir, assets, session_)
    else:
        logging.info('resources not found. continue...')

    file_path = make_path(base_dir, url)
    with open(file_path, "w") as wf:
        wf.write(pretty)
        logging.info(f'html file downloaded and modified "{file_path}"')

    if file_path:
        return file_path
    raise Exception(
        logging.error('error - no PATH for return')
    )
