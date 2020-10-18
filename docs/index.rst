.. pyClearURLs documentation master file, created by
   sphinx-quickstart on Mon Oct 12 23:10:59 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyClearURLs Documentation
==========================

Python implementation of
`ClearURLs <https://gitlab.com/KevinRoebert/ClearUrls>`_ add-on.

Installation
------------

Clone the repository from GitHub to install the latest
development version:

.. code-block:: console

    $ git clone https://github.com/mromanelli9/pyclearurls
    $ cd pyclearurls
    $ pip install .

Alternatively, install directly from the GitHub repository:

.. code-block:: console

    $ pip install git+https://github.com/mromanelli9/pyclearurls


Example Usage
-------------

.. code-block:: python

    from pyclearurls import URLCleaner

    cleaner = URLCleaner()

    url = "https://www.amazon.com/dp/exampleProduct/ref=sxin_0_pb?__mk_de_DE=dsa"
    print(cleaner.clean(url))


Contents
--------

.. toctree::
   :maxdepth: 2

   api

License
-------

Licensed under the MIT license.
See `LICENSE <https://github.com/mromanelli9/pyclearurls/blob/master/README.md>`_.

Copyright 2020 Marco Romanelli, pilate

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
