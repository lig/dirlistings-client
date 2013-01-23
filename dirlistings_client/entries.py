import locale
from datetime import datetime
from warnings import warn


class Entry:
    dt_format = '%d-%b-%Y %H:%M'
    dt_locale = ('en_US', 'UTF-8')

    def __init__(self, name=None, type_=None, last_modified=None):
        self.name = name
        self.type_ = type_
        self.last_modified = last_modified

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name and name.strip('/')

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, type_):
        self._type = type_ and type_.strip('[]')

    @property
    def last_modified(self):
        return self._last_modified

    @last_modified.setter
    def last_modified(self, last_modified):

        if last_modified:
            user_locale = locale.getlocale(locale.LC_TIME)
            locale.setlocale(locale.LC_TIME, self.dt_locale)

            try:
                self._last_modified = datetime.strptime(
                    last_modified.strip(), self.dt_format)
            except ValueError:
                warn('Cannot parse datetime {} via format "{}"'.format(
                    last_modified, self.dt_format))
                self._last_modified = last_modified

            locale.setlocale(locale.LC_TIME, user_locale)
        else:
            self._last_modified = last_modified
