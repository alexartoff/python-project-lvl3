import logging
import sys


def init_logging(func):
    def wrapper():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter_stream = logging.Formatter(
            ' [ %(levelname)s ]: %(message)s'
        )
        formatter = logging.Formatter(
            '[ %(asctime)s ] - %(name)s - %(levelname)s: %(message)s'
        )

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter_stream)

        file_handler = logging.FileHandler('loader_main.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logging.basicConfig(
            format='[ %(asctime)s ] - %(levelname)s: %(message)s',
            handlers=[file_handler, stream_handler],
            level=logging.INFO
        )
        func()
    return wrapper
