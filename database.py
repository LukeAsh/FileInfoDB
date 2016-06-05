"""
Idea is to put what is currently in csv into sqlite database for further analysis
"""

import sqlite3
from calculate_hashes import HASHES

DB_NAME = 'fileinfo.sqlite'


class FileInfoDatabase(object):
    def __init__(self, db_name):
        self.conn = sqlite3.connect('example.db')
        # self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        # Create the table
        hashes = [h for h in HASHES]
        hashes = ', '.join(hashes)
        self.conn.execute('create table file_info(file_path, file_name, size, ctime, mtime, atime, {0})'.format(hashes))

    def fill_table(self, csv_file_name):
        """FIll table using values form csv file
        If file_path contains file_name then remove it
        """
