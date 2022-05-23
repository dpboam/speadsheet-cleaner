import re

def split_name(data, name, exceptions=None):
    output_names = ["First Name", "Surname"]
    sep = r'\s+'
    field = data.pop(name)
    splits = exceptions[field] \
        if field in exceptions \
        else re.split(sep, field)
    new_fields = dict(zip(output_names, splits))
    data.update(new_fields)
    return data


def merge_and_tag(data, fields, tags, output_field):
    values = [data.pop(k, None) for k in fields]
    field = ";".join(
        [str(v) + ":" + t for v, t in zip(values, tags) if v is not None])
    data[output_field] = field
    return data


def add_fields(data, fields):
    data.update(fields)
    return data
