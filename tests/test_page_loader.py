from tempfile import TemporaryDirectory
import os
import requests_mock
# import pytest

from page_loader.page_loader import download
from page_loader.url_modifier import make_assets_path, make_path
# from page_loader.resources import check_url


# @pytest.mark.parametrize(
#     "url, expectation",
#     [
#         ("http://site.com", True),
#         ("https://www.site.com", True),
#     ]
# )
# def test_url_adress(url, expectation):
#     result = check_url(url)
#     assert result == expectation


def test_make_assets_path():
    result = make_assets_path("http://site.com/page")
    assert result == "site-com-page_files"


def test_make_path():
    result = make_path("download", "http://site.com/page")
    assert result == "download/site-com-page.html"


def test_download():
    with open("tests/fixtures/original.html", "r") as f:
        original_html = f.read()
    with open("tests/fixtures/nodejs.png", "rb") as f:
        image = f.read()
    with open("tests/fixtures/runtime.js", "rb") as f:
        script = f.read()
    with open("tests/fixtures/application.css", "rb") as f:
        style = f.read()
    with open("tests/fixtures/downloaded.html", "rb") as f:
        link_ = f.read()
    url = "https://ru.hexlet.io"
    url_image = "/assets/professions/nodejs.png"
    url_script = "/packs/js/runtime.js"
    url_style = "/assets/application.css"
    url_link = "/courses"
    expect_assets_dir = "ru-hexlet-io_files"
    expect_image_path = ("ru-hexlet-io_files/"
                         "ru-hexlet-io-assets-professions-nodejs.png")
    expect_script_path = "ru-hexlet-io_files/ru-hexlet-io-packs-js-runtime.js"
    expect_style_path = "ru-hexlet-io_files/ru-hexlet-io-assets-application.css"
    expect_link_path = "ru-hexlet-io_files/ru-hexlet-io-courses.html"

    with requests_mock.Mocker() as mock, TemporaryDirectory() as tmpd:
        mock.get(url, text=original_html)
        mock.get(url_image, content=image)
        mock.get(url_script, content=script)
        mock.get(url_style, content=style)
        mock.get(url_link, content=link_)
        download(url, tmpd)

        image_path = os.path.join(tmpd, expect_image_path)
        script_path = os.path.join(tmpd, expect_script_path)
        style_path = os.path.join(tmpd, expect_style_path)
        link_path = os.path.join(tmpd, expect_link_path)

        with open(image_path, "rb") as f:
            image_data = f.read()
        assert image_data == image

        with open(script_path, "rb") as f:
            script_data = f.read()
        assert script_data == script

        with open(style_path, "rb") as f:
            style_data = f.read()
        assert style_data == style

        with open(link_path, "rb") as f:
            link_data = f.read()
        assert link_data == link_

        current_path = os.path.join(tmpd, expect_assets_dir)
        assert len(os.listdir(current_path)) == 4

        assert len(os.listdir(tmpd)) == 2


# def test_response():
#     result = check_url('https://www.site.com')
#     assert result is True
