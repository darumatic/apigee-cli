.. apigee-cli documentation master file, created by
   sphinx-quickstart on Thu Jan  9 15:09:20 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Apigee Management API command-line interface documentation!
==========================================================================

|Upload Python Package badge|

The package can be found here:

* `GitHub`_
* `Python Package Index (PyPI)`_

.. note::
   * Many of the docstrings in the ``apigee.api.*`` modules have been taken
     directly from the `Apigee Product Documentation`_ with a few modifications,
     as many methods have a one-to-one mapping with the Apigee Edge APIs.

.. toctree::
   :maxdepth: 1
   :caption: Getting started

   installation
   quickstart

.. toctree::
   :maxdepth: 1
   :caption: API

   auth
   source/apigee.api
   source/apigee.abstract.api
   source/apigee.parsers

.. toctree::
   :maxdepth: 2
   :caption: Guide

   license
   disclaimer
   help

Indices and tables
==================

.. toctree::
   :maxdepth: 2
   :caption: Indices and tables

* :ref:`modindex`

.. |Upload Python Package badge| image:: https://github.com/mdelotavo/apigee-cli/workflows/Upload%20Python%20Package/badge.svg
    :target: https://github.com/mdelotavo/apigee-cli/actions?query=workflow%3A%22Upload+Python+Package%22
.. _`GitHub`: https://github.com/mdelotavo/apigee-cli
.. _`Python Package Index (PyPI)`: https://pypi.org/project/apigeecli/
.. _`Apigee Product Documentation`: https://apidocs.apigee.com/management/apis
