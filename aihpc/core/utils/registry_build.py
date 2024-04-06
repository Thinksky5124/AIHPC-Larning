'''
Author       : Thinksky5124
Date         : 2024-03-26 20:50:01
LastEditors  : Thinksky5124
LastEditTime : 2024-03-29 11:09:52
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/utils/registry_build.py
'''

import abc
from threading import RLock
from typing import Callable, List, Tuple, Union, Dict, Any

class Registry(object):
    """
    A generic registry that stores objects by name.

    Parameters
    ----------
    name : str
        The name of the registry.

    Attributes
    ----------
    name : str
        The name of the registry.
    _obj_map : Dict[str, Any]
        A mapping from object names to objects.
    """
    def __init__(self, name) -> None:
        self._name = name
        self._obj_map = {}
    
    @property
    def name(self):
        return self._name
    
    def __contains__(self, key):
        """
        Returns whether an object with the given name is registered.

        Parameters
        ----------
        key : str
            The name of the object.

        Returns
        -------
        bool
            Whether an object with the given name is registered.
        """
        return self._obj_map.get(key) is not None
    
    def _do_register(self, name, obj):
        """
        Registers an object with the given name.

        Parameters
        ----------
        name : str
            The name of the object.
        obj : Any
            The object to register.
        """
        assert (
            name not in self._obj_map
        ), f"An object named '{name}' was already registered in '{self._name}' registry!"
        self._obj_map[name] = obj
    
    def register(self, obj: Callable, name: str = None) -> Callable:
        """
        Registers an object with the given name, or uses the object's name if no name is given.

        Parameters
        ----------
        obj : Any
            The object to register.
        name : str, optional
            The name of the object, by default None.

        Returns
        -------
        Any
            The registered object.
        """
        if obj is None:
            # use as a decorator
            def decorator(obj, name=name):
                if name is None:
                    name = obj.__name__
                self._do_register(name, obj)
                return obj
            
            return decorator
        
        # use as a function call
        if name is None:
            name = obj.__name__
        self._do_register(name, obj)
        return obj
    
    def get(self, name):
        """
        Returns the object registered with the given name, or None if no object is registered with the given name.

        Parameters
        ----------
        name : str
            The name of the object.

        Returns
        -------
        Any
            The registered object, or None if no object is registered with the given name.
        """
        ret = self._obj_map.get(name)
        if ret is None:
            raise KeyError(
                f"No object named '{name}' was registered in '{self._name}' registry!"
            )
        return ret

class BaseBuildFactory(metaclass=abc.ABCMeta):
    """
    Base class for build factories.
    """
    def __init__(self, registry_table: Registry = None) -> None:
        self._registry_table = registry_table
    
    @property
    def registry_table(self) -> Registry:
        return self._registry_table

    @staticmethod
    def get_registry_table(object_type_name: str):
        for registry_table_name, registry_table in ObjectRegister.REGISTRY_MAP.items():
            if object_type_name in registry_table:
                return registry_table
        raise KeyError(f"No registry table found for object type '{object_type_name}'!")
    
    @abc.abstractmethod
    def build(self, *args, **kwargs):
        raise NotImplementedError

class FromArgsBuildFactory(BaseBuildFactory):
    def build_from_args(self, object_type_name: str, *args, **kwargs):
        """
        Build a module from arguments
        """
        if self.registry_table is None:
            self.registry_table = self.get_registry_table(object_type_name)
        
        obj_cls = self.registry_table.get(object_type_name)
        if obj_cls is None:
            raise KeyError(f"{object_type_name} is not registered in the {self.registry_table.name}!")
        
        return obj_cls(*args, **kwargs)
    
    def build(self, object_type_name: str, *args, **kwargs):
        return self.build_from_args(object_type_name, *args, **kwargs)

class FromConfigBuildFactory(BaseBuildFactory):
    def build_from_config(self, key: str = 'type', cfg: Dict = None, *args, **kwargs):
        if cfg is None:
            return None
        assert isinstance(cfg, dict) and key in cfg, f"key name: {key} not in config!"

        cfg_copy = cfg.copy()
        cfg_copy.update(kwargs)
        obj_type = cfg_copy.pop(key)

        if self.registry_table is None:
            self.registry_table = self.get_registry_table(obj_type)
        
        obj_cls = self.registry_table.get(obj_type)
        if obj_cls is None:
            raise KeyError(f"{obj_type} is not registered in the {self.registry_table.name}!")
        return obj_cls(*args, **cfg_copy)
    
    def build(self, cfg: Dict,  *args, key: str = 'type', **kwargs):
        return self.build_from_config(key=key, cfg=cfg, *args, **kwargs)

class ObjectRegister(metaclass=abc.ABCMeta):
    BUILD_METHOD_MAP = dict(
        from_config = FromConfigBuildFactory,
        from_args = FromArgsBuildFactory
    )
    REGISTRY_MAP = dict()
    single_lock = RLock()

    def __init__(self) -> None:
        pass

    # singleton design
    def __new__(cls, registry_name = None, build_method = "from_config", *args, **kwargs):
        if registry_name is None:
            with ObjectRegister.single_lock:
                if not hasattr(ObjectRegister, "_instance"):
                    ObjectRegister._instance = object.__new__(cls)
            
            return ObjectRegister._instance
        else:
            assert build_method in ObjectRegister.BUILD_METHOD_MAP.keys(), f"Unsupported build method: {build_method}!"
            assert registry_name in ObjectRegister.REGISTRY_MAP.keys(), f"Registry name: {registry_name} do not registered in REGISTRY_MAP!"
            if registry_name is None:
                return ObjectRegister.BUILD_METHOD_MAP[build_method]()
            return ObjectRegister.BUILD_METHOD_MAP[build_method](ObjectRegister.REGISTRY_MAP[registry_name])
    
    @staticmethod
    @property
    def registry_keys() -> List[str]:
        return list(ObjectRegister.REGISTRY_MAP.keys())
    
    @staticmethod
    def get_registry_table(registry_name: str) -> List[str]:
        return list(ObjectRegister.REGISTRY_MAP[registry_name].keys())
    
    @staticmethod
    def create_factory(registry_name: str = None, build_method: str = "from_config"):
        assert build_method in ObjectRegister.BUILD_METHOD_MAP.keys(), f"Unsupported build method: {build_method}!"
        assert registry_name in ObjectRegister.REGISTRY_MAP.keys(), f"Registry name: {registry_name} do not registered in REGISTRY_MAP!"
        if registry_name is None:
                return ObjectRegister.BUILD_METHOD_MAP[build_method]()
        return ObjectRegister.BUILD_METHOD_MAP[build_method](ObjectRegister.REGISTRY_MAP[registry_name])
    
    @staticmethod
    def register(registry_name: str):
        """
        Register a class from `registry_name`, can be used as decorate
        .. code-block:: python
            @ObjectRegister.register('backbone')
            class ResNet:
                pass
                
            build_factory_1 = ObjectRegister('backbone')
            abstract_build_factory_2 = ObjectRegister()
            build_factory_2 = abstract_build_factory_2.create_factory('backbone')
            a = build_factory_1.build(...)
            a = build_factory_2.build(...)
        """
        assert isinstance(registry_name, str), "registry_name must be a string!"
        if registry_name not in ObjectRegister.REGISTRY_MAP.keys():
            ObjectRegister.REGISTRY_MAP[registry_name] = Registry(registry_name)
        
        Registry_class: Registry = ObjectRegister.REGISTRY_MAP[registry_name]
        def actually_register(obj: Callable = None, name: str = None):
            return Registry_class.register(obj, name)
        
        return actually_register
    
    @staticmethod
    def register_obj(obj: Callable, registry_name: str, obj_name: str = None):
        assert isinstance(registry_name, str), "registry_name must be a string!"
        if registry_name not in ObjectRegister.REGISTRY_MAP.keys():
            ObjectRegister.REGISTRY_MAP[registry_name] = Registry(registry_name)
        
        Registry_class: Registry = ObjectRegister.REGISTRY_MAP[registry_name]
        return Registry_class.register(obj, obj_name)
    