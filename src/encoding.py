import base64
import urllib.parse

def encoder(type:str, data:str):
    try:
        if type == "b64":
            encoded = bytes.decode(base64.b64encode((bytes(data, "utf-8"))))
        elif type == "url":
            encoded = urllib.parse.quote_plus(data, safe=":/?=%")
        elif type == "hex":
            encoded = data.encode("utf-8").hex()
        elif type == "ord":
            encoded = " ".join([str(ord(c)) for c in data])
        elif type == "bin":
            encoded = ''.join(format(ord(i), '08b') for i in data)

        return f"```{encoded}```"
    except:
        return "Invalid string provided!"

def decoder(type:str, data:str):
    try:
        if type == "b64":
            decoded = bytes.decode(base64.b64decode(data))
        elif type == "url":
            decoded = urllib.parse.unquote_plus(data)
        elif (type == "hex"):
            decoded = bytes.fromhex(data).decode("utf-8")
        elif (type == "ord"):
            decoded = "".join([str(chr(int(c))) for c in data.split(" ")])
        elif (type == "bin"):
            decoded = ""
            for i in range(0, len(data), 7):
                temp_data = int(data[i:i + 7])
                decimal_data = int(temp_data, 2)
                decoded += chr(decimal_data)
        
        return f"```{decoded}```"
    except:
        return "Invalid string provided!"