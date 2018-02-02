"""
>>> lg = lua.globals()
>>> lg == lg._G
True
>>> lg._G == lg._G
True
>>> lg._G == lg['_G']
True

>>> lg.foo = 'bar'
>>> lg.foo == u'bar'
True

>>> lg.tmp = []
>>> lg.tmp
[]

>>> lua.execute("x = {1, 2, 3, foo = {4, 5}}")
>>> lg.x[1], lg.x[2], lg.x[3]
(1..., 2..., 3...)
>>> lg.x['foo'][1], lg.x['foo'][2]
(4..., 5...)

>>> lua.require
<built-in function require>

>>> lg.string
<Lua table at 0x...>
>>> lg.string.lower
<Lua function at 0x...>
>>> lg.string.lower("Hello world!") == u'hello world!'
True

>>> d = {}
>>> lg.d = d
>>> lua.execute("d['key'] = 'value'")
>>> d
{...'key': ...'value'}

>>> d2 = lua.eval("d")
>>> d is d2
True
"""


class MyClass(object):
    def __repr__(self): return '<MyClass>'

obj = MyClass()


if __name__ == '__main__':
    import lua
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
