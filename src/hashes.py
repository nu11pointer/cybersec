import requests
import hashid

ALGS = [
    "auto",
    "md5",
    "md5-sha1",
    "md5WithRSAEncryption",
    "RSA-MD5",
    "RSA-RIPEMD160",
    "RSA-SHA1",
    "RSA-SHA1-2",
    "RSA-SHA224",
    "RSA-SHA256",
    "RSA-SHA3-224",
    "RSA-SHA3-256",
    "RSA-SHA3-384",
    "RSA-SHA3-512",
    "RSA-SHA384",
    "RSA-SHA512",
    "RSA-SHA512/224",
    "RSA-SHA512/256",
    "RSA-SM3",
    "blake2b512",
    "blake2s256",
    "id-rsassa-pkcs1-v1_5-with-sha3-224",
    "id-rsassa-pkcs1-v1_5-with-sha3-256",
    "id-rsassa-pkcs1-v1_5-with-sha3-384",
    "id-rsassa-pkcs1-v1_5-with-sha3-512",
    "ripemd",
    "ripemd160",
    "ripemd160WithRSA",
    "rmd160",
    "sha1",
    "sha1WithRSAEncryption",
    "sha224",
    "sha224WithRSAEncryption",
    "sha256",
    "sha256WithRSAEncryption",
    "sha3-224",
    "sha3-256",
    "sha3-384",
    "sha3-512",
    "sha384",
    "sha384WithRSAEncryption",
    "sha512",
    "sha512-224",
    "sha512-224WithRSAEncryption",
    "sha512-256",
    "sha512-256WithRSAEncryption",
    "sha512WithRSAEncryption",
    "shake128",
    "shake256",
    "sm3",
    "sm3WithRSAEncryption",
    "ssl3-md5",
    "ssl3-sha1"
]

def crack(hash:str, alg:str):
    global ALGS
    url = "https://api.hash-decrypt.io/v1/hash/"
    ret = ""
    found = False

    for a in ALGS:
        if (alg.lower() == a.lower()):
            found = True
            if (alg.lower() == "auto"):
                guess = hash_id(hash)
                if (guess == "No results returned."):
                    ret = f"Could not identify hash algorithm."
                    break
                else:
                    guess = guess.split("\n")[7].split(" ")[0]
                # convert algorithms from hashid to hash-decrypt
                a = __convert__(guess)
                if (a is None):
                    ret = f"Could not identify hash algorithm."
                    break
            fullurl = url + a + "/" + hash
            req = requests.get(fullurl)
            if (req.status_code == 404 or req.status_code == 429):
                ret = "API is currently offline or you made too many requests to the API! Please wait a few minutes and try again."
            else:
                data = req.json()
                if (data["found"] is True):
                    if (data["password"] == ""):
                        ret = f"""
**Hash:** `{hash}` **({a})**

✅ **Cracked!**"""
                    else:
                        ret = f"""
**Hash:** `{hash}` **({a})**

✅ **Cracked!**

`{data["password"]}`"""
                    
                else:
                    ret = f"**Hash:** `{hash}` **({a})**\n\n❌ **Not Cracked!**"
            break
    if (not found):
        ret = "Invalid algorithm specified!"
    return ret

def hash_id(hash):
    id = hashid.HashID()
    guess = id.identifyHash(hash)
    res = {"names":[], "hashcat":[], "john":[]}
    ret = ""
    c = 0
    try:
        for g in guess:
            res["names"].append(g.name)
            res["hashcat"].append(g.hashcat)
            res["john"].append(g.john)
            c += 1
        if (c == 0):
            raise Exception()
        ret = f"""
**Hash:** `{hash}`

Results ({c} guess(es)):
```
Hash                                              Hashcat            John
|------------------------------------------------|----------|------------------"""
        for i in range(len(res["names"])):
            before = ret
            h = __formatout__("Hash", str((res["names"])[i]))
            hc = __formatout__("Hashcat", str((res["hashcat"])[i]))
            j = str((res["john"])[i])
            ret += f"""
{h}{hc}{j}"""
            if (len(ret) > 2000):
                ret = before
                break
        ret +="```"
        
    except:
        ret = f"Could not identify hash algorithm."
    
    return ret

def __formatout__(type, content):
    final = ""
    spaces = ""
    length = len(content)

    if (type == "Hash"):
        spaces = " " * (50 - length)
    elif (type == "Hashcat"):
        spaces = " " * (11 - length)

    final = content + spaces

    return final

def __convert__(hashid):
    if (hashid == "SHA-1"):
        return "sha1"
    elif (hashid == "MD5" or hashid == "MD2" or hashid == "MD4"):
        return "md5"
    elif (hashid == "SHA-224"):
        return "sha224"
    elif (hashid == "SHA-256" or hashid == "Snefru-256"):
        return "sha256"
    elif (hashid == "SHA3-224"):
        return "sha3-224"
    elif (hashid == "SHA3-256"):
        return "sha3-256"
    elif (hashid == "SHA3-384"):
        return "sha3-384"
    elif (hashid == "SHA3-512"):
        return "sha3-512"
    elif (hashid == "SHA-384"):
        return "sha384"
    elif (hashid == "SHA-512"):
        return "sha512"
    elif (hashid == "RIPEMD-160"):
        return "ripemd160"
    else:
        return None