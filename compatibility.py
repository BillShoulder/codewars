""" Compatibility """

try:
    # Python 3.8+
    from functools import cached_property
except ImportError:
    # Previously
    class cached_property(object):
        """ https://stackoverflow.com/a/4037979 """
        def __init__(self, factory):
            self._attr_name = factory.__name__
            self._factory = factory

        def __get__(self, instance, owner):
            attr = self._factory(instance)
            setattr(instance, self._attr_name, attr)
            return attr