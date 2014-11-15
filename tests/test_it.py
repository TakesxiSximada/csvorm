#-*- coding: utf-8 -*-
from unittest import TestCase

class UsecaseTest(TestCase):
    def test_it(self):
        import datetime
        from csvorm import Model, Column, Integer, Unicode, DateTime, on_memory_io_factory

        class TestCSV(Model):
            _encoding_ = 'cp932'
            id_ = Column(Integer, aliases=[u'ID'])
            name = Column(Unicode, aliases=[u'名前'])
            modified_at = Column(DateTime('%Y-%m-%d %H:%M:%S.%f'), aliases=[u'更新日'])

        test_csv = TestCSV()
        record = test_csv.create()
        record.id_ = 5
        record.name = u'テスト'
        record.modified_at = now = datetime.datetime.now()

        import six
        if six.PY3:
            import io
        else:
            import StringIO as io
        fp = on_memory_io_factory()
        test_csv.dumpfp(fp)
        fp.seek(0)
        print(fp.read())
        fp.seek(0)

        other_csv = TestCSV()
        other_csv.loadfp(fp)
        records = [record for record in other_csv]
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.id_, 5)
        self.assertEqual(record.name, u'テスト')
