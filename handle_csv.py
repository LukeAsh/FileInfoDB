import settings


def save_to_csv(data, filename=settings.CSV_DATABASE):
    """
    Write FileInfo data to csv file
    :return:
    """
    log.debug('Saving results to csv file')
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        for file_info in data:
            writer.writerow(file_info.get_attributes())