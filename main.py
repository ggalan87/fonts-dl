import argparse
from sites import *


def main(args):
    site = initialize_site(args.site)
    site.download()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download fonts.')
    parser.add_argument('--site', default='aka-acid', choices=['aka-acid'], type=str, help='Which site to download from')
    args = parser.parse_args()

    main(args)


