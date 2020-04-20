from collections import defaultdict
from urllib.parse import unquote
import re


URL_RE = re.compile("\\?.*")
QUERY_RE = re.compile(".*?\\?")
FINAL_RE = re.compile("[^\\/|\\?|&]+=[^\\/|\\?|&]+")


class URLCleaner(object):

    def __init__(self, database):
        self.compile_rules(database)
        self.group_to_provider = {}


    def compile_rules(self, database):
        self.compiled = defaultdict(lambda: defaultdict(list))

        for provider, rules in database.get("providers", {}).items():
            pattern = rules["urlPattern"]

            current = self.compiled[re.compile(pattern)]
            for query_rule in (rules["rules"] + rules["referralMarketing"]):
                rule_re = re.compile("([\\/|\\?]|(&|&amp;))("+query_rule+"=[^\\/|\\?|&]*)")
                current["param_rules"].append(rule_re)

            current["exceptions"] = list(map(re.compile, rules["exceptions"]))
            current["redirections"] = list(map(re.compile, rules["redirections"]))
            current["full_rules"] = list(map(re.compile, rules["rawRules"]))


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
            return domain + "?" + "&".join(final_fields);

        return domain


    def clean(self, url):
        providers = self.find_providers(url)
        # print(list(providers))
        for provider in providers:
            url = self.apply_provider(url, provider)

        return url


def test():
    print(c.clean("http://www.amazon.com/gp/navigation/redirector.html/?tag=5"))
    # test rules
    assert c.clean("https://www.amazon.com/?pf_rd_f=5") == "https://www.amazon.com/"
    # test referralMarketing
    assert c.clean("https://www.amazon.com/?tag=5") == "https://www.amazon.com/"
    # test excludes
    assert c.clean("http://www.amazon.com/gp/navigation/redirector.html/?tag=5") == "http://www.amazon.com/gp/navigation/redirector.html/?tag=5"
    # test rawRules
    assert c.clean("https://www.amazon.com/dp/exampleProduct/ref=sxin_0_pb?__mk_de_DE=dsa") == "https://www.amazon.com/dp/exampleProduct"
