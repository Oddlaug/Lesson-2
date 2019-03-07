# -*- coding:utf-8 -*-
import os.path
import hashlib
import optparse


def is_exists(file: str) -> bool:
    return os.path.exists(file) and os.path.isfile(file)


def get_file_gen(file: str) -> object:
    if is_exists(file):
        with open(file, 'rb') as f:
            for line in f:
                yield line
    else:
        print('Bad input data!')


def get_file_line_md5(file: str) -> set:
    lines_md5_hashes = set()

    for line in get_file_gen(file):
        md5_hash = hashlib.md5()
        md5_hash.update(line)
        lines_md5_hashes.add(md5_hash.hexdigest())
        print(md5_hash.hexdigest())

    return lines_md5_hashes


def main():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--path",
                      dest="path",
                      default=False,
                      action="store_true",
                      help="path to processed file"
                      )

    (_, args) = parser.parse_args()
    try:
        file = rf'{args[0]}'
        get_file_line_md5(file)
    except IndexError:
        print('Usage: python generator.py -p <path to file>')


if __name__ == '__main__':
    main()
