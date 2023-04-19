import requests

ALGS = ["md5",
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

def crack(alg:str, hash:str):
    global ALGS
    url = "https://api.hash-decrypt.io/v1/hash/"
    ret = ""
    found = False

    for a in ALGS:
        if (alg.lower() == a.lower()):
            found = True
            fullurl = url + a + "/" + hash
            req = requests.get(fullurl)
            if (req.status_code == 404 or req.status_code == 429):
                ret = "API is currently offline or you made too many requests to the API! Please wait a few minutes and try again."
            else:
                data = req.json()
                if (data["found"] is True):
                    ret = f"""
✅ **Cracked!**
`{data["password"]}`"""
                else:
                    ret = f"❌ **Not Cracked!**"
            break
    if (not found):
        ret = "Invalid algorithm specified!"
    return ret
