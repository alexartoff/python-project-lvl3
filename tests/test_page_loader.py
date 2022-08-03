from tempfile import TemporaryDirectory
import os
import requests_mock
import pytest
import pytest_cov

# from pageloader.scripts import loader
from pageloader.page_loader import download
from pageloader.pathwork import make_assets_dir, make_filename


def test_url():
    pass


@pytest.mark.parametrize('save_dir, expectation',
                         [
                            ('download',
                             'download/site-com-page_files'
                            ),
                            ('download/folder',
                             'download/folder/site-com-page_files'
                            ),
                         ])
def test_dir(save_dir, expectation):
    result = make_assets_dir(save_dir, "http://site.com/page")
    assert result == expectation


def test_file():
    result = make_filename("download", "http://site.com/page")
    assert result == "download/site-com-page.html"


def test_download():
    with open("tests/fixtures/original.html", "r") as f:
        original_html = f.read()
    with open("tests/fixtures/downloaded.html", "r") as f:
        downloaded_html = f.read()
    with open("tests/fixtures/nodejs.png", "rb") as f:
        image = f.read()
    with open("tests/fixtures/runtime.js", "rb") as f:
        script = f.read()
    with open("tests/fixtures/application.css", "rb") as f:
        style = f.read()
    url = "https://ru.hexlet.io/courses"
    url_image = "/assets/professions/nodejs.png"
    url_script = "/packs/js/runtime.js"
    url_style = "/assets/application.css"
    expect_assets_dir = "ru-hexlet-io-courses_files"
    expect_filename = "ru-hexlet-io-courses.html"
    expect_image_path = "ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png"
    expect_script_path = "ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js"
    expect_style_path = "ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css"

    with requests_mock.Mocker() as mock, TemporaryDirectory() as tmpd:
        mock.get(url, text=original_html)
        mock.get(url_image, content=image)
        mock.get(url_script, content=script)
        mock.get(url_style, content=style)
        download(tmpd, url)

        # html_path = os.path.join(tmpd, expect_assets_dir, expect_filename)
        image_path = os.path.join(tmpd, expect_image_path)
        script_path = os.path.join(tmpd, expect_script_path)
        style_path = os.path.join(tmpd, expect_style_path)

        # with open(html_path, "r") as f:
        #     html_data = f.read()
        # assert html_data == downloaded_html

        with open(image_path, "rb") as f:
            image_data = f.read()
        assert image_data == image

        with open(script_path, "rb") as f:
            script_data = f.read()
        assert script_data == script

        with open(style_path, "rb") as f:
            style_data = f.read()
        assert style_data == style

        current_path = os.path.join(tmpd, expect_assets_dir)
        assert len(os.listdir(current_path)) == 4


def test_download_resourse():
    pass


def test_response():
    pass
