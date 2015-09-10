# -*- coding: utf-8 -*-
import six

if six.PY3:
    import csv  # noqa
    from io import StringIO  # noqa
else:
    from StringIO import StringIO  # noqa
    import unicodecsv as csv  # noqa
