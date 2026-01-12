import importlib
m = importlib.import_module('backend.config')
print('ATTRS:', sorted([n for n in dir(m) if not n.startswith('_')]))
print('HAS Config:', 'Config' in dir(m))
print('HAS config:', 'config' in dir(m))
print('Config value repr:', repr(getattr(m, 'Config', None)))
print('module repr:', repr(m))