import csv
from .util import get_fieldnames

def write_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = get_fieldnames(data)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
