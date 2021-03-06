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
    * After cloning, cd into the directory named after the remote repository::

        cd Flask-RESTful-Auth

    * Create the python virtual environment::

        python3 -m venv venv

    * Activate the virtual environment::

        source venv/bin/activate

    * Install all the requirements to run the project::

        pip install -r requirements.txt

    * To run the example::

        python ./examples/00_basic/app.py

2. Windows
    * After cloning, cd into the directory named after the remote repository::

        cd .\Flask-RESTful-Auth\

    * Create the python virtual environment::

        python -m venv venv

    * Activate the virtual environment::

        .\venv\Scripts\Activate.ps1

    * Install all the requirements to run the project::

        pip install -r requirements.txt

    * To run the example::

        python .\examples\00_basic\app.py

API Reference
**************
.. toctree::
  :maxdepth: 2
  :caption: Contents:


Decorators
==========

.. automodule:: flask_restful_auth.restful_auth_decorators
  :members:

Routes
======

.. automodule:: flask_restful_auth.restful_auth_routes
  :members:

Default Config
==============

.. automodule:: flask_restful_auth.default_config
  :members:

Storage Adaptors
================

.. automodule:: flask_restful_auth.storage_adaptors.__init__
  :members:

Server
======

.. automodule:: examples.basic.server
  :members:

Client
======

.. automodule:: examples.basic.client
  :members:

Testing
=======

.. automodule:: tests.testing
  :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
