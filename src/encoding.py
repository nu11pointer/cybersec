import base64
import urllib.parse

def encoder(type, data):
    encoded = ""
    if type == "b64":
        encoded = bytes.decode(base64.b64encode((bytes(data, "utf-8"))))
    elif type == "url":
        encoded = urllib.parse.quote_plus(data, safe=":/?=%")

    return f"```{encoded}```"

def decoder(type, data):
    try:
        if type == "b64":
            decoded = bytes.decode(base64.b64decode(data))
        elif type == "url":
            decoded = urllib.parse.unquote_plus(data)
        
        return f"```{decoded}```"
    except:
        return "Invalid string provided!"