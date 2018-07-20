"""
Region File Reader
==================

"""
import io
import struct
import zlib

from bemis import nbt


class Region:
    """The region class provides decoded chunk data for individual region
    files in a Minecraft world.

    :param str filename: The region file to read

    """

    def __init__(self, filename):
        self.filename = filename
        parts = filename.split('.')
        self.location = int(parts[1]) >> 5, int(parts[2]) >> 5
        self.handle = open(filename, 'rb')
        self.locations = struct.unpack('>1024i', self.handle.read(4096))
        self.timestamps = struct.unpack('>1024i', self.handle.read(4096))
        self.decoder = nbt.Decoder()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.handle.close()

    def __iter__(self):
        """Iterate over all of the regions in the file.

        :rtype: chunk

        """
        for chunk in self.chunks():
            yield chunk

    def chunk(self, x, z):
        """Return a chunk at the specified x and z offset

        :rtype: dict
        :raises: ValueError

        """
        index = (x % 32) + (z % 32) * 32
        location = self.locations[index]
        offset = (location >> 8) * 4096
        if offset == 0:
            return None

        chunk = {
            'location': self.location,
            'timestamp': self.timestamps[index],
            'x': x,
            'z': z
        }

        self.handle.seek(offset)
        length, compression = struct.unpack('>iB', self.handle.read(5))
        if compression != 2:
            raise ValueError(
                'Invalid compression value: {}'.format(compression))

        chunk.update(
            self.decoder.load(
                io.BytesIO(zlib.decompress(
                    self.handle.read(length - 1)))).read()[1])
        return chunk

    def chunks(self):
        """Iterator that returns each chunk in a region file.

        :rtype: dict

        """
        for x in range(32):
            for z in range(32):
                if self.locations[x + z * 32] >> 8 != 0:
                    yield self.chunk(x, z)
