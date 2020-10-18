#!/usr/bin/env python

# pyClearURLs
# Copyright (c) 2020 pilate
# Copyright (c) 2020-present Marco Romanelli
# See LICENSE for details.

from collections import defaultdict
from urllib.parse import unquote
import re

from .database import download_database

URL_RE = re.compile("\\?.*")
QUERY_RE = re.compile(".*?\\?")
FINAL_RE = re.compile("[^\\/|\\?|&]+=[^\\/|\\?|&]+")

class URLCleaner:
    """This is the main class of the module.
    It compiles the regular expressions found in the rules database and
    provides the method to clean URLs.

    :param database: ClearURLs rules, defaults to None
    :type database: dict

    :raises ValueError: When the database is not provided
    """

    def __init__(self, database=None):
        """Constructor method
        """
        if database is None:
            database = download_database()

        # If we couldn't get the database,
        # abort with error
        if not database:
            raise ValueError("Is not possible to download the database. "\
                "See the logs for more info.")

        self._compile_rules(database)

    def _compile_rules(self, database):
        """Compile the regular expressions found inside the ClearURLs rules.

        :param database: ClearURLs rules
        :type database: str
        """
        self._compiled = defaultdict(lambda: defaultdict(list))

        for _, rules in database.get("providers", {}).items():
            pattern = rules.get("urlPattern", {})

            current = self._compiled[re.compile(pattern)]
            for query_rule in (rules.get("rules", []) + rules.get("referralMarketing", [])):
                rule_re = re.compile("([\\/|\\?]|(&|&amp;))("+query_rule+"=[^\\/|\\?|&]*)")
                current["param_rules"].append(rule_re)

            current["exceptions"] = list(map(re.compile, rules.get("exceptions", [])))
            current["redirections"] = list(map(re.compile, rules.get("redirections", [])))
            current["full_rules"] = list(map(re.compile, rules.get("rawRules", [])))

    def _find_providers(self, url):
        """Finds the providers for the given URL.

        :param url: An URL
        :type url: str
        :return: Returns an iterator of the provider regular expressions that matched the URL
        :rtype: :class:`filter`
        """
        return filter(bool, map(lambda r: r.match(url), self._compiled))

    def _apply_provider(self, url, provider):
        """Apply the provider regular expressions to the URL.

        :param url: An URL
        :type url: str
        :param provider: Provider regular expressions
        :type provider: :class:`re.Match`
        :return: Cleaned URL
        :rtype: str
        """
        domain = URL_RE.sub("", url)
        fields = "?" + QUERY_RE.sub("", url)

        rules = self._compiled[provider.re]
        for exception in rules["exceptions"]:
            if exception.match(url):
                return url

        for redirection in rules["redirections"]:
            redir = redirection.match(url)
            if redir:
                return unquote(redir.group(1))

        for rule in rules["param_rules"]:
            fields = rule.sub("", fields)

        for raw_rule in rules["full_rules"]:
            domain = raw_rule.sub("", domain)

        final_fields = FINAL_RE.findall(fields)
        if len(final_fields):
            return domain + "?" + "&".join(final_fields)

        return domain

    def clean(self, url):
        """Returns a cleaned URL, by removing tracking elements from it.

        :param url: URL to clean
        :type url: str
        :return: Cleaned URL
        :rtype: str
        """
        providers = self._find_providers(url)

        for provider in providers:
            url = self._apply_provider(url, provider)

        return url
