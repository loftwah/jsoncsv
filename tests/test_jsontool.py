# coding=utf-8
# author@alingse
# 2016.08.09
from __future__ import unicode_literals

import io
import unittest

from jsoncsv import PY3
from jsoncsv.jsontool import expand, restore
from jsoncsv.jsontool import is_array
from jsoncsv.jsontool import convert_json


class TestJSONTool(unittest.TestCase):

    def test_string(self):
        s = "sss"
        exp = expand(s)
        _s = restore(exp)
        self.assertEqual(s, _s)

    def test_list(self):
        s = ["sss", "ttt", 1, 2, ["3"]]
        exp = expand(s)
        _s = restore(exp)

        self.assertListEqual(s, _s)

    def test_dict(self):
        s = {
            "s": 1,
            "w": 5,
            "t": {
                "m": 0,
                "x": {
                    "y": "z"
                },
            },
        }

        exp = expand(s)
        _s = restore(exp)

        self.assertDictEqual(s, _s)

    def test_complex(self):
        s = [
            {"s": 0},
            {"t": ["2", {"x": "z"}]},
            0,
            "w",
            ["x", "g", 1]
        ]
        exp = expand(s)
        _s = restore(exp)

        self.assertDictEqual(s[0], _s[0])
        self.assertDictEqual(s[1], _s[1])

        self.assertEqual(s[2], _s[2])
        self.assertEqual(s[3], _s[3])

        self.assertListEqual(s[4], _s[4])

    def test_is_array(self):
        assert is_array([0, 1, 2, 3])
        assert is_array(['0', '1', '2', '3'])
        assert not is_array([1, 2, 3])
        assert not is_array(['0', 1, 2])

    def test_unicode(self):
        data = [
            {u"河流名字": u"长江", u"河流长度": u"6000千米"},
            {u"河流名字": u"黄河", u"河流长度": u"5000千米"}
        ]

        expobj = expand(data)
        assert expobj

    def test_expand_with_safe(self):
        data = {
            "www.a.com": {"qps": 100, "p95": 20},
            "api.a.com": {"qps": 100, "p95": 20, "p99": 100},
        }
        expobj = expand(data, safe=True)
        self.assertEqual(expobj['api.a.com\\.p95'], 20)
        self.assertEqual(expobj['api.a.com\\.p99'], 100)

        origin = restore(expobj, safe=True)
        self.assertEqual(origin, data)


class TestConvertJSON(unittest.TestCase):

    def test_convert_expand(self):
        fin = io.StringIO('{"a":{"b":3}}\n{"a":{"c":4}}\n')
        if PY3:
            fout = io.StringIO()
        else:
            fout = io.BytesIO()

        convert_json(fin, fout, expand)

        self.assertEqual('{"a.b": 3}\n{"a.c": 4}\n', fout.getvalue())

        fin.close()
        fout.close()

    def test_convert_restore(self):
        fin = io.StringIO('{"a.b": 3}\n{"a.c": 4}\n')
        if PY3:
            fout = io.StringIO()
        else:
            fout = io.BytesIO()

        convert_json(fin, fout, restore)

        self.assertEqual('{"a": {"b": 3}}\n{"a": {"c": 4}}\n', fout.getvalue())

        fin.close()
        fout.close()
