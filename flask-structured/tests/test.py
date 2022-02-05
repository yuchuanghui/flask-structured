import os
file = os.path.dirname(__file__)
print(type(file))
abs = os.path.abspath(file)
print(abs)
print(__name__)