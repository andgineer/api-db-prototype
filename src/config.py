"""
    Config loder.

    There is could be nested sections.
    Values can include environment vars like `$PATH` or `${PATH}`

    All params from config set as attributes to the resulting object.
    Nested level separated in attributes names by '_'.

    If obj param is present it should be Python3-style object and not internal types like dict.
    This is necessary to add new attributes to the object.

    >>> load({'section': {'var': 'value'}}).section_var
    'value'

    >>> class Config:
    ...     pass
    >>> conf = Config()
    >>> _ = load({'var': 'value'}, conf)  # doctest: +ELLIPSIS
    >>> conf.var
    'value'
"""
import collections
import os.path
import yaml


def load(config:dict, obj: object=None, _prefix=None):
    """
    Loads config from dict.

    :param _prefix: internal usage for recursion
    """
    if obj is None:
        class Config:
            pass
        obj = Config()
    assert hasattr(obj, '__dict__') or isinstance(obj, object), \
        'obj should be Python3-style object subclass without __slots__ and not internal types like dict.'
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


def load_yaml(file_name: str, obj: object=None):
    return load(yaml.load(open(file_name, 'r')), obj)

