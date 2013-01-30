from html.parser import HTMLParser

from .processor import EntriesIterator


class ListingsParser(HTMLParser):

    def __init__(self, processor=EntriesIterator, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.processor = processor()
        self.is_significant = True
        self.col_num = 0
        self.put_data_to_attr = None

    def handle_starttag(self, tag, attrs):

        if tag == 'th':
            self.is_significant = False
        elif tag == 'img' and ('src', '/icons/back.gif') in attrs:
            self.is_significant = False

        if self.is_significant:

            if tag == 'img' and self.col_num == 0:
                self.processor.handle_entry()
                self.processor.handle_entry_attr('type_', dict(attrs)['alt'])
            elif tag == 'a' and self.col_num == 1:
                self.processor.handle_entry_attr('name', dict(attrs)['href'])
            elif tag == 'td' and self.col_num == 2:
                self.put_data_to_attr = 'last_modified'

    def handle_data(self, data):

        if self.put_data_to_attr:
            self.processor.handle_entry_attr(self.put_data_to_attr, data)
            self.put_data_to_attr = None

    def handle_endtag(self, tag):

        if tag == 'tr':

            if self.is_significant:
                self.processor.handle_entry_end()

            self.col_num = 0
            self.is_significant = True
        elif tag == 'td':
            self.col_num += 1


def parse(data):
    parser = ListingsParser()
    parser.feed(str(data))
    return parser.processor.entries
