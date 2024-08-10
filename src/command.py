import random
from src.version import __version__

def hello(name):
    name = name.mention
    messages = [
        f"Hello {name}!",
        f"Well, hello there, general {name}!",
        f"Oh hi there, {name}!",
        f"HEY! Look who's here! It's {name}!",
        f"HI {name}, I missed you!",
        f"Oh... you again, {name}...",
        f"Wassuppp {name}!",
        f"Well well well, look who decided to say hi... It's {name}.",
        f"Greetings, {name}.",
        f"Still here {name}...?",
        f"Long time no see, {name}!"
    ]
    return random.choice(messages)

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