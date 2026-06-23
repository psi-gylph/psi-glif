import importlib.util
import os

def load_unicode_module(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.expanduser(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
