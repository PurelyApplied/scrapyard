#!/usr/bin/env python3

from datetime import datetime


class Filter:
    # I don't really know if these are used, but they seem important
    id_start = 1490225016100
    id_end = 1490225016500
    current_id = id_start
    property_priority = [
        'label',
        'from',
        'to',
        'subject',
        'shouldArchive',
        'sizeOperator',
        'sizeUnit'
    ]

    def __init__(self, from_filter=None, to_filter=None, subject_filter=None,
                 archive=True, label_with=None):
        self.props = {
            'from': from_filter,
            'to': to_filter,
            'subject': subject_filter,
            'shouldArchive': archive,
            'label': label_with,
            # These appear to be default
            'sizeOperator': 's_sl',
            'sizeUnit': 's_smb',
        }
        self.id = Filter.current_id
        Filter.current_id += 1

    @staticmethod
    def from_props(props):
        f = Filter()
        f.props = props
        return f

    @staticmethod
    def property_sorter(key_value_pair):
        return Filter.property_priority.index(key_value_pair[0])

    def to_xml_block(self, depth=0, indent="    "):
        s = depth * indent + "<entry>\n"
        s += "\n".join((depth+1) * indent + s for s in (
            "<category term='filter'></category>",
            "<title>Mail Filter</title>",
            "<id>tag:mail.google.com,2008:filter:{}</id>".format(self.id),
            "<updated>{}</updated>".format(datetime.utcnow()),
            "<content></content>"))
        for key, prop in sorted(self.props.items(), key=Filter.property_sorter):
            if prop:
                s += "\n{}<apps:property name='{}' value='{}'/>".format((depth + 1) * indent, key, prop)
        s += "\n" + depth * indent + "</entry>"
        return s

    @staticmethod
    def property_and(p1, p2):
        if None in (p1, p2):
            return p1 or p2
        if p1 == p2:
            return p1
        return "{} {}".format(p1, p2)

    @staticmethod
    def property_or(p1, p2):
        if None in (p1, p2):
            return None
        if p1 == p2:
            return p1
        return "{}|{}".format(p1, p2)

    def __or__(self, other):
        new_f = Filter.from_props(self.props)
        for k in self.props.keys():
            p1 = self.props[k]
            p2 = other.props[k]
            new_f.props[k] = self.property_or(p1, p2)
        return new_f

    def __and__(self, other):
        new_f = Filter.from_props(self.props)
        for k in self.props.keys():
            p1 = self.props[k]
            p2 = other.props[k]
            new_f.props[k] = self.property_and(p1, p2)
        return new_f

