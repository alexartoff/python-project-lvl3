#!/usr/bin/env python


import logging
from page_loader.url_modifier import make_assets_path, make_filename
from page_loader.resources import get_data, check_url, prepare_data
from page_loader.files_dirs import download_resources, make_assets_dir


def download(url, base):
    # check url.
    check_result, session_, resp = check_url(url)
    if check_result:
        # load original html page.
        data = get_data(resp)

        # parse html --> make dict, change data
        resource_dict = prepare_data(data, url)

        # make file_name for parsed html page and save it
        filename = make_filename(base, url)
        with open(filename, "w") as wf:
            wf.write(data.prettify())
            logging.info(f'html file downloaded and modified "{filename}"')

        # create assets directory if dict is exists
        if resource_dict:
            make_assets_dir(base, make_assets_path(url))
            # download resources (from dict)
            download_resources(resource_dict, base, session_)
        else:
            logging.info('nothing to download')

        # done, return filename
        return filename
