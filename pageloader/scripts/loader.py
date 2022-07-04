#!/usr/bin/env python


from pageloader.cli import parse_args
from pageloader.page_loader import download


def main():
    args = parse_args()
    filepath = download(args.output, args.url_adress)
    print(filepath)


if __name__ == "__main__":
    main()
