from calendar import c
from os import chdir
from cleaner import load_sheet, write_csv, add_fields, drop_fields, filter_list, extract_and_leave_ref, rename_fields, split_name


def process_staff_data():
    chdir('./data')
    infile = 'FR Contacts Funding List.xlsx'
    data = load_sheet(infile, sheet="Corporate")
    data = filter_list(data, 'Name')

    contacts = []

    def process_fundraising_org(record):
        record = add_fields(record, fields={
            "Organisation Type": "Fundraising"
        })

        record = drop_fields(record, ['Relationship Type2'])

        record = extract_and_leave_ref(record, ['Main contact', 'Role', 'Email'], 'Main Contact', 'Email', contacts)
        record = extract_and_leave_ref(record, ['Secondary Contact', 'Role.', 'Email.'], 'Secondary Contact', 'Email.', contacts)

        record = drop_fields(record, ['Leeds 2023 Relationship Lead'])
        record = drop_fields(record, ['Leeds 2023 Relationship Support'])

        record = drop_fields(record, ['Notes'])

        record = drop_fields(record, ['Next Step', 'Due Date', 'Who to complete?'])
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

    data = [process_fundraising_org(r) for r in data]
    contacts = [process_contacts(r) for r in contacts]
    write_csv(data, 'CRM0002_organisations.csv')
    write_csv(contacts, 'CRM0002_contacts.csv')


if __name__ == "__main__":
    process_staff_data()
