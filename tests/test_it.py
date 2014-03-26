#-*- coding: utf-8 -*-
from unittest import TestCase

class UsecaseTest(TestCase):
    def test_it(self):
        import datetime
        from csvorm import Model, Column, Integer, Unicode, DateTime

        class TestCSV(Model):
            _encoding_ = 'cp932'
            id_ = Column(Integer, aliases=[u'ID'])
            name = Column(Unicode, aliases=[u'名前'])
            modified_at = Column(DateTime(), aliases=[u'更新日'])

        test_csv = TestCSV()
        record = test_csv.create()
        record.id_ = 5
        record.name = u'テスト'
        record.modified_at = now = datetime.datetime.now()

        import StringIO as stringio
        fp = stringio.StringIO()
        test_csv.dumpfp(fp)
        fp.seek(0)
        print fp.read()
        fp.seek(0)

        other_csv = TestCSV()
        other_csv.loadfp(fp)
        records = [record for record in other_csv]
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.id_, 5)
        self.assertEqual(record.name, u'テスト')
