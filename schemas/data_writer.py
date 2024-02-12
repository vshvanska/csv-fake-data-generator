import csv
import os

from django.conf import settings


class DataWriter:
    def __init__(self, headers, rows, path, delimiter, quotechar):
        self.headers = headers
        self.rows = rows
        self.path = path
        self.delimiter = delimiter
        self.quotechar = quotechar

    def write_data(self):
        path = os.path.join(settings.MEDIA_ROOT, self.path)
        with open(path, mode="w", newline="") as file:
            writer = csv.writer(
                file, delimiter=self.delimiter, quotechar=self.quotechar
            )
            writer.writerow(self.headers)
            writer.writerows(self.rows)
