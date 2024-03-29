csvorm - ORM for CSV
===============================

This allows to use the CSV as ORM.

.. image:: https://github.com/TakesxiSximada/csvorm/actions/workflows/test.yml/badge.svg
    :target: https://github.com/TakesxiSximada/csvorm/actions/workflows/test.yml

INSTALL
-----------------

::

    pip install csvorm

HOW TO USE IT
-----------------------

layout define::

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

creating csv::

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


parse csv::

    test_csv = TestCSV()
    test_csv.load('test.csv')

export data::

    id_,name,modified_at
    1,first,2014-03-26-15-05-50
    2,second,2014-03-26-15-05-50


CONTRIBUTORS
------------

Thank you for `contributors <https://github.com/TakesxiSximada/csvorm/graphs/contributors>`_.



