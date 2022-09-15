import random

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
        f"Well well well, look who decided to say hi... It's {name}",
        f"Greetings, {name}",
        f"Still here {name}...?"
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