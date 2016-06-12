"""
Idea is to put what is currently in csv into sqlite database for further analysis
"""
import csv
import sqlite3
import sys
import logging as log

from calculate_hashes import FileInfo
import handle_csv
import settings


# configure logger
log.basicConfig(filename=settings.LOG_FILE, level=log.DEBUG)


class FileInfoDatabase(object):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(settings.DB_FILE_NAME)
        self.hashes = ', '.join([h for h in settings.HASHES])   # for example 'sha512, md5'
        # database operations
        self.db_op = {
            'create_table': 'create table file_info(file_path, file_name, size, ctime, mtime, atime, {0})'.format(
                self.hashes),
            'insert_into_many': 'insert into file_info(file_path, file_name, size, ctime, mtime, atime, {hashes}) \
            values (?, ?, ?, ?, ?, ?, {hv})'.format(
                hashes=self.hashes,
                hv=', '.join(['?' for i in range(len(settings.HASHES))])),
            'delete_duplicates': 'delete from file_info where rowid not in\
            (select min(rowid) from file_info group by\
            file_info.md5,\
            file_info.sha512,\
            file_info.file_name,\
            file_info.file_path,\
            file_info.size);',
            'list_duplicates_by_sha512': 'select * from file_info where sha512 in (\
            select sha512 from file_info group by file_info.sha512 having count(*)>1)\
            order by sha512;',
        }

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        # Create the table
        try:
            self.conn.execute(self.db_op['create_table'])
        except sqlite3.OperationalError:
            log.warning('Creation of table file_info failed. maybe it already exists?')

    def fill_table(self, csv_file_name):
        """FIll table using values form csv file
        If file_path contains file_name then remove it
        """
        values = []
        with open(csv_file_name, 'r', newline='') as f:
            reader = csv.reader(f)
            for index, line in enumerate(reader):
                file_info_data = [handle_csv.convert_string_representation_to_bytes(bs) for bs in line[0:2]]
                file_info_data += line[2:]
                fi = FileInfo(file_info_data=file_info_data)
                log.debug(fi.get_attributes())
                values.append(tuple(fi.get_attributes()))
                if index % 1024 == 0 and index != 0:
                    log.debug('inserting data to database, line {0}'.format(index))
                    self.conn.executemany(self.db_op['insert_into_many'], values)
                    values = []
            if values:
                log.debug('inserting data to database, line {0}'.format(index))
                self.conn.executemany(self.db_op['insert_into_many'], values)
        # TODO: handle file_name in dir_name for old-style files

    def delete_duplicated_rows_in_db(self):
        """Remove duplicates from sqlite database
        """
        self.conn.execute(self.db_op['delete_duplicates'])

    def duplicates_by_sha512(self):
        """Return duplicates grouped by sha512"""
        return self.conn.execute(self.db_op['list_duplicates_by_sha512'])

    def group_rows_by_sha512(self):
        """Gather rows with the same sha512 and send to next method
        """
        sha512 = None
        group = []
        for row in self.duplicates_by_sha512():
            fi = FileInfo(file_info_data=row)
            if fi.hashes['sha512'] == sha512:
                group.append(fi)
            else:
                if group and len(group) > 1:
                    self.delete_duplicated_files(group)
                    group = []
                else:
                    group.append(fi)
                    sha512 = fi.hashes['sha512']

    def delete_duplicated_files(self, file_info_list):
        """Remove duplicated files
        criteria for deletion:
        - file_path contains to_review2_wde
        - file_path is longest one
        """
        log.debug('ttt {0}'.format(file_info_list))
        log.debug('full path {0}'.format(file_info_list[0].full_path))
        paths = []
        paths_to_delete = []
        # for fi in file_info_list:
        #     if fi.path


def main(csv_database):
    db = FileInfoDatabase(db_name=settings.DB_FILE_NAME)
    # db.create_table()
    # db.fill_table(csv_database)
    # db.delete_duplicated_rows_in_db()
    db.group_rows_by_sha512()


if __name__ == '__main__':
    main('file_hashes.csv')
