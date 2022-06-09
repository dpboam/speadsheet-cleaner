from os import chdir

from pip import main

from cleaner.list import split_to_rows_on_field, filter_list
from cleaner.processes import extract_and_take_ref, add_fields, drop_fields, extract_and_leave_ref, rename_fields, split_name
from cleaner.reader import load_sheet
from cleaner.writer import write_csv


def process_staff_data():
    chdir('./data')
    infile = 'FR Contacts Funding List.xlsx'
    data = load_sheet(infile, sheet="Corporate")
    data = filter_list(data, 'Name')

    contacts = []
    notes = []

    def process_fundraising_org(record):
        record = add_fields(record, fields={
            "Organisation Type": "Fundraising"
        })

        fake_emails = ';'.join(['NOREPLY@{}'.format(x) for x in set([e.split('@')[1].lower()
                               for e in [record.get('Email', None), record.get('Email.', None)] if e and '@' in e])])
        record = add_fields(record, {
            'Organisation Email': fake_emails
        })

        record = drop_fields(record, ['Relationship Type2'])

        record = extract_and_leave_ref(
            record, ['Main contact', 'Role', 'Email'], 'Main Contact', 'Email', contacts)
        record = extract_and_leave_ref(record, [
                                       'Secondary Contact', 'Role.', 'Email.'], 'Secondary Contact', 'Email.', contacts)

        record = rename_fields(record, {
            'Leeds 2023 Relationship Lead': 'Relationhip Lead',
            'Leeds 2023 Relationship Support': 'Relationship Support'
        })

        record = extract_and_take_ref(record, ['Notes'], 'Name', notes)

        record = drop_fields(
            record, ['Next Step', 'Due Date', 'Who to complete?'])
        record = drop_fields(record, ['Action Archive'])

        record = add_fields(record, {
            'Organisation Type': 'Fundraising'
        })

        return record

    def process_contacts(contact):
        contact = rename_fields(contact, {
            'Main contact': 'Name',
            'Secondary Contact': 'Name',
            'Role.': 'Role',
            'Email.': 'Email'
        })

        contact = split_name(contact, 'Name', exceptions={
            "Richard Bickers + Alaistair Gordon": ["Richard", "Bickers"],
            "Martijn de Lange": ["Martin", "de Lange"],
            "Professor Charles Egbu": ["Charles", "Egbu (Professor)"],
            "Eleanor Trigwell or Lee Savage - Was at WNY Property Forum that ASP Presented at 09.09.21": ["Eleanor", "Trigwell"],
            "Dr Edward Ziff": ["Edward", "Ziff (Dr)"]
        })

        contact = add_fields(contact, {
            'Person Type': 'Fundraising'
        })

        return contact

    def process_notes(note):
        note = rename_fields(note, {
            'Name': 'Organisation',
            'Notes': 'Content'
        })

        note = add_fields(note, {
            'Heading': 'Note imported from fundraising spreadsheet'
        })
        return note

    data = [process_fundraising_org(r) for r in data]
    contacts = [process_contacts(r) for r in contacts]
    write_csv(data, 'CRM0002_organisations.csv')
    write_csv(contacts, 'CRM0002_contacts.csv')

    notes = filter_list(notes, 'Notes')
    notes = split_to_rows_on_field(notes, 'Notes', separator="|")
    notes = [process_notes(r) for r in notes]

    write_csv(notes, 'CRM0002_notes.csv')


if __name__ == "__main__":
    process_staff_data()
