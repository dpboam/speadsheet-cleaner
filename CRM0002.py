from calendar import c
from os import chdir

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

        return record

    def process_contacts(contact):
        contact = rename_fields(contact, {
            'Main contact': 'Name',
            'Secondary Contact': 'Name',
            'Role.': 'Role',
            'Email.': 'Email'
        })

        # contact = split_name(contact, 'Name')

        return contact

    def process_notes(note):
        note = rename_fields(note, {
            'Name': 'Organisation',
            'Notes': 'Content'
        })

        note = add_fields(note, {
            'Heading': 'Note imported from original spreadsheet'
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
