import random
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
search      search for CTFtime writeups
vt          search for a given hash on VirusTotal
whoami      who am I?

Command     Arguments
------      ------
cve         <CVE>
decode      <b64|url> <text>
encode      <b64|url> <text>
vt          <hash>
search      <keyword> [<keyword> ...]
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
search      search for CTFtime writeups
set         modify API keys or bot prefix
vt          search for a given hash on VirusTotal
whoami      who am I?

Command     Arguments
------      ------
cve         <CVE>
decode      <b64|url> <text>
encode      <b64|url> <text>
set         <prefix|API Variable> <value>
vt          <hash>
search      <keyword> [<keyword> ...]

API Variables
------
GOOGLE_API_KEY
MALSHARE_API_KEY
NVD_API_KEY
VIRUSTOTAL_API_KEY
```
`v{__version__}`
"""