def get_fieldnames(data):
    return sorted(list(set([item for row in data for item in row.keys()])))


def clean_row(original):
    return {k: v for k, v in original.items() if k is not None and v is not None}
