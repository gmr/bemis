import gzip
import json
import io
import random
import struct
import unittest
import uuid

from bemis import nbt


class DecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.decoder = nbt.Decoder()

    def test_invalid_file_raises(self):
        handle = io.BytesIO()
        handle.write(b'\04\00\00\00')
        handle.seek(0)
        with self.assertRaises(ValueError):
            self.decoder.load(handle)

    def test_decode_end(self):
        self.assertEqual(self.decoder._decode_end(), 0)

    def test_byte_array(self):
        value = uuid.uuid4().hex.encode('utf-8')
        self.decoder._fp = io.BytesIO()
        self.decoder._fp.write(struct.pack('>i', len(value)))
        self.decoder._fp.write(value)
        self.decoder._fp.seek(0)
        self.assertEqual(self.decoder._decode_byte_array(), value)

    def test_int_array(self):
        value = sorted([random.randint(0, 32768) for _ in range(100)])
        self.decoder._fp = io.BytesIO()
        self.decoder._fp.write(struct.pack('>i', len(value)))
        self.decoder._fp.write(struct.pack('>{}i'.format(len(value)), *value))
        self.decoder._fp.seek(0)
        self.assertEqual(self.decoder._decode_int_array(), value)

    def test_long_array(self):
        value = sorted([random.randint(0, 32768) for _ in range(100)])
        self.decoder._fp = io.BytesIO()
        self.decoder._fp.write(struct.pack('>i', len(value)))
        self.decoder._fp.write(struct.pack('>{}q'.format(len(value)), *value))
        self.decoder._fp.seek(0)
        self.assertEqual(self.decoder._decode_long_array(), value)

    def test_level(self):
        with open('tests/data/level.json', 'r') as handle:
            expectation = json.load(handle)
        with gzip.open('tests/data/level.dat', 'rb') as handle:
            name, result = self.decoder.load(handle)
        self.assertIsNone(name)
        self.assertDictEqual(result, expectation)

    def test_user_data(self):
        with open('tests/data/userdata.json', 'r') as handle:
            expectation = json.load(handle)
        with gzip.open('tests/data/userdata.dat', 'rb') as handle:
            name, result = self.decoder.load(handle)
        self.assertIsNone(name)
        self.assertDictEqual(result, expectation)

    def test_villages(self):
        with open('tests/data/villages.json', 'r') as handle:
            expectation = json.load(handle)
        with gzip.open('tests/data/villages.dat', 'rb') as handle:
            name, result = self.decoder.load(handle)
        self.assertIsNone(name)
        self.assertDictEqual(result, expectation)
