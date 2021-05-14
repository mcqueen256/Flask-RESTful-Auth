Flask Restful API and Authentication
*************************************

This is an API that is built to handle protective sharing of resources between user, client and server. This project introduces a middleware that provides developers with fast, configurable initial setup, out of the box security and user management.

Overview on How to run this API
===============================
1. Either install a Python IDE or create a Python virtual environment to install the packages required
2. Install packages required
3. Install curl

Setup Procedure
===============
1. Mac/Linux
    * cd Flask-RESTful-Auth
    * python3 -m venv venv
    * source venv/bin/activate
    * pip install -r requirements.txt
    * To run the example
        - python ./examples/00_basic/app.py
2. Windows
    * cd .\Flask-RESTful-Auth\
    * python -m venv venv
    * .\venv\Scripts\Activate.ps1
    * pip install -r requirements.txt
    * To run the example
        - python .\\examples\\00_basic\\app.py

API Reference
**************
.. toctree::
  :maxdepth: 2
  :caption: Contents:

Flask_Restful_Auth
==================
.. automodule:: flask_restful_auth
  :members:

Restful_Auth_decorators
=======================
.. automodule:: flask_restful_auth.restful_auth_decorators
  :members:

Decorators
===========
.. automodule:: flask_restful_auth.decorators
  :members:

Routes
======
.. automodule:: flask_restful_auth.restful_auth_routes
  :members:

Client Manager
==============
.. automodule:: flask_restful_auth.client_manager
  :members:

Default Config
==============
.. automodule:: flask_restful_auth.default_config
  :members:

Server
======
.. automodule:: examples.basic.server
  :members:

Client
======
.. automodule:: examples.basic.client
  :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
