#!/usr/bin/env python


import logging
from page_loader.url_modifier import make_assets_path, make_filename
from page_loader.resources import get_data, check_url, prepare_data
from page_loader.files_dirs import download_resources, make_assets_dir


def download(url, base):
    # 1. check url.
    check_result, session_, resp = check_url(url)
    if check_result:
        # 2. load original html page.
        data = get_data(resp)

    # 3&4. parse html --> make dict, change data
    resource_dict = prepare_data(data, url)
    # print(resource_dict)

    # 5. make file_name for parsed html page and save it
    filename = make_filename(base, url)
    with open(filename, "w") as wf:
        wf.write(data.prettify())
        logging.info(f'html file downloaded and modified "{filename}"')

    # 6. create assets directory if dict is exist
    if resource_dict:
        make_assets_dir(base, make_assets_path(url))
        # 7. download resources (from dict)
        download_resources(resource_dict, base, session_)
    else:
        logging.info('nothing to download')

    # 8. done, return filename
    return filename


# def download_(url_adress, base_dir_path):
#     logging.info('page-loader started!')
#     logging.info(f'checking url - {url_adress}')
#     check_result, session_, resp = check_url(url_adress)
#     if check_result:
#         assets_dir_path = make_assets_path(url_adress)
#         dirs = (base_dir_path, assets_dir_path)
#         make_assets_dir(dirs)
#         data = get_data(url_adress,
#                         base_dir_path,
#                         assets_dir_path,
#                         session_,
#                         resp)

#     for tag in ["img", "script", "link"]:
#         logging.info(f'searching data with tag <{tag}>...')
#         download_data(tag, data)
#         change_html(tag, data)

#     logging.info(f'writing finaly edited html page to "{base_dir_path}/"')
#     filename = make_filename(base_dir_path, url_adress)
#     bs_data, _, _, _, _ = data
#     with open(filename, "w") as wf:
#         wf.write(bs_data.prettify())

#     if os.path.exists(filename):
#         return filename
