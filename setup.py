#!/usr/bin/python

from distutils.sysconfig import get_python_version
import os
from setuptools import (
    Extension,
    setup,
)
import sys

if sys.version > '3':
    PY3 = True
else:
    PY3 = False

if PY3:
    import subprocess as commands
else:
    import commands


if os.path.isfile('MANIFEST'):
    os.unlink('MANIFEST')

PYTHON_VERSION = get_python_version()


def pkg_config():
    # map pkg-config output to kwargs for distutils.core.Extension
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}

    pc_status = 0
    pc_output = None
    lua_version = None
    combined_pc_output = ''

    for python in ('python-{}'.format(PYTHON_VERSION), 'python{}'.format(PYTHON_VERSION)):
        # Try two possible .pc file names for this version
        pc_status, pc_output = commands.getstatusoutput('pkg-config --libs --cflags {}'.format(python))
        if pc_status == 0:
            combined_pc_output = pc_output
            break
    if pc_status != 0:
        sys.exit(
            'pkg-config failed for `python` (tried `python-{v}` and `python{v}`); most recent output was:\n{o}'.format(
                v=PYTHON_VERSION,
                o=pc_output,
            ),
        )

    commands.getstatusoutput('pkg-config --libs --cflags python-'.format())

    for lua in ('lua5.3', 'lua-5.3', 'lua5.2', 'lua-5.2', 'lua5.1', 'lua-5.1'):
        # Try two different supported versions and two possible .pc file names for each version
        pc_status, pc_output = commands.getstatusoutput('pkg-config --libs --cflags {}'.format(lua))
        if pc_status == 0:
            combined_pc_output += ' ' + pc_output
            lua_version = lua[-3:]
            break
    if pc_status != 0:
        sys.exit(
            'pkg-config failed for `lua` (tried `lua5.3`, `lua-5.3`, `lua5.2`, `lua-5.2`, `lua5.1`, and `lua-5.1`; '
            'most recent output was:\n{}'.format(
                pc_output,
            ),
        )

    kwargs = {}
    for token in combined_pc_output.split():
        if token[:2] in flag_map:
            kwargs.setdefault(flag_map.get(token[:2]), []).append(token[2:])
        else:
            # throw others to extra_link_args
            kwargs.setdefault('extra_link_args', []).append(token)

    if PY3:
        items = kwargs.items()
    else:
        items = kwargs.iteritems()
    for k, v in items:     # remove duplicated
        kwargs[k] = list(set(v))

    return kwargs, lua_version

lua_pkg_config, lua_version_string = pkg_config()

lua_directory_1 = '/usr/include/lua{}'.format(lua_version_string)
lua_directory_2 = '/usr/local/include/lua{}'.format(lua_version_string)
if os.path.isdir(lua_directory_1):
    lua_pkg_config['extra_compile_args'] = ['-I{}'.format(lua_directory_1)]
elif os.path.isdir(lua_directory_2):
    lua_pkg_config['extra_compile_args'] = ['-I{}'.format(lua_directory_2)]
else:
    print('Neither {} nor {} exists; skipping extra compile args.'.format(lua_directory_1, lua_directory_2))
print('pkg-config succeeded; ready to compile extensions.\n{}'.format(lua_pkg_config))

setup(
    name='lunatic-python-universal',
    version='2.0.0',
    author='Gustavo Niemeyer',
    author_email='gustavo@niemeyer.net',
    description='Two-way bridge between Python and Lua',
    long_description="""
Lunatic Python is a two-way bridge between Python and Lua, allowing these languages to intercommunicate. Being two-way
means that it allows Lua inside Python, Python inside Lua, Lua inside Python inside Lua, Python inside Lua inside
Python, and so on. This package is a fork of the original from http://labix.org/lunatic-python, updated to support
Python 3, and forked again from https://github.com/bastibe/lunatic-python to release to PyPi and support newer versions
of Lua and macOS Homebrew-installed Lua.
""",
    url='https://github.com/OddSource/lunatic-python',
    license='LGPLv2',
    ext_modules=[
        Extension('lua-python', ['src/pythoninlua.c', 'src/luainpython.c'], **lua_pkg_config),
        Extension('lua', ['src/pythoninlua.c', 'src/luainpython.c'], **lua_pkg_config),
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
)
