Welcome to the lunatic-python wiki!
[![Build Status](https://travis-ci.org/OddSource/lunatic-python.svg?branch=master)](https://travis-ci.org/OddSource/lunatic-python)

Details
=======

This is a fork of Lunatic Python, which can be found on the 'net at http://labix.org/lunatic-python.

Sadly, Lunatic Python is very much outdated and won't work with either a current Python or Lua.

This is an updated version of lunatic-python that works with Python 2.7, 3.4, 3.5, and 3.6 and Lua 5.1, 5.2, and 5.3.
I tried contacting the original author of Lunatic Python, but got no response.

Installing
----------
### On Ubuntu

To install, you will need to have the Python and Lua development libraries on your system. If you
do, use the recommended methods (``pip``, ``easy-install``, etc) to install lunatic-python.

This version has been modified to compile under Ubuntu. I haven't tested it under other
distributions, your mileage may vary.
Something similar to:
```bash
sudo apt-get install build-essential liblua5.2-0 liblua5.2-0-dbg liblua5.2-dev lua5.2 lua-cjson python3-dev python3 python3-pip
pip3 install pipenv
pipenv install lunatic-python-universal
```

### On OS X High Sierra

in shell:
```bash 
brew install openssl libmemcached pkg-config libffi pyenv pipenv lua
```

in ~/.bash_profile:
```bash
if hash pyenv 2>/dev/null; then
    eval "$(pyenv init -)"
    export PIPENV_PYTHON=$(pyenv root)/shims/python
fi
```

in a new shell
```bash
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.5.5 # we need enable shared for this library not to segfault on import
pyenv global 3.5.5
pip install --upgrade pip
export PKG_CONFIG_PATH=~/.pyenv/versions/3.5.5/lib/pkgconfig # install direnv to auto-reset this when you get into this directory
pip install pipenv
pipenv install lunatic-python-universal
```

Try it out
----------
```bash
pipenv shell
python
```
```python
import lua
lg = lua.globals()
lua.execute("x = {1, 2, 3, foo = {4, 5}}")
lg.x[1], lg.x[2], lg.x[3], lg.x['foo'][1], lg.x['foo'][2]
```