from shodan import Shodan
import os
import re

def search(query):
    api = Shodan(os.getenv("SHODAN_API_KEY"))
    ip = False
    if (re.match(r"^(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$", query)):
        ip = True
    if (ip):
        print(api.host(query))
    else:
        print(api.search(query))
    return "TODO"