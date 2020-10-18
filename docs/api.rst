.. _api:

.. py:module:: pyclearurls

API Documentation
=================

There's two way to initialise the main :class:`~pyclearurls.URLCleaner` class:

- directly providing the `ClearURLs rules <https://gitlab.com/KevinRoebert/ClearUrls/raw/master/data/data.min.json>`_
  rules by setting the ``database`` paramater:

  .. code-block:: python

    cleaner = URLCleaner(database=my_clearurls_rules)

- let ClearURLs download the latest rules from GitLab and store them in a local file:

  .. code-block:: python

    cleaner = URLCleaner()

The rules file is stored under ``.pyclearurls/data.min.json``
in the directory containing the script that was used to invoke
the Python interpreter.

URLCleaner
-------------

.. autoclass:: URLCleaner
   :members:
   :undoc-members:
