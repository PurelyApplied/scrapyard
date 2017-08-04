from gmailFilter import Filter


def main():
    f = Filter(from_filter="toolsmiths@pivotal.io",
               subject_filter="pipeline",
               label_with="precheckin failure")
    f2 = Filter(to_filter="geode-dev")
    megastring = "\n".join((
        head((f, f2)),
        f.to_xml_block(1, "    "),
        f2.to_xml_block(1, "    "),
        foot()))
    print(megastring)
    # node = parseXMLString(megastring)
    # print(node)
    # print(node.toprettyxml())


def head(filters):
    return """<?xml version='1.0' encoding='UTF-8'?><feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <title>Mail Filters</title>
    <id>tag:mail.google.com,2008:filters:{}</id>
    <updated>2017-06-27T17:45:14Z</updated>
    <author>
        <name>Patrick S Rhomberg</name>
        <email>prhomberg@pivotal.io</email>
    </author>""".format(",".join((str(f.id) for f in filters)))


def foot():
    return '</feed>'


if __name__ == "__main__":
    main()
