Oozie workflow tools AKA Slippin Jimmy
======================================

|Build Status|

Generating Oozie workflows can be a tedious task, coding XML is not
awesome, so you can generate them from Jinja templates using the
process\_templates.py script.

Installing the module
---------------------

::

    # pip install slippinj


About the dependencies, cx_Oracle is a Python extension module
that enables Slippin Jimmy Scribe access to Oracle Database.
This module is currently built against Oracle Client 11.2, 12.1 and 12.2,
and is required for its operation to install the Oracle Instanclient.
You can see how to install it at:
http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html
or
https://anaconda.org/anaconda/oracle-instantclient
for conda enviroment users.

Running the script
------------------

The arguments not provided and mandatory are asked for during script
execution:

::

    jimmy -h

Running the tests
-----------------

Remember to remove the package before running the tests or the installed
version will be used to run them

::

    $ make test

Components of the module
------------------------

Slippin Jimmy is composed by the above components: \* Scribe: It creates
the documentation and basic configuration from the Source database \*
Valet: It provisions the cluster with the needed software \* Tlacuilo:
It compiles the XML workflows from the YAML configuration \* Anabasii:
It uploads the code to the cluster \* Cooper: Once the code has been
uploaded it run the workflows \* Hersir: Execute compilation, upload and
once is uploaded the code to the cluster run the workflows

.. figure:: http://i.imgur.com/zeLOD2s.jpg?1
   :alt: alt tag

   alt tag

.. |Build Status| image:: https://travis-ci.org/scm-spain/slippin-jimmy.svg?branch=master
   :target: https://travis-ci.org/scm-spain/slippin-jimmy

