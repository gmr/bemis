Bemis
=====
A work-in-progress, multi-format Minecraft file reader for Python3 (that has
all the time in the world).

.. image:: https://travis-ci.org/gmr/bemis.svg?branch=master
    :target: https://travis-ci.org/gmr/bemis

Example Usage
-------------

.. code:: Python3

    import gzip

    from bemis import nbt

    with gzip.open('player.dat', 'rb') as handle:
        name, data = nbt.load(handle)
