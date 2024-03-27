'''
Author       : Thinksky5124
Date         : 2024-03-27 19:53:19
LastEditors  : Thinksky5124
LastEditTime : 2024-03-27 20:03:13
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/utils/config.py
'''
import os
import yaml
import datetime

from .logger import get_logger, setup_logger

def get_config(fname, overrides=None, show=True):
    """
    Read config from file
    """
    assert os.path.exists(fname), ('config file({}) is not exist'.format(fname))
    with open(fname, 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)

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