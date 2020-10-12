#!/usr/bin/env python

# pyClearURLs
# Copyright (c) 2020-present Marco Romanelli
# See LICENSE for details.

import logging

from os.path import join, isfile, isdir
from os import mkdir
from urllib.request import urlopen, Request
from urllib.error import URLError
import tempfile
import json

from pyclearurls.utils import get_project_root

logger = logging.getLogger(__name__)

RULES_URL = "https://gitlab.com/KevinRoebert/ClearUrls/raw/master/data/data.min.json"
RULES_DIR = join(get_project_root(), ".pyclearurls")
RULES_FILENAME = "data.min.json"

def get_database():
    # Check if database file exists
    filname = join(RULES_DIR, RULES_FILENAME)
    if isfile(filname):
        logger.info("Database file found at <%s>", filname)
        with open(filname, "rb") as file:
            return json.load(file)

    # Otherwise, download it and store it
    # in a local folder
    logger.info("Downloading database file ...")
    database = None

    try:
        request = Request(RULES_URL, headers={"User-Agent": "Mozilla/5.0"})
        response = urlopen(request).read().decode('utf-8')

        if response:
            database = json.loads(response)

    except URLError as err:
        logger.error("Cannot download ClearUrls rules: %s", err)

    except json.JSONDecodeError as err:
        logger.error("Cannot parse ClearUrls rules: %s", err)

    # Create the local folder to store the file
    if not isdir(RULES_DIR):
        # Create target Directory
        mkdir(RULES_DIR)

    with open(join(RULES_DIR, RULES_FILENAME), 'w') as file:
        json.dump(database, file)

    logger.info("Database file stored to '%s'", join(RULES_DIR, RULES_FILENAME))

    return database

