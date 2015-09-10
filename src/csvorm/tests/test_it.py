# -*- coding: utf-8 -*-
from unittest import TestCase


class RecordTest(TestCase):
    def test_it(self):
        pass


class TypeTest(TestCase):
    def _target(self):
        from .. import Type_ as klass
        return klass

    def test_it(self):
        type_ = self._target()
        data = 'test'
        self.assertEqual(type_.encode(data), data)
        self.assertEqual(type_.decode(data), data)


class IntegerTypeTest(TestCase):
    def _target(self):
        from .. import Integer as klass
        return klass

    def test_it(self):
        type_ = self._target()
        data = '1'

        decoded_data = type_.decode(data)
        self.assertEqual(decoded_data, int(data))

        encoded_data = type_.encode(decoded_data)
        self.assertEqual(encoded_data, data)


class UnicodeTypeTest(TestCase):
    def _target(self):
        from .. import Unicode as klass
        return klass

    def _make(self, *args, **kwds):
        factory = self._target()
        return factory(*args, **kwds)

    def test_it(self):
        encoding = 'utf8'
        type_ = self._make(encoding)
        data = 'string'

        decoded_data = type_.decode(data)
        self.assertEqual(decoded_data, data)

        encoded_data = type_.encode(decoded_data)
        self.assertEqual(encoded_data, data)


class DateTimeTypeTest(TestCase):
    def _target(self):
        from .. import DateTime as klass
        return klass

    def _make(self, *args, **kwds):
        factory = self._target()
        return factory(*args, **kwds)

    def test_it(self):
        import datetime
        type_ = self._make()
        fmt = '%Y-%m-%d-%H-%M-%S'
        original_now = datetime.datetime.now()
        data = original_now.strftime(fmt)
        now_ = datetime.datetime.strptime(data, fmt)

        decoded_data = type_.decode(data)
        self.assertEqual(decoded_data, now_)

        encoded_data = type_.encode(decoded_data)
        self.assertEqual(encoded_data, data)
