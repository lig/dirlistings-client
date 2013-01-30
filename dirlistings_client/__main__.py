import os
import sys
from datetime import datetime
from tempfile import mkdtemp
from urllib.request import urlopen

from .parser import parse

epoch = datetime(1970, 1, 1)


def parse_listing(url, cache=None, last_modified=None, recursive=True):
    # prepare attrs
    cache = cache and os.path.abspath(cache) or mkdtemp()
    last_modified = int(
        ((last_modified or datetime.utcnow()) - epoch).total_seconds())

    # check cache
    cache_dir = os.path.join(
        cache, os.path.join(*url.strip('/').split('/')[2:]))
    cache_filename = os.path.join(cache_dir, 'index.html')

    if (not os.path.isfile(cache_filename)
            or int(os.stat(cache_filename).st_mtime) < last_modified):
        # get listing
        data = urlopen(url).read()

        # update cache
        os.makedirs(cache_dir, exist_ok=True)
        with open(cache_filename, 'wb') as cache_file:
            cache_file.write(data)
        os.utime(cache_filename, (last_modified, last_modified))
    else:
        print('from cache', cache_filename)
        # get cached listing
        with open(cache_filename, 'rb') as cache_file:
            data = cache_file.read()

    # parse data
    entries = parse(data)

    # call dirs recursive
    for entry in entries:
        print(entry)

        if recursive and entry.type_ == 'DIR':
            entry_url = '/'.join((url.strip('/'), entry.name))
            parse_listing(entry_url, cache, entry.last_modified)


parse_listing(*sys.argv[1:])
