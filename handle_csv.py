import csv
import logging as log

import settings


def save_to_csv(data, file_name=settings.CSV_DATABASE):
    """
    Write FileInfo data to csv file
    :return:
    """
    log.debug('Saving results to csv file')
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        for file_info in data:
            writer.writerow(file_info.get_attributes())


def read_csv(file_name):
    lines = []
    with open(file_name, 'r', newline='') as f:
        reader = csv.reader(f)
        for line in reader:
            lines.append(line)
    return lines


def convert_string_representation_to_bytes(bs):
    """
    :param bs:  "b'/home/luke/workspace/filesystem/filesystem_test'"
                "b'\\xe7\\x99\\x98T\\xc2\\x98#%&#\\xde\\x87\\xc4\\x91\\xe0\\xa6\\x87'"
    :return:    b'/home/luke/workspace/filesystem/filesystem_test'
                b'\\xe7\\x99\\x98T\\xc2\\x98#%&#\\xde\\x87\\xc4\\x91\\xe0\\xa6\\x87'
    """
    return bytes(bs.lstrip("b'").rstrip("'"), encoding=settings.CSV_BYTE_STRING_ENCODING)
