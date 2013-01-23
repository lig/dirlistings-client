from html.parser import HTMLParser

from .entries import Entry


class ListingsParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._entries = {}
        self.entries = {}
        self.is_significant = True
        self.row_num = 0
        self.col_num = 0
        self.put_data_to_attr = None

    def handle_starttag(self, tag, attrs):

        if tag == 'th':
            self.is_significant = False
        elif tag == 'img' and ('src', '/icons/back.gif') in attrs:
            self.is_significant = False

        if self.is_significant:

            if tag == 'img' and self.col_num == 0:
                self._entries[self.row_num] = Entry(type_=dict(attrs)['alt'])
            elif tag == 'a' and self.col_num == 1:
                name = dict(attrs)['href']
                self._entries[self.row_num].name = dict(attrs)['href']
                self.entries[name] = self._entries[self.row_num]
            elif tag == 'td' and self.col_num == 2:
                self.put_data_to_attr = 'last_modified'

    def handle_data(self, data):

        if self.put_data_to_attr:
            setattr(self._entries[self.row_num], self.put_data_to_attr, data)
            self.put_data_to_attr = None

    def handle_endtag(self, tag):

        if tag == 'tr':

            if self.is_significant:
                self.row_num += 1

            self.col_num = 0
            self.is_significant = True
        elif tag == 'td':
            self.col_num += 1


def parse(data, ParserClass=ListingsParser):
    parser = ParserClass()
    parser.feed(data)
    return parser.entries
