# Setup Python

```
cd Flask-RESTful-Auth
python3 -m venv venv
source venv/bin/activate
```

# Constructing Repository for Publishing

First, create another folder with the same name as the repository inside the repository. The `Flask-RESTful-Auth/` directory is at the top level and is the repository. With in that, `flask_restful_auth/` is the library and contains all of the library code. It will be called in python as: `from flask_restful_auth import ...`.

```
Flask-RESTful-Auth/
  |- flask_restful_auth/
```

To create a minimally useful library, add `__init__.py` in `flask_restful_auth/` to make that directory a python module. Then add a `__main__.py` file to make it a top level script that can be called with `python -m flask_restful_auth` (ref: 2).

Contents of `__init__.py`:
```
__version__ = "0.1.0"
test_message = "Hello Flask!"
```

Contents of `__main__.py`:
```
print("TODO: Main example is run here..")
from . import test_message
print(test_message)
```

Now try `python -m flask_restful_auth`.

This library will not need a `__main__.py` as it is a plugin for Flask, but perhaps it can remain to run a main example. (Design Descision)




Refs:

1. [https://realpython.com/pypi-publish-python-package/]
2. [https://docs.python.org/3/library/__main__.html]

