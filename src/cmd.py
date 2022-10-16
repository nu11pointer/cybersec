import random
import requests
from discord import ActionRow, Button, ButtonStyle
from src.version import __version__

def hello(name):
    name = name.mention
    messages = [
        f"Hello {name}!",
        f"Well, hello there, general {name}!",
        f"Oh hi there, {name}!",
        f"HEY! Look who's here! It's {name}!",
        f"HI {name}, I missed you so much!",
        f"Oh... you again, {name}...",
        f"Wassuppp {name}!",
        f"Well well well, look who decided to say hi... It's {name}.",
        f"Greetings, {name}.",
        f"Still here {name}...?",
        f"Long time no see, {name}!"
    ]
    return random.choice(messages)

def whoami(name):
    return f"`{name}`"

def ping(latency):
    lat = f"{latency*1000:,.0f}ms"
    response = f"""
```sh
Pinging cyber.sec [11.3.333.77] with 32 bytes of data:
Reply from 11.3.333.77: bytes=32 time={lat} TTL=113
Reply from 11.3.333.77: bytes=32 time={lat} TTL=113
Reply from 11.3.333.77: bytes=32 time={lat} TTL=113
Reply from 11.3.333.77: bytes=32 time={lat} TTL=113

Ping statistics for 11.3.333.77:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = {lat}, Maximum = {lat}, Average = {lat}

Latency: {lat}
```"""

    return response

def id(name, author):
    return f"```sh\nuid=1337({name}) gid=7331 groups=0(root),101(h4x0r),133(pwn),1234({author})```"

def exploit(keywords):
    link = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/files_exploits.csv"
    req = requests.get(link)
    data = req.text.split("\n")
    keywordsplit = keywords.split(" ")
    rows = []

    for row in data:
        splited = row.split(",")
        found = {}
        for word in keywordsplit:
            found[word] = False
            if (len(splited) == 8 and word.lower() in splited[2].lower()):
                found[word] = True
        
        if (False not in found.values()):
            rows.append(splited)
    
    if (rows):
        ret = f"""**Query:** `{keywords}`

```
ID        TYPE          EXPLOIT
|--------|-------------|-------------------------------------------"""
        for row in rows:
            id = __formatout__("ID", row[0])
            type = __formatout__("TYPE", row[5])
            ret += f"""
{id}{type}{row[2]}"""
        
        ret += """```"""

        if (len(ret) > 2000 - 36 - len(keywords)):
            ret = "Query too vague."
        else:
            keywords = keywords.replace(" ", "+")
            components = ActionRow(
                Button(label="Results", style=ButtonStyle.blurple, emoji="🔗", url=f"https://www.exploit-db.com/search?q={keywords}"),
            )
            return ret, components
    else:
        ret = "No results returned."

    ret = "Could not perform query."
    
    return ret

__help__ = f"""
```
Command     Description
------      -------
cve         get details from a CVE
decode      decode a given string
encode      encode a given string
hello       be nice and greet me
help        shows this page
id          why not?
ping        check the bot latency
exploit     search for exploits
vt          search for a given hash on VirusTotal
whoami      who am I?
writeup     search for CTFtime writeups

Command     Arguments
------      ------
cve         <CVE>
decode      <b64|url> <text>
encode      <b64|url> <text>
exploit     <keyword> [<keyword> ...]
vt          <hash>
writeup     <keyword> [<keyword> ...]
```
`v{__version__}`
"""

__helpadmin__ = f"""
```
Command     Description
------      -------
cve         get details from a CVE
decode      decode a given string
encode      encode a given string
env         display the API keys
hello       be nice and greet me
help        shows this page
id          why not?
ping        check the bot latency
exploit     search for exploits
set         modify API keys or bot prefix
vt          search for a given hash on VirusTotal
whoami      who am I?
writeup     search for CTFtime writeups

Command     Arguments
------      ------
cve         <CVE>
decode      <b64|url> <text>
encode      <b64|url> <text>
exploit     <keyword> [<keyword> ...]
set         <prefix|API Variable> <value>
vt          <hash>
writeup     <keyword> [<keyword> ...]

API Variables
------
GOOGLE_API_KEY
MALSHARE_API_KEY
NVD_API_KEY
VIRUSTOTAL_API_KEY
```
`v{__version__}`
"""

def __formatout__(type, content):
    final = ""
    spaces = ""
    length = len(content)

    if (type == "ID"):
        spaces = " " * (10 - length)
    elif (type == "TYPE"):
        spaces = " " * (14 - length)

    final = content + spaces

    return final