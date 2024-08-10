import requests

def shellcode(query:str):
    url = "http://shell-storm.org/api/?s="
    q = query
    query.replace("*", "")
    query.replace(" ", "*")
    req = requests.get(url + query)
    if (req.status_code == 200):
        if (len(req.text) > 0):
            lines = req.text.split("\n")
            lines.pop(len(lines) - 1)
            ret = f"**Query:** `{q}`"
            ret += f"""

Results:
```
"""
            for line in lines:
                before = ret
                fields = line.split("::::")
                system = fields[1]
                name = fields[2]
                link = fields[4]
                left = system + " - " + name
                send = left + " " * (70 - len(left) if (70 - len(left)) > 0 else 1) + "| " + link + "\n"
                ret += send
                if (len(ret) > 2000):
                    ret = before
                    ret += "...\n"
                    break

            ret += "```"
        else:
            ret = "No results."
    else:
        ret = "Could not perform query! Try again later"

    return ret