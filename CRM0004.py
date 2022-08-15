import logging
import os
from cleaner.processes import add_fields, clean_field_names, clean_values, drop_fields, extract_and_leave_ref, merge, rename_fields, split_name
from cleaner.reader import load_sheet
from cleaner.writer import write_csv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
source_path = '/Users/gilesdring/Library/CloudStorage/OneDrive-OpenInnovationsLimited/Projects/2022/2022-001 - Leeds 2023/Sub-projects/GoodCRM/Stories/CRM-0004'


def process():
    os.chdir('./data')
    input_file = 'Commercial Contact List Andy Mc updated Column P standard 12072022.xlsx'
    data = load_sheet(
        input_file, 'NEW Commercial contacts s\'sheet', skip_rows=1)

    contacts = []

    def cleanse(row):
        # row = drop_fields(row, 'Row')
        # row = add_fields(row, {
        #     'T': 'Political Contact',
        # })
        # row = merge(row, ['T', 'Person Type', 'Source Sheet'], 'Person Type', merge_character=',')
        row = clean_field_names(row)

        row = drop_fields(row, [
            'Commercial next Steps',
            'Commercial next steps due',
            'Commercial Next Steps Person',
            "All new Org records being created need the Fundraising Stage field, defaulted to 'Unknown'",
            'Leeds 2023 Strategic Lead contact |(email)',
        ])

        row = rename_fields(row, {
            'Leeds2023 Main Contact (email)': 'Leeds 2023 Main Contact for Commercial',
            'Sector of Business (see sample list below). Add more if not in list': 'Sector',
            'Brief Details': 'Notes',
        })

        row = extract_and_leave_ref(
            row, [
                'Commercial Primary Contact Name',
                'Commercial Primary Contact email',
                'Commercial Primary Contact number',
            ], 'Commercial Primary Contact', 'Commercial Primary Contact email', contacts)
        row = extract_and_leave_ref(
            row, [
                'Commrcial Secondary Contact Name (if needed or known)',
                'Commercial Secondary Contact Email',
                'Commcercial Secondary Contact number if known',
            ], 'Commercial Secondary Contact', 'Commercial Secondary Contact Email', contacts)

        row = clean_values(row, 'Partnership', null_values=['???????'])

        return row

    def cleanse_contacts(row):
        row = rename_fields(row, {
            'Commercial Primary Contact Name': 'Name',
            'Commercial Primary Contact email': 'Email',
            'Commercial Primary Contact number': 'Phone',
            'Commrcial Secondary Contact Name (if needed or known)': 'Name',
            'Commercial Secondary Contact Email': 'Email',
            'Commcercial Secondary Contact number if known': 'Phone',
        })
        row = split_name(row, 'Name', {
            'Corinne Bailey Rae': ['Corinne', 'Bailey Rae'],
            'Maria Terron Busteros': ['Maria', 'Terron Busteros'],
            'Natalia Amelia Saied': ['Natalia Amelia', 'Saied'],
            'GRAFT': ['GRAFT', None],
            'Rheima': ['Rheima', None],
        })
        row = clean_values(row, 'Phone', null_values=['unknown'])

        return row

    data = [cleanse(row) for row in data]
    contacts = [cleanse_contacts(row) for row in contacts]

    write_csv(data, 'CRM0004_organisations.csv')
    write_csv(contacts, 'CRM0004_people.csv')


def process_20220812():
    os.chdir('./data')
    input_file = 'CRM-0004-consolidated-20220812.xlsx'
    people_preload = load_sheet(
        input_file, 'People Preload')
    organisations = load_sheet(
        input_file, 'Organisations')
    people = load_sheet(
        input_file, 'People')

    def process_people(person):
        person = clean_field_names(person)
        person['Person Type'] = ','.join(
            [type.strip() for type in person['Person Type'].split(',')])

        def map_checkbox(value):
            return {
                'Yes': 1,
                'Y': 1,
                'N': 0,
                '': 0
            }.get(value.strip(), 'UNKNOWN')
        person['Brief Signed Off'] = map_checkbox(
            person.get('Brief Signed Off', ''))
        person['Contract Issued'] = map_checkbox(
            person.get('Contract Issued', ''))
        person['Contract Signed'] = map_checkbox(
            person.get('Contract Signed', ''))
        person['Paid'] = map_checkbox(person.get('Paid', ''))
        return person

    people_preload = [process_people(person) for person in people_preload]
    people = [process_people(person) for person in people]

    write_csv(people_preload, 'CRM0004_20220812_people_preload.csv')
    write_csv(organisations, 'CRM0004_20220812_organisations.csv')
    write_csv(people, 'CRM0004_20220812_people.csv')


# 'CRM_0004.7_Making a Stand Contact Sheet 250722.xlsx'

if __name__ == '__main__':
    process_20220812()
