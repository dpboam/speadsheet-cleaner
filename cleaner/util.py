def get_fieldnames(data):
    return list(set([item for row in data for item in row.keys()]))


def clean_row(original):
    return {k: v for k, v in original.items() if v is not None}
