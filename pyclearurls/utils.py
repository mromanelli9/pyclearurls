#!/usr/bin/env python

# pyClearURLs
# Copyright (c) 2020-present Marco Romanelli
# See LICENSE for details.

from os.path import join, dirname, abspath

def get_project_root():
    """
    Gets project root.
    :return: str (path)
    """
    root_path = dirname(dirname(abspath(__file__)))

    return root_path


