"""
Idea is to put what is currently in csv into sqlite database for further analysis
"""
import csv
import sqlite3
import logging as log

from calculate_hashes import FileInfo
import handle_csv
import settings


# configure logger
log.basicConfig(filename=settings.LOG_FILE, level=log.DEBUG)


class FileInfoDatabase(object):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(settings.DB_FILE_NAME)
        # self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        # Create the table
        hashes = [h for h in settings.HASHES]
        hashes = ', '.join(hashes)
        try:
            self.conn.execute('create table file_info(file_path, file_name, size, ctime, mtime, atime, {0})'.format(hashes))
        except sqlite3.OperationalError:
            log.warning('Creation of table file_info failed. maybe it already exists?')

    def fill_table(self, csv_file_name):
        """FIll table using values form csv file
        If file_path contains file_name then remove it
        """
        with open(csv_file_name, 'r', newline='') as f:
            reader = csv.reader(f)
            for line in reader:
                file_info_data = [handle_csv.convert_string_representation_to_bytes(bs) for bs in line[0:2]]
                file_info_data += line[2:]
                fi = FileInfo(file_info_data=file_info_data)
                log.debug(fi.get_attributes())


def main():
    db = FileInfoDatabase(db_name=settings.DB_FILE_NAME)
    db.create_table()
    db.fill_table(settings.CSV_DATABASE)


if __name__ == '__main__':
    main()