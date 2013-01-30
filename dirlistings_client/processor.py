import abc

from .entries import Entry


class ProcessorError(Exception):
    pass


class AbstractProcessor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle_entry(self, **attrs):
        return NotImplemented

    @abc.abstractmethod
    def handle_entry_end(self):
        return NotImplemented

    @abc.abstractmethod
    def handle_entry_attr(self, attr_name, attr_value):
        return NotImplemented


class EntriesIterator(AbstractProcessor):

    def __init__(self):
        self.entries = []
        self.entry = None

    def handle_entry(self, **attrs):
        self.handle_entry_end()
        self.entry = Entry()

        for name, value in attrs.items():
            self.handle_entry_attr(name, value)

    def handle_entry_end(self):

        if self.entry:
            self.entries.append(self.entry)

        self.entry = None

    def handle_entry_attr(self, attr_name, attr_value):

        if self.entry:
            setattr(self.entry, attr_name, attr_value)
        else:
            raise ProcessorError('No entry to set attr on.')
