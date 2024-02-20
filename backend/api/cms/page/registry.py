from typing import Union


REGISTRY = {}


def register_page_block(*args, **kwargs):
    def decorator(cls):
        name = kwargs.get("name", camel_to_snake(cls.__name__))
        REGISTRY[name or camel_to_snake()] = cls
        return cls

    if len(args) == 1 and callable(args[0]) and not kwargs:
        return decorator(args[0])

    return decorator


def camel_to_snake(name):
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def get_block_union():
    import importlib
    import glob

    # Import all blocks to register them
    for file_ in glob.glob("api/cms/*/blocks/*.py"):
        module_path = file_.replace("/", ".").replace(".py", "")
        importlib.import_module(module_path)

    return Union[tuple(REGISTRY.values())]


def get_block(block_type):
    matching_type = REGISTRY.get(block_type)
    assert matching_type, f"Block type {block_type} not found in registry"
    return matching_type
