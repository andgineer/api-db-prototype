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
import collections.abc
import os.path

import yaml

last_loaded = None  # contains dict with last loaded params


def load(config: dict, obj: object = None, _prefix=None):
    """
    Loads config from dict.

    :param _prefix: internal usage for recursion
    """
    global last_loaded
    if obj is None:

        class Config:
            pass

        obj = Config()
    if _prefix is None:
        last_loaded = {}
    assert hasattr(obj, "__dict__") or isinstance(
        obj, object
    ), "obj should be Python3-style object subclass without __slots__ and not internal types like dict."
    if not isinstance(config, collections.abc.Mapping):
        raise ValueError(f"Bad config:\n{str(config)[:100]}\n")
    for param in config:
        if _prefix is None:
            param_path = param
        else:
            param_path = "_".join([_prefix, param])
        if isinstance(config[param], collections.abc.Mapping):
            load(config[param], obj, param_path)
        else:
            if isinstance(config[param], str):
                var = os.path.expandvars(config[param])
            else:
                var = config[param]
            last_loaded[param_path] = var
            setattr(obj, param_path, var)
    return obj


def load_yaml(file_name: str, obj: object = None):
    return load(yaml.load(open(file_name, "r")), obj)
