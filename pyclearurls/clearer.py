from collections import defaultdict
from urllib.parse import unquote
import re

URL_RE = re.compile("\\?.*")
QUERY_RE = re.compile(".*?\\?")
FINAL_RE = re.compile("[^\\/|\\?|&]+=[^\\/|\\?|&]+")

class URLCleaner(object):

    def __init__(self, database):
        self.compile_rules(database)

    def compile_rules(self, database):
        self.compiled = defaultdict(lambda: defaultdict(list))

        for _, rules in database.get("providers", {}).items():
            pattern = rules.get("urlPattern", {})

            current = self.compiled[re.compile(pattern)]
            for query_rule in (rules.get("rules", []) + rules.get("referralMarketing", [])):
                rule_re = re.compile("([\\/|\\?]|(&|&amp;))("+query_rule+"=[^\\/|\\?|&]*)")
                current["param_rules"].append(rule_re)

            current["exceptions"] = list(map(re.compile, rules.get("exceptions", [])))
            current["redirections"] = list(map(re.compile, rules.get("redirections", [])))
            current["full_rules"] = list(map(re.compile, rules.get("rawRules", [])))

    def find_providers(self, url):
        return filter(bool, map(lambda r: r.match(url), self.compiled))

    def apply_provider(self, url, provider):
        domain = URL_RE.sub("", url)
        fields = "?" + QUERY_RE.sub("", url)

        rules = self.compiled[provider.re]
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
        providers = self.find_providers(url)
        for provider in providers:
            url = self.apply_provider(url, provider)

        return url
