import logging
import re
from .util import clean_row


def split_name(data, name, exceptions=None):
    if not data or not name in data.keys():
        return data
    output_names = ["First Name", "Surname"]
    sep = r'\s+'
    field = data.pop(name).strip()
    splits = exceptions[field] \
        if exceptions and field in exceptions \
        else re.split(sep, field)
    if len(splits) != len(output_names):
        logging.warn('Wrong length ({})'.format(field))
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


def drop_fields(data, fields):
    return {k: v for k, v in data.items() if k not in fields}


def extract_and_leave_ref(data, fields_to_extract, field_name, key_field, reference_data):
    fields = {k: data.pop(k, None) for k in fields_to_extract}
    ref = fields.get(key_field, None)
    if ref:
        reference_data.append(fields)
        data.update({field_name: ref})
    return data


def extract_and_take_ref(data, fields_to_extract, key_field, reference_data):
    fields = {k: data.pop(k, None) for k in fields_to_extract}
    ref = data.get(key_field, None)
    fields[key_field] = ref
    if ref:
        reference_data.append(fields)
    return data


def rename_fields(data, name_mapper):
    new_fields = clean_row({new_key: data.pop(old_key, None)
                            for old_key, new_key in name_mapper.items() if old_key in data.keys()})
    data.update(new_fields)
    return data
