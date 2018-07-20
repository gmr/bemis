"""
NBT Reader
==========

"""
import io
import struct


def load(fp):
    """Load a NBT data structure from a file object, returning a tuple
    of name, and a dict containing the NBT content.

    :param fp: A binary file object to load the NBT data from
    :type fp: A binary `file object`
    :raises: ValueError

    """
    tag_type = ord(fp.read(1))
    if tag_type != 10:
        raise ValueError('Invalid NBT file format: expected compound tag,'
                         ' not {}'.format(tag_type))
    return _decode_string(fp), _decode_compound(fp)


def unpackb(value):
    """Load a NBT data structure from bytes, returning a tuple
    of name, and a dict containing the NBT content.

    :param bytes value: The NBT data value to decode
    :raises: ValueError

    """
    return load(io.BytesIO(value))


def loads(value):
    """Load a NBT data structure from bytes, returning a tuple
    of name, and a dict containing the NBT content.

    Compatibility alias for use like `json` and `pickle`.

    :param bytes value: The NBT data value to decode
    :raises: ValueError

    """
    return unpackb(value)


def _decode_end(_fp):
    """Decode the end tag, which has no data in the file, returning 0.

    :type _fp: A binary `file object`
    :rtype: int

    """
    return 0


def _decode_byte(fp):
    """Decode a byte tag

    :type fp: A binary `file object`
    :rtype: byte

    """
    return struct.unpack('b', fp.read(1))[0]


def _decode_short(fp):
    """Decode a short integer tag

    :type fp: A binary `file object`
    :rtype: int

    """
    return struct.unpack('>h', fp.read(2))[0]


def _decode_int(fp):
    """Decode an int tag

    :type fp: A binary `file object`
    :rtype: int

    """
    return struct.unpack('>i', fp.read(4))[0]


def _decode_long(fp):
    """Decode a long integer tag

    :type fp: A binary `file object`
    :rtype: int

    """
    return struct.unpack('>q', fp.read(8))[0]


def _decode_float(fp):
    """Decode a float tag

    :type fp: A binary `file object`
    :rtype: float

    """
    return struct.unpack('>f', fp.read(4))[0]


def _decode_double(fp):
    """Decode a double tag

    :type fp: A binary `file object`
    :rtype: float

    """
    return struct.unpack('>d', fp.read(8))[0]


def _decode_byte_array(fp):
    """Decode a byte array tag

    :type fp: A binary `file object`
    :rtype: bytes

    """
    return fp.read(_decode_int(fp))


def _decode_string(fp):
    """Decode a string tag

    :type fp: A binary `file object`
    :rtype: str or None

    """
    return fp.read(_decode_short(fp)).decode('utf-8') or None


def _decode_list(fp):
    """Decode a list tag

    :type fp: A binary `file object`
    :rtype: list

    """
    tag_id = _decode_byte(fp)
    size = _decode_int(fp)
    return [_MAP[tag_id](fp) for _ in range(size)]


def _decode_compound(fp):
    """Decode a compound tag

    :type fp: A binary `file object`
    :rtype: dict

    """
    values = {}
    tag_type = ord(fp.read(1))
    while tag_type > 0:
        name = _decode_string(fp)
        values[name] = _MAP[tag_type](fp)
        tag_type = ord(fp.read(1))
    return values


def _decode_int_array(fp):
    """Decode an integer array tag

    :type fp: A binary `file object`
    :rtype: list[int]

    """
    size = _decode_int(fp)
    return list(struct.unpack('>{}i'.format(size), fp.read(size * 4)))


def _decode_long_array(fp):
    """Decode an long array tag

    :type fp: A binary `file object`
    :rtype: list[int]

    """
    size = _decode_int(fp)
    return list(struct.unpack('>{}q'.format(size), fp.read(size * 8)))


_MAP = {
    0: _decode_end,
    1: _decode_byte,
    2: _decode_short,
    3: _decode_int,
    4: _decode_long,
    5: _decode_float,
    6: _decode_double,
    7: _decode_byte_array,
    8: _decode_string,
    9: _decode_list,
    10: _decode_compound,
    11: _decode_int_array,
    12: _decode_long_array
}
