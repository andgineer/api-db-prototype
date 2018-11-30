import collections
import os.path


def load(config:dict, obj: object, _prefix=None):
    """
    Loads config from dict.
    There is could be nested dicts.
    Values can include environment vars like `$PATH` or `${PATH}`

    All params from config set as attributes to the obj.
    Nested level separated in attributes names by '_'.

    obj should be Python3-style object and not internal types like dict.
    This is neccessary to add new attributes to the object.

    class O:
        pass
    o = O()
    >>> load({'a': 'b', 'c': {'d': 'e'}}, o)
    o.a == 'b'; o.c_d == 'e'


    :param _prefix: internal usage for recursion
    """
    assert hasattr(obj, '__dict__'), 'obj should be Python3-style object and not internal types like dict.'
    for param in config:
        if _prefix is None:
            param_path = param
        else:
            param_path = '_'.join([_prefix, param])
        if isinstance(config[param], collections.Mapping):
            load(config[param], obj, param_path)
        else:
            setattr(obj, param_path, os.path.expandvars(config[param]))
    return obj


if __name__ == '__main__':
    class O:
        pass
    o = O()
    print(dir(load({'a': 'b${PATH}', 'c': {'d': 'e'}}, o)))
    print(o.a, o.c_d)
