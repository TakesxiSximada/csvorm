#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import datetime
from csvorm import (
    Model,
    Column,
    Integer,
    Unicode,
    DateTime,
    )


class TestCSV(Model):
    _encoding_ = 'cp932'
    id_ = Column(Integer)
    name = Column(Unicode)
    modified_at = Column(DateTime())


def create():
    test_csv = TestCSV()

    record = test_csv.create()
    record.id_ = 1
    record.name = u'first'
    record.modified_at = datetime.datetime.now()

    record = test_csv.create()
    record.id_ = 2
    record.name = u'second'
    record.modified_at = datetime.datetime.now()

    test_csv.dump('test.csv')


def parse():
    test_csv = TestCSV()
    test_csv.load('test.csv')

    for record in test_csv:
        print record.id_, record.name, record.modified_at


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')
    opts = parser.parse_args()

    cmd_func = {'create': create,
                'parse': parse,
                }

    func = cmd_func[opts.cmd]
    func()

if __name__ == '__main__':
    main()
