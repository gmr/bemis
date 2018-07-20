"""
Tests for the NBT Decoder

"""
import gzip
import json
import io
import random
import struct
import unittest
import uuid

from bemis import nbt


class DecoderTestCase(unittest.TestCase):

    def test_invalid_file_raises(self):
        handle = io.BytesIO()
        handle.write(b'\04\00\00\00')
        handle.seek(0)
        with self.assertRaises(ValueError):
            nbt.load(handle)

    def test_decode_end(self):
        self.assertEqual(nbt._decode_end(None), 0)

    def test_byte_array(self):
        value = uuid.uuid4().hex.encode('utf-8')
        fp = io.BytesIO()
        fp.write(struct.pack('>i', len(value)))
        fp.write(value)
        fp.seek(0)
        self.assertEqual(nbt._decode_byte_array(fp), value)

    def test_int_array(self):
        value = sorted([random.randint(0, 32768) for _ in range(100)])
        fp = io.BytesIO()
        fp.write(struct.pack('>i', len(value)))
        fp.write(struct.pack('>{}i'.format(len(value)), *value))
        fp.seek(0)
        self.assertEqual(nbt._decode_int_array(fp), value)

    def test_long_array(self):
        value = sorted([random.randint(0, 32768) for _ in range(100)])
        fp = io.BytesIO()
        fp.write(struct.pack('>i', len(value)))
        fp.write(struct.pack('>{}q'.format(len(value)), *value))
        fp.seek(0)
        self.assertEqual(nbt._decode_long_array(fp), value)

    def test_level(self):
        with open('tests/data/level.json', 'r') as handle:
            expectation = json.load(handle)
        with gzip.open('tests/data/level.dat', 'rb') as handle:
            name, result = nbt.load(handle)
        self.assertIsNone(name)
        self.assertDictEqual(result, expectation)

    def test_user_data_and_loads(self):
        with open('tests/data/userdata.json', 'r') as handle:
            expectation = json.load(handle)
        with gzip.open('tests/data/userdata.dat', 'rb') as handle:
            name, result = nbt.loads(handle.read())
        self.assertIsNone(name)
        self.assertDictEqual(result, expectation)

    def test_villages_and_unpackb(self):
        with open('tests/data/villages.json', 'r') as handle:
            expectation = json.load(handle)
        with gzip.open('tests/data/villages.dat', 'rb') as handle:
            name, result = nbt.unpackb(handle.read())
        self.assertIsNone(name)
        self.assertDictEqual(result, expectation)
