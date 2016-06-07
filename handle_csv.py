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
            print(line)
            lines.append(line)
    return lines
