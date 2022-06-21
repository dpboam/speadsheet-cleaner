import logging
import os
from cleaner.processes import add_fields, drop_fields, merge
from cleaner.reader import load_sheet
from cleaner.writer import write_csv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def process():
    os.chdir('./data')
    input_file = 'ASP Contacts Consolidated 1+2_Checked 20220619.xlsx'
    data = load_sheet(input_file, 'Political Contacts')

    def clean_political_contact(row):
        row = drop_fields(row, 'Row')
        row = add_fields(row, {
            'T': 'Political Contact',
        })
        row = merge(row, ['T', 'Person Type', 'Source Sheet'], 'Person Type', merge_character=',')
        return row

    data = [clean_political_contact(row) for row in data]

    write_csv(data, 'CRM0003_political.csv')


if __name__ == '__main__':
    process()
