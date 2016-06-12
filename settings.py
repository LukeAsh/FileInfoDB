# CALCULATE_HASHES
DIRECTORIES_LIST = [
    b'/home/luke/workspace/filesystem/filesystem_test'
    # b'/media/to_review2_wde',
    # b'/media/to_review2'
]
CSV_DATABASE = 'file_hashes.csv'    # default csv file name
HASHES = ('sha512', 'md5')  # hashes to generate for each file

SAVE_EVERY_X_RESULTS = 128     # save file hashes after getting this number of results
BLOCK_SIZE = 102400   # read BLOCK_SIZE bytes at a time

CSV_BYTE_STRING_ENCODING = 'utf-8'

# LOGGING
LOG_FILE = 'filesystem.log'

# DATABASE
DB_FILE_NAME = 'file_info.sqlite'
