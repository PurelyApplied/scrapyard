#!/usr/bin/env python3

from datetime import datetime
from random import randint
from xml.dom.minidom import parseString as parseXMLString


class Filter:
    # I don't really know if these are used, but they seem important
    id_start = 1490225016100
    id_end = 1490225016500

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
        self.id = randint(Filter.id_start, Filter.id_end)

    def to_xml_block(self):
        s = "\n".join((
            "<entry>",
            "<category term='filter'></category>",
            "<title>Mail Filter</title>",
            "<id>tag:mail.google.com,2008:filter:{}</id>".format(self.id),
            "<updated>{}</updated>".format(datetime.utcnow()),
            "<content></content>"))
        for key, prop in sorted(self.props.items()):
            s += "\n<apps:property name='{}' value='{}'/>".format(key, prop)
        s += "\n</entry>"
        return s


def head(filters):
    return """<?xml version='1.0' encoding='UTF-8'?>
    <feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <title>Mail Filters</title>
    <id>tag:mail.google.com,2008:filters:{}</id>
    <updated>2017-06-27T17:45:14Z</updated>
    <author>
    <name>Patrick S Rhomberg</name>
    <email>prhomberg@pivotal.io</email>
    </author>""".format((f.id for f in filters))


def foot():
    return '</feed>'


def main():
    f = Filter(from_filter="toolsmiths@pivotal.io",
               subject_filter="pipeline",
               label_with="precheckin failure");
    # print()
    megastring = head((f,)) + f.to_xml_block() + foot()
    # print(megastring)
    node = parseXMLString(megastring)
    print(node)
    # print(node.toprettyxml())


if __name__ == "__main__":
    main()
