def filter_list(data, field):
    return [r for r in data if r.get(field, None) is not None]


def split_to_rows_on_field(data_list, field, separator="\n"):
    output = []
    for row in data_list:
        new_rows = row.pop(field, None).split(separator)
        new_rows = [{field: r} | row for r in new_rows]
        output += new_rows

    output = filter_list(output, 'Notes')

    return output
