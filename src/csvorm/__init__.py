# -*- coding: utf-8 -*-

import datetime
import collections
import six
if six.PY3:
    import io
    import csv
else:
    import StringIO as io
    import unicodecsv as csv

on_memory_io_factory = io.BytesIO if six.PY3 else io.StringIO


class Record(object):
    def __init__(self, model):
        self._name_value = collections.OrderedDict(
            (name, Value(column))
            for name, column in model.get_name_column_pairs()
            )
        self._alias_name = collections.OrderedDict(
            (alias, name)
            for name, column in model.get_name_column_pairs()
            for alias in column.aliases
            )

    def alias_to_name(self, alias_or_name):
        try:
            return self._alias_name[alias_or_name]
        except KeyError:
            return alias_or_name

    def __getattr__(self, name):
        if name in ('_name_value', '_alias_name'):
            return getattr(super(type(self), self), name)
        elif hasattr(self, '_name_value') and name in self._name_value:
            return self._name_value[name].get()
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in ('_name_value', '_alias_name'):
            super(type(self), self).__setattr__(name, value)
        elif hasattr(self, '_name_value'):
            if name in self._name_value:
                self._name_value[name].set(value)
            else:
                msg = self._name_value.keys()
                raise AttributeError('not {} in {}'.format(repr(name), repr(msg)))
        else:
            super(type(self), self).__setattr__(name, value)

    def __getattr__encode(self, name):
        if hasattr(self, '_name_value') and name in self._name_value:
            return self._name_value[name].encode()
        raise AttributeError(name)

    def __setattr__decode(self, name, value):
        if hasattr(self, '_name_value'):
            if name in self._name_value:
                self._name_value[name].decode(value)
            else:
                msg = self._name_value.keys()
                raise AttributeError('not {} in {}'.format(repr(name), repr(msg)))
        else:
            super(type(self), self).__setattr__(name, value)

    def _dump(self, encode=False):
        row = {}
        for name, value in self._name_value.items():
            data = None
            if encode:
                data = self.__getattr__encode(name)
            else:
                data = getattr(self, name)
            name = value.export_name or name
            row[name] = data
        return row

    def _load(self, row, decode=False):
        name_value = {}
        if not hasattr(row, 'items'):  # no dict
            name_value = dict(
                (name_value[name], row[ii])
                for ii, name in enumerate(self._name_value.keys())
                )
        else:
            name_value = row

        for name, value in name_value.items():
            name = self.alias_to_name(name)
            self._name_value[name].decode(value)


class Value(object):
    def __init__(self, column):
        self._column = column
        self._value = None

    def get(self):
        return self._value

    def set(self, value):
        self._value = value

    def encode(self):
        value = self.get()
        type_ = self._column.type_
        return type_.encode(value)

    def decode(self, value):
        type_ = self._column.type_
        value = type_.decode(value)
        self.set(value)

    @property
    def export_name(self):
        return self._column.export_name


class Column(object):
    _column_index_auto_increment = 0

    def __new__(cls, *args, **kwds):
        cls._column_index_auto_increment += 1
        obj = object.__new__(cls)
        obj.__init__(*args, **kwds)
        return obj

    def __init__(self, type_, aliases=[], export_name=None, *args, **kwds):
        self._column_index = self._column_index_auto_increment
        self.type_ = type_
        self.aliases = aliases
        self.export_name = export_name

    def create(self):
        return Value(self)

    def set_encoding_for_unicode_type(self, encoding):
        if self.type_ == Unicode:
            self.type_ = Unicode(encoding)


class ModelAdapter(list):
    def __init__(self, model):
        self._model = model
        self._columns = None
        self._name_column = None

    @property
    def encoding(self):
        return self._model._encoding_

    def get_columns(self):
        return [column for name, column in self.get_name_column_pairs()]

    def get_names(self):
        return [name for name, column in self.get_name_column_pairs()]

    def get_header(self):
        return [column.export_name or name for name, column in self.get_name_column_pairs()]

    def get_name_column_pairs(self):
        model = self._model
        if self._name_column is None:
            name_column = [[name, getattr(model, name)]
                           for name in dir(model)
                           if type(getattr(model, name)) is Column]
            name_column.sort(key=lambda name_column: id(name_column[1]))

            encoding = self._model._encoding_
            for name, column in name_column:
                column.set_encoding_for_unicode_type(encoding)

            self._name_column = name_column
        return self._name_column

    def get_record(self):
        return Record(self)

    def create(self):
        record = self.get_record()
        self.append(record)
        return record

    def dump(self, path):
        with open(path, 'w+b') as fp:
            self.dumpfp(fp)

    def dumpfp(self, fp):
        fp.write(self.dumps())

    def dumps(self):
        fp = io.StringIO()
        encoding = self._model._encoding_
        # header = map(lambda head: head.encode(encoding), self.get_header())
        kwds = {} if six.PY3 else {'encoding': self.encoding}
        header = self.get_header()
        writer = csv.DictWriter(fp, header, **kwds)
        writer.writeheader()

        for record in self:
            row = record._dump()
            row = dict((key, value) for key, value in row.items())
            writer.writerow(row)
        fp.seek(0)
        buf = fp.read()
        buf = buf.encode(self.encoding) if six.PY3 else buf
        return buf

    def load(self, path):
        with open(path, 'rb') as fp:
            self.loadfp(fp)

    def loadfp(self, fp):
        buf = fp.read()
        self.loads(buf)

    def loads(self, msg):
        if six.PY3:
            msg = msg.decode(self.encoding)
        fp = io.StringIO(msg)
        fp.seek(0)
        kwds = {} if six.PY3 else {'encoding': self.encoding}
        reader = csv.DictReader(fp, **kwds)
        records = []
        for row in reader:
            row = dict((key, value) for key, value in row.items())
            record = self.get_record()
            record._load(row)
            records.append(record)
        self.extend(records)


class Model(object):
    def __new__(cls, *args, **kwds):
        self = super(Model, cls).__new__(cls, *args, **kwds)
        return ModelAdapter(self)


class Type_(object):
    @staticmethod
    def encode(value):
        return value

    @staticmethod
    def decode(value):
        return value


class Integer(Type_):
    @staticmethod
    def encode(value):
        return str(value)

    @staticmethod
    def decode(value):
        return int(value)


class Unicode(Type_):
    def __init__(self, encoding):
        self._encoding = encoding

    def encode(self, value):
        return value

    def decode(self, value):
        return value


class DateTime(Type_):
    _fmt = '%Y-%m-%d-%H-%M-%S'

    def __init__(self, fmt=None):
        self._fmt = fmt if fmt else self._fmt

    def encode(self, value):
        return datetime.datetime.strftime(value, self._fmt)

    def decode(self, value):
        return datetime.datetime.strptime(value, self._fmt)
