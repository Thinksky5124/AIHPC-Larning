'''
Author       : Thinksky5124
Date         : 2024-03-27 19:53:19
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 19:06:12
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/utils/config.py
'''
import os
import yaml
import datetime
import json
import os
import os.path as osp
import sys
from ast import literal_eval
from collections.abc import Mapping
from importlib import import_module
from pathlib import PurePath
from typing import Dict, Any
import yaml
import torch
import numpy as np
from .logger import get_logger, setup_logger

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_jsonable(obj):
            return super(JSONEncoder, self).default(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, torch.Tensor):
            return obj.cpu().numpy().tolist()
        else:
            return str(obj)

def is_jsonable(x: Any):
    """To show if a variable is jsonable.

    Args:
        x : a variable.

    Returns:
        bool: True means jsonable, False the opposite.
    """
    try:
        json.dumps(x)
        return True
    except Exception:
        return False


def strify_keys(cfg: Mapping):
    """Convert keys of dict to strings if they are not for json dump.

    Args:
        cfg: dict for strify keys.

    Returns:
        dict of strified keys.
    """

    for key, value in list(cfg.items()):
        value = strify_keys(value) if isinstance(value, Mapping) else value
        if not isinstance(key, (str, int)):
            del cfg[key]
            cfg[str(key)] = value
    return cfg

def _check_and_coerce_cfg_value_type(replacement, original, key, full_key):
    """Check that `replacement`, which is intended to replace `original` is \
    of the right type. The type is correct if it matches exactly or is one of \
    a few cases in which the type can be easily coerced.

    Copied from `yacs <https://github.com/rbgirshick/yacs>`.

    """
    _VALID_TYPES = {tuple, list, str, int, float, bool, type(None)}

    original_type = type(original)
    replacement_type = type(replacement)

    # The types must match (with some exceptions)
    if replacement_type == original_type:
        return replacement

    # If either of them is None, allow type convert to one of the valid types
    if (replacement is None and original_type in _VALID_TYPES) or (
        original is None and replacement_type in _VALID_TYPES
    ):
        return replacement

    # Cast replacement from from_type to to_type if the replacement and
    # original types match from_type and to_type
    def conditional_cast(from_type, to_type):
        if replacement_type == from_type and original_type == to_type:
            return True, to_type(replacement)
        else:
            return False, None

    # Conditionally casts
    # list <-> tuple
    casts = [(tuple, list), (list, tuple)]

    for (from_type, to_type) in casts:
        converted, converted_value = conditional_cast(from_type, to_type)
        if converted:
            return converted_value

    raise ValueError(
        "Type mismatch ({} vs. {}) with values ({} vs. {}) for config "
        "key: {}".format(
            original_type, replacement_type, original, replacement, full_key
        )
    )


def get_config(fname, overrides=None, show=True):
    """
    Read config from file
    """
    assert os.path.exists(fname), ('config file({}) is not exist'.format(fname))
    config = Config.fromfile(fname)

    if "work_dir" not in config:
        config['work_dir'] = "output"

    if os.path.isabs(config['work_dir']):
        os.environ['AIHPC_LOG_DIR'] = os.path.join(config['work_dir'], datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    else:
        os.environ['AIHPC_LOG_DIR'] = os.path.join(os.getcwd(), config['work_dir'], datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    setup_logger(cfg=config['LOGGER_LIST'])
    override_config(config, overrides)
    if show:
        print_config(config)
    return config

def override(dl, ks, v):
    """
    Recursively replace dict of list
    Args:
        dl(dict or list): dict or list to be replaced
        ks(list): list of keys
        v(str): value to be replaced
    """
    logger = get_logger("AIHPC")
    def str2num(v):
        try:
            return eval(v)
        except Exception:
            return v

    assert isinstance(dl, (list, dict)), ("{} should be a list or a dict")
    assert len(ks) > 0, ('lenght of keys should larger than 0')
    if isinstance(dl, list):
        k = str2num(ks[0])
        if len(ks) == 1:
            assert k < len(dl), ('index({}) out of range({})'.format(k, dl))
            dl[k] = str2num(v)
        else:
            override(dl[k], ks[1:], v)
    else:
        if len(ks) == 1:
            #assert ks[0] in dl, ('{} is not exist in {}'.format(ks[0], dl))
            if not ks[0] in dl:
                logger.warning('A new filed ({}) detected!'.format(ks[0], dl))
            dl[ks[0]] = str2num(v)
        else:
            assert ks[0] in dl, (
                '({}) doesn\'t exist in {}, a new dict field is invalid'.format(
                    ks[0], dl))
            override(dl[ks[0]], ks[1:], v)
            
def override_config(config, options=None):
    """
    Recursively override the config
    Args:
        config(dict): dict to be replaced
        options(list): list of pairs(key0.key1.idx.key2=value)
            such as: [
                epochs=20',
                'DATASETPIPLINE.train.transform.1.ResizeImage.resize_short=300'
            ]
    Returns:
        config(dict): replaced config
    """
    if options is not None:
        for opt in options:
            assert isinstance(opt,
                              str), ("option({}) should be a str".format(opt))
            assert "=" in opt, (
                "option({}) should contain a ="
                "to distinguish between key and value".format(opt))
            pair = opt.split('=')
            assert len(pair) == 2, ("there can be only a = in the option")
            key, value = pair
            keys = key.split('.')
            override(config, keys, value)

    return config

def print_config(config):
    """
    visualize configs
    Arguments:
        config: configs
    """
    print_dict(config)

def print_dict(d, delimiter=0):
    """
    Recursively visualize a dict and
    indenting acrrording by the relationship of keys.
    """
    logger = get_logger("AIHPC")
    placeholder = "-" * 60
    for k, v in sorted(d.items()):
        if isinstance(v, dict):
            logger.info("{}{} : ".format(delimiter * " ", k))
            print_dict(v, delimiter + 4)
        elif isinstance(v, list) and len(v) >= 1 and isinstance(v[0], dict):
            logger.info("{}{} : ".format(delimiter * " ", str(k)))
            for value in v:
                print_dict(value, delimiter + 4)
        else:
            logger.info("{}{} : {}".format(delimiter * " ", k, v))
        try:
            if k.isupper():
                logger.info(placeholder)
        except:
            logger.info(placeholder)

class Config(object):
    """A facility for config and config files.

    It supports common file formats as configs: python/json/yaml. The interface
    is the same as a dict object and also allows access config values as
    attributes.
    """

    @staticmethod
    def fromfile(filename):
        if isinstance(filename, PurePath):
            filename = filename.as_posix()
        filename = osp.abspath(osp.expanduser(filename))
        if not osp.isfile(filename):
            raise KeyError("file {} does not exist".format(filename))
        if filename.endswith(".py"):
            module_name = osp.basename(filename)[:-3]
            if "." in module_name:
                raise ValueError("Dots are not allowed in config file path.")
            config_dir = osp.dirname(filename)

            old_module = None
            if module_name in sys.modules:
                old_module = sys.modules.pop(module_name)

            sys.path.insert(0, config_dir)
            mod = import_module(module_name)
            sys.path.pop(0)
            cfg_dict = {
                name: value
                for name, value in mod.__dict__.items()
                if not name.startswith("__")
            }
            # IMPORTANT: pop to avoid `import_module` from cache, to avoid the
            # cfg sharing by multiple processes or functions, which may cause
            # interference and get unexpected result.
            sys.modules.pop(module_name)

            if old_module is not None:
                sys.modules[module_name] = old_module

        elif filename.endswith((".yml", ".yaml")):
            with open(filename, "r") as fid:
                cfg_dict = yaml.load(fid, Loader=yaml.Loader)
        else:
            raise IOError(
                "Only py/yml/yaml type are supported now, "
                f"but found {filename}!"
            )
        return Config(cfg_dict, filename=filename)

    def __init__(self, cfg_dict=None, filename=None, encoding="utf-8"):
        if cfg_dict is None:
            cfg_dict = {}
        elif not isinstance(cfg_dict, dict):
            raise TypeError(
                "cfg_dict must be a dict, but got {}".format(type(cfg_dict))
            )

        super(Config, self).__setattr__("_cfg_dict", cfg_dict)
        super(Config, self).__setattr__("_filename", filename)
        if filename:
            with open(filename, "r", encoding=encoding) as f:
                super(Config, self).__setattr__("_text", f.read())
        else:
            super(Config, self).__setattr__("_text", "")

    def merge_from_list_or_dict(self, cfg_opts, overwrite=False):
        """Merge config (keys, values) in a list or dict into this cfg.

        Examples:
            cfg_opts is a list:
            >>> cfg_opts = [
                                'model.backbone.type', 'ResNet18',
                                'model.backbone.num_classes', 10,
                            ]
            >>> cfg = Config(dict(model=dict(backbone=dict(type='ResNet50'))))
            >>> cfg.merge_from_list_or_dict(cfg_opts)
            >>> cfg_dict = super(Config, self).__getattribute__('_cfg_dict')
            >>> assert cfg_dict == dict(
            ...    model=dict(backbone=dict(type="ResNet18", num_classes=10)))

            cfg_opts is a dict:
            >>> cfg_opts = {'model.backbone.type': "ResNet18",
            ...            'model.backbone.num_classes':10}
            >>> cfg = Config(dict(model=dict(backbone=dict(type='ResNet50'))))
            >>> cfg.merge_from_list_or_dict(cfg_opts)
            >>> cfg_dict = super(Config, self).__getattribute__('_cfg_dict')
            >>> assert cfg_dict == dict(
            ...    model=dict(backbone=dict(type="ResNet18", num_classes=10)))
        Args:
            cfg_opts (list or dict): list or dict of configs to merge from.
            overwrite (bool): Weather to overwrite existing (keys, values).
        """

        if isinstance(cfg_opts, list):
            assert len(cfg_opts) % 2 == 0, (
                "Override list has odd length: "
                f"{cfg_opts}; it must be a list of pairs"
            )
            opts_dict = {}
            for k, v in zip(cfg_opts[0::2], cfg_opts[1::2]):
                opts_dict[k] = v
        elif isinstance(cfg_opts, dict):
            opts_dict = cfg_opts
        else:
            raise ValueError(
                f"cfg_opts should be list or dict, but is {type(cfg_opts)}"
            )

        for full_key, v in opts_dict.items():
            d = self
            key_list = full_key.split(".")
            for subkey in key_list[:-1]:
                d.setdefault(subkey, {})
                d = d[subkey]
            subkey = key_list[-1]
            try:
                value = literal_eval(v)
            except Exception:
                raise ValueError(
                    f"The incoming value of key `{full_key}` should be str, "
                    f"list or tuple, but get {v}"
                )
            if isinstance(value, dict):
                raise ValueError(
                    f"The incoming value of key `{full_key}` should be str, "
                    f"list or tuple, but get a dict."
                )

            if subkey in d:
                if overwrite:
                    value = _check_and_coerce_cfg_value_type(
                        value, d[subkey], subkey, full_key
                    )
                    d[subkey] = value
            else:
                d[subkey] = value

    def dump_json(self, skip_keys=False):
        if skip_keys:
            cfg_dict = self._cfg_dict
        else:
            cfg_dict = strify_keys(self._cfg_dict)
        return json.dumps(
            cfg_dict, cls=JSONEncoder, sort_keys=False, skipkeys=skip_keys
        )

    @property
    def filename(self):
        return self._filename

    @property
    def text(self):
        return self._text

    def __repr__(self):
        return "Config (path: {}): {}".format(
            self.filename, self._cfg_dict.__repr__()
        )

    def __len__(self):
        return len(self._cfg_dict)

    def __getattr__(self, name):
        try:
            return getattr(self._cfg_dict, name)
        except AttributeError as e:
            if isinstance(self._cfg_dict, dict):
                try:
                    return self.__getitem__(name)
                except KeyError:
                    raise AttributeError(name)
            raise e

    def __getitem__(self, name):
        return self._cfg_dict.__getitem__(name)

    def __setattr__(self, name, value):
        self._cfg_dict.__setitem__(name, value)

    def __setitem__(self, name, value):
        self._cfg_dict.__setitem__(name, value)

    def __iter__(self):
        return iter(self._cfg_dict)