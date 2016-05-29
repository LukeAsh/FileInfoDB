"""
Traverse given directory, get list of all available files (full path)
the calculate secure hashes and write it along with file size to csv file

Currently checking WD Elements
    '''
    lvscan
    lvchange -ay /dev/wde
    for i in `ls -x1 /dev/wde`;do udisks --mount /dev/wde/$i; don
    '''
"""
import csv
import hashlib
import logging as log
import os

DIRECTORIES_LIST = [
    '/media/backup',
    '/media/daito_backup',
    '/media/to_review',
    '/media/media',
    '/media/daitoryu',
    '/media/to_review2'
]
CSV_DATABASE = 'file_hashes.csv'
HASHES = ('md5', 'sha512')


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
    hashes = {h: None for h in HASHES}
    try:
        with open(filepath, 'rb') as f:
            file_content = f.read()
            for h_name in hashes.keys():
                hashes[h_name] = getattr(hashlib, h_name)(file_content).hexdigest()
    except PermissionError as e:
        log.exception(e)
    return hashes


def save_to_csv(data, filename=CSV_DATABASE):
    """
    Write FileInfo data to csv file
    :return:
    """
    log.info('data: {0}'.format(data))
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        for file_info in data:
            writer.writerow(file_info.get_attributes())


def process_directories(directories_list=DIRECTORIES_LIST):
    file_info_list = []
    for directory in directories_list:
        f_paths = get_all_files_from_dir(directory)
        for f_path in f_paths:
            hashes = generate_hashes_from_file(f_path)
            """log.debug('f: {filepath} hashes: {hashes}'.format(
                filepath=f_path,
                hashes=generate_hashes_from_file(f_path))
            )"""
            file_info_list.append(FileInfo(f_path, hashes=hashes))
    save_to_csv(data=file_info_list)


class FileInfo(object):
    def __init__(self, path, hashes=None):
        self.path = path
        self.name = os.path.basename(path)
        self.size = os.path.getsize(self.path)
        self.ctime = os.path.getctime(self.path)
        self.mtime = os.path.getmtime(self.path)
        self.atime = os.path.getatime(self.path)
        self.hashes = hashes

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