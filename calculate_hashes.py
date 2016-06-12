"""
Traverse given directory, get list of all available files (full path)
the calculate secure hashes and write it along with file size to csv file

os.walk returns byte strings instead of unicode strings if you pass byte string as argument

What you end up is settings.CSV_DATABASE file with:
dir_name, file_name, size, ctime, mtime, atime, [hash for hash in settings.HASHES]
"""
import functools
import hashlib
import logging as log
import os

from handle_csv import save_to_csv
import settings

# configure logger
log.basicConfig(filename=settings.LOG_FILE, level=log.DEBUG)


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
            for buffer in iter(functools.partial(f.read, settings.BLOCK_SIZE), b''):
                for _hash in h:
                    h[_hash].update(buffer)
        for h_name in hashes.keys():
            hashes[h_name] = h[h_name].hexdigest()
    except PermissionError as e:
        log.warning('Couldn\'t access file {fpath}'.format(fpath=filepath))
        log.exception(e)
    return hashes


def process_directories(directories_list):
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
            file_info_list.append(FileInfo(full_path=f_path, hashes=hashes))
            index += 1
            file_info_list = save_intermediate_results(file_info_list, index)
    save_to_csv(data=file_info_list)


def save_intermediate_results(file_info_list, index):
    # save every settings.SAVE_EVERY_X_RESULTS files
    if index % settings.SAVE_EVERY_X_RESULTS == 0 and index != 0:
        save_to_csv(data=file_info_list)
        return []
    else:
        return file_info_list


class FileInfo(object):
    def __init__(self, full_path=None, hashes=None, file_info_data=None):
        # path is byte string so encoding is needed
        if file_info_data is None:
            self.full_path = full_path
            self.dir_name = os.path.dirname(self.full_path)
            self.name = os.path.basename(self.full_path)
            self.size = os.path.getsize(self.full_path)
            self.ctime = os.path.getctime(self.full_path)
            self.mtime = os.path.getmtime(self.full_path)
            self.atime = os.path.getatime(self.full_path)
            self.hashes = hashes    # {'sha512': '9d6f3a6e9e7faacaceecaaa1417461c9fe5cd6268b9055d30518542b04272a437865\
            # af2dc709215957592d896237b1837a9639ec806582a92c941b9c7015d971', 'md5': 'b5a8ecb1e6292a676c2a27ce8f3f0ad0'}
        else:
            self.full_path = file_info_data[0] + b'/' + file_info_data[1]
            self.dir_name = file_info_data[0]
            self.name = file_info_data[1]
            self.size = file_info_data[2]
            self.ctime = file_info_data[3]
            self.mtime = file_info_data[4]
            self.atime = file_info_data[5]
            self.hashes = file_info_data[6:]    # list of hashes in same order as in settings.HASHES
            self.hashes = {settings.HASHES[index]: element for index, element in enumerate(self.hashes)}

    def __repr__(self):
        attributes = self.get_attributes()
        return ' '.join(map(str, attributes))

    def get_attributes(self):
        """Return output for csv writer
        Output is compatible with row format from database using query 'select * from table;'
        :return: output for csv writer
        """
        out = [
            self.dir_name,
            self.name,
            self.size,
            self.ctime,
            self.mtime,
            self.atime,
        ]
        hashes = [self.hashes[h] for h in settings.HASHES]
        return tuple(out + hashes)


def main():
    process_directories(settings.DIRECTORIES_LIST)

if __name__ == '__main__':
    main()
