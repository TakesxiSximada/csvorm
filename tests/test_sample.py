# -*- coding: utf-8 -*-
import os
from unittest import TestCase


class SampleCSVTest(TestCase):
    def test_it(self):
        from csvorm import (
            Model,
            Column,
            Integer,
            Unicode,
            )

        class SampleCSV(Model):
            _encoding_ = 'cp932'
            name = Column(Unicode, aliases=[u'生徒氏名'], export_name=u'生徒氏名')
            japanese = Column(Integer, aliases=[u'国語'], export_name=u'国語')
            mathematics = Column(Integer, aliases=[u'数学'], export_name=u'数学')
            english = Column(Integer, aliases=[u'英語'], export_name=u'英語')
            society = Column(Integer, aliases=[u'社会'], export_name=u'社会')
            science = Column(Integer, aliases=[u'理科'], export_name=u'理科')

        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample.csv')
        sample_csv = SampleCSV()
        sample_csv.load(csv_file_path)
        sample_csv.dump('output.csv')
