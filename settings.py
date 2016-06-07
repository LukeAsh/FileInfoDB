# CALCULATE_HASHES
DIRECTORIES_LIST = [
    b'/home/luke/workspace/filesystem/filesystem_test'
]
CSV_DATABASE = 'file_hashes.csv'    # default csv file name
HASHES = ('md5', 'sha512')  # hashes to generate for each file

SAVE_EVERY_X_RESULTS = 128     # save file hashes after getting this number of results
BLOCK_SIZE = 102400   # read BLOCK_SIZE bytes at a time

# LOGGING
LOG_FILE = 'filesystem.log'