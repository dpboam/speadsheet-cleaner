from os import chdir
from cleaner import load_sheet, write_csv, add_fields, drop_fields, filter_list


def process_staff_data():
    chdir('./data')
    infile = 'FR Contacts Funding List.xlsx'
    data = load_sheet(infile, sheet="Corporate")
    data = filter_list(data, 'Name')

    def process_fundraising_org(record):
        record = add_fields(record, fields={
            "Organisation Type": "Fundraising"
        })

        record = drop_fields(record, ['Relationship Type2'])

        record = drop_fields(record, ['Main contact', 'Role', 'Email'])
        record = drop_fields(record, ['Secondary Contact', 'Role.', 'Email.'])

        record = drop_fields(record, ['Leeds 2023 Relationship Lead'])
        record = drop_fields(record, ['Leeds 2023 Relationship Support'])

        record = drop_fields(record, ['Notes'])

        record = drop_fields(record, ['Next Step', 'Due Date', 'Who to complete?'])
        record = drop_fields(record, ['Action Archive'])

        return record

    data = [process_fundraising_org(r) for r in data]
    write_csv(data, 'CRM0002_organisations.csv')


if __name__ == "__main__":
    process_staff_data()
