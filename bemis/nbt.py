"""
NBT Reader
==========

"""
import struct


class Decoder:
    """Decode a NBT structure from the file object"""

    def __init__(self):
        """Initialize the decoding map"""
        self._fp = None
        self._map = {
            0: self._decode_end,
            1: self._decode_byte,
            2: self._decode_short,
            3: self._decode_int,
            4: self._decode_long,
            5: self._decode_float,
            6: self._decode_double,
            7: self._decode_byte_array,
            8: self._decode_string,
            9: self._decode_list,
            10: self._decode_compound,
            11: self._decode_int_array,
            12: self._decode_long_array,
        }

    def load(self, fp):
        """Load a NBT data structure from the file object, returning a tuple
        of name, and a dict containing the NBT content.

        :param fp: A binary file object to load the NBT data from
        :type fp: A binary `file object`
        :raises: ValueError

        """
        self._fp = fp
        tag_type = ord(self._fp.read(1))
        if tag_type != 10:
            raise ValueError('Invalid NBT file format: expected compound tag,'
                             ' not {}'.format(tag_type))
        return self._decode_string(), self._decode_compound()

    def _decode_end(self):
        """Decode the end tag, which has no data in the file, returning 0.

        :rtype: int

        """
        return 0

    def _decode_byte(self):
        """Decode a byte tag

        :rtype: byte

        """
        return struct.unpack('b', self._fp.read(1))[0]

    def _decode_short(self):
        """Decode a short integer tag

        :rtype: int

        """
        return struct.unpack('>h', self._fp.read(2))[0]

    def _decode_int(self):
        """Decode an int tag

        :rtype: int

        """
        return struct.unpack('>i', self._fp.read(4))[0]

    def _decode_long(self):
        """Decode a long integer tag

        :rtype: int

        """
        return struct.unpack('>q', self._fp.read(8))[0]

    def _decode_float(self):
        """Decode a float tag

        :rtype: float

        """
        return struct.unpack('>f', self._fp.read(4))[0]

    def _decode_double(self):
        """Decode a double tag

        :rtype: float

        """
        return struct.unpack('>d', self._fp.read(8))[0]

    def _decode_byte_array(self):
        """Decode a byte array tag

        :rtype: bytes

        """
        return self._fp.read(self._decode_int())

    def _decode_string(self):
        """Decode a string tag

        :rtype: str or None

        """
        return self._fp.read(self._decode_short()).decode('utf-8') or None

    def _decode_list(self):
        """Decode a list tag

        :rtype: list

        """
        tag_id = self._decode_byte()
        length = self._decode_int()
        return [self._map[tag_id]() for _ in range(length)]

    def _decode_compound(self):
        """Decode a compound tag

        :rtype: dict

        """
        values = {}
        tag_type = ord(self._fp.read(1))
        while tag_type > 0:
            name = self._decode_string()
            values[name] = self._map[tag_type]()
            tag_type = ord(self._fp.read(1))
        return values

    def _decode_int_array(self):
        """Decode an integer array tag

        :rtype: list[int]

        """
        length = self._decode_int()
        return list(
            struct.unpack('>{}i'.format(length), self._fp.read(length * 4)))

    def _decode_long_array(self):
        """Decode an long array tag

        :rtype: list[int]

        """
        length = self._decode_int()
        return list(
            struct.unpack('>{}q'.format(length), self._fp.read(length * 8)))
