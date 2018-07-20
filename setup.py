import setuptools

from flatdict import __version__

setuptools.setup(
    name='bemis',
    version=__version__,
    description='A multi-format Minecraft file reader for Python3',
    long_description=open('README.rst').read(),
    author='Gavin M. Roy',
    author_email='gavinmroy@gmail.com',
    url='https://github.com/gmr/bemis',
    package_data={'': ['LICENSE', 'README.rst']},
    py_modules=['bemis'],
    license='BSD',
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe=True)
