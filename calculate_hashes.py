"""
Traverse given directory, get list of all available files (full path)
the calculate secure hashes and write it along with file size to csv file

os.walk returns byte strings instead of unicode strings if you pass byte string as argument

What you end up is settings.CSV_DATABASE file with:
full_path, file_name, size, ctime, mtime, atime, [hash for hash in settings.HASHES]
"""
import csv
import functools
import hashlib
import logging as log
import os

from handle_csv import save_to_csv
import settings

DIRECTORIES_LIST = [
    b'/media/MasterCollection'
]
BLOCK_SIZE = 102400   # read BLOCK_SIZE bytes at a time
SAVE_EVERY_X_RESULTS = 128     # save file hashes after getting 1024 results

# configure logger
log.basicConfig(filename='filesystem.log', level=log.DEBUG)


def get_all_files_from_dir(directory):
    gen = os.walk(directory)
    fn_list = []
    for dirpath, dirnames, filenames in gen:
        for fn in filenames:
            path = os.path.abspath(os.path.join(dirpath, fn))
            if os.path.isfile(path):
                fn_list.append(path)
        for dn in dirnames:
            fn_list += get_all_files_from_dir(dn)
    return fn_list


def generate_hashes_from_file(filepath):
    log.info('Generating hash for file {fpath}'.format(fpath=filepath))
    hashes = {h: None for h in settings.HASHES}
    try:
        h = {h_name: getattr(hashlib, h_name)() for h_name in hashes.keys()}
        with open(filepath, 'rb') as f:
            for buffer in iter(functools.partial(f.read, BLOCK_SIZE), b''):
                for _hash in h:
                    h[_hash].update(buffer)
        for h_name in hashes.keys():
            hashes[h_name] = h[h_name].hexdigest()
    except PermissionError as e:
        log.warning('Couldn\'t access file {fpath}'.format(fpath=filepath))
        log.exception(e)
    return hashes


def process_directories(directories_list=DIRECTORIES_LIST):
    file_info_list = []
    index = 0
    for directory in directories_list:
        log.info('Processing directory {dir}'.format(dir=directory))
        f_paths = get_all_files_from_dir(directory)
        for f_path in f_paths:
            hashes = generate_hashes_from_file(f_path)
            """log.debug('f: {filepath} hashes: {hashes}'.format(
                filepath=f_path,
                hashes=generate_hashes_from_file(f_path))
            )"""
            file_info_list.append(FileInfo(f_path, hashes=hashes))
            index += 1
            file_info_list = save_intermediate_results(file_info_list, index)
    save_to_csv(data=file_info_list)


def save_intermediate_results(file_info_list, index):
    # save every SAVE_EVERY_X_RESULTS files
    if index%SAVE_EVERY_X_RESULTS == 0 and index != 0:
        save_to_csv(data=file_info_list)
        return []
    else:
        return file_info_list


class FileInfo(object):
    def __init__(self, path, hashes=None):
        self.path = path
        self.name = os.path.basename(path)
        self.size = os.path.getsize(self.path)
        self.ctime = os.path.getctime(self.path)
        self.mtime = os.path.getmtime(self.path)
        self.atime = os.path.getatime(self.path)
        self.hashes = hashes

    def __repr__(self):
        attributes = self.get_attributes()
        return ' '.join(map(str, attributes))

    def get_attributes(self):
        """
        :return: output for csv writer
        """
        out = [
            self.path,
            self.name,
            self.size,
            self.ctime,
            self.mtime,
            self.atime,
        ]
        hashes = [self.hashes[h] for h in self.hashes]
        return out + hashes


def main():
    process_directories()

if __name__ == '__main__':
    main()
