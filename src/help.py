from src.hashes import ALGS
from src.version import __version__

SUBS = ["crack", "cve", "decode", "encode", "env", "exploit", "hashid", "hello", "help", "listener", "ping", "revshell", "set", "shellcode", "shodan", "vt", "writeup"]

def help():
    return f"""
```
Command     Description
------      -------
crack       crack a hash
cve         get details from a CVE
decode      decode a given string
encode      encode a given string
exploit     search for exploits
hashid      identify hash algorithms
hello       be nice and greet me
help        shows this page
listener    reverse shell listener generator
ping        check the bot latency
revshell    generate reverse shell code/script
shellcode   search for shellcode
shodan      search on shodan
vt          search for a given hash on VirusTotal
writeup     search for CTFtime writeups

Command     Arguments
------      ------
crack       <algorithm> <hash>
cve         <CVE>
decode      <encoding> <text>
encode      <encoding> <text>
exploit     <keyword> [<keyword> ...]
hashid      <hash>
help        [<command>]
listener    <type> <port>
revshell    <type> <host> <port> <shell>
shellcode   <keyword> [<keyword> ...]
shodan      <keyword> [<keyword> ...]
vt          <hash>
writeup     <keyword> [<keyword> ...]
```
`v{__version__}`
"""

def help_admin():
    return f"""
```
Command     Description
------      -------
crack       crack a hash
cve         get details from a CVE
decode      decode a given string
encode      encode a given string
env         display the API keys
exploit     search for exploits
hashid      identify hash algorithms
hello       be nice and greet me
help        shows this page
listener    reverse shell listener generator
ping        check the bot latency
revshell    generate reverse shell code/script
set         modify API keys or bot prefix
shellcode   search for shellcode
shodan      search on shodan
vt          search for a given hash on VirusTotal
writeup     search for CTFtime writeups

Command     Arguments
------      ------
crack       <algorithm> <hash>
cve         <CVE>
decode      <encoding> <text>
encode      <encoding> <text>
exploit     <keyword> [<keyword> ...]
hashid      <hash>
help        [<command>]
listener    [<type>] [<port>]
revshell    <type> <host> <port> [<shell>]
set         <prefix|API Variable> <value>
shellcode   <keyword> [<keyword> ...]
shodan      <keyword> [<keyword> ...]
vt          <hash>
writeup     <keyword> [<keyword> ...]
```
`v{__version__}`
"""

def help_crack(prefix):
    return f"""
```
Usage: {prefix}crack <algorithm> <hash>
Example: {prefix}crack sha1 b1b3773a05c0ed0176787a4f1574ff0075f7521e

Tries to find the cleartext from the provided hash.
If the algorithm is unknown by the user, the bot can try to find the algorithm by itself if 'auto' is passed as the algorithm.

Hash Algorithms
------
{", ".join(ALGS)}
```
`v{__version__}`
"""

def help_cve(prefix):
    return f"""
```
Usage: {prefix}cve <CVE>
Example: {prefix}cve CVE-2021-2012

Provides information about a certain CVE such as its description, link, base metrics (CVSSv2 and CVSSv3) and the date it was published.
```
`v{__version__}`
"""

def help_decode(prefix):
    return f"""
```
Usage: {prefix}decode <algorithm> <text>
Example: {prefix}decode b64 aGVsbG8gbWF0ZSE=

Decodes a given string.

Algorithms
------
b64 (base64), url, hex, ord (ascii decimal value), bin (binary)
```
`v{__version__}`
"""

def help_encode(prefix):
    return f"""
```
Usage: {prefix}encode <algorithm> <text>
Example: {prefix}encode b64 hello mate!

Encodes a given string.

Algorithms
------
b64 (base64), url, hex, ord (ascii decimal value), bin (binary)
```
`v{__version__}`
"""

def help_env(prefix):
    return f"""
```
Usage: {prefix}env

Returns all the API variables used by the bot and their respective values.

API Variables
------
MALSHARE_API_KEY
NVD_API_KEY
VIRUSTOTAL_API_KEY
SHODAN_API_KEY
```
`v{__version__}`
"""

def help_exploit(prefix):
    return f"""
```
Usage: {prefix}exploit <keyword> [<keyword> ...]
Example: {prefix}exploit goahead 2.18

Searches for public exploits available through Exploit-DB.
```
`v{__version__}`
"""

def help_hashid(prefix):
    return f"""
```
Usage: {prefix}hashid <hash>
Example: {prefix}hashid b1b3773a05c0ed0176787a4f1574ff0075f7521e

Try to detect the algorithm of a given hash.
```
`v{__version__}`
"""

def help_hello(prefix):
    return f"""
```
Usage: {prefix}hello

Greets the user that sent the command, by selecting one random message from a compiled source of greetings.
```
`v{__version__}`
"""

def help_help(prefix):
    return f"""
```
Usage: {prefix}help [<command>]
Example: {prefix}help revshell

Help page for general bot usage or for a specific command.
It is not required to invoke the command with an argument.

Commands
------
crack, cve, decode, encode, env, exploit, hello, help, id, listener, ping, revshell, set, shellcode, vt, writeup
```
`v{__version__}`
"""

def help_listener(prefix):
    return f"""
```
Usage: {prefix}listener [<type>] [<port>]
Example: {prefix}listener socat 1337

Generates commands to create a network listener. Useful when exploiting remote targets and in need of a reverse shell.
The command does not require any arguments. 
The command can be invoked passing only the port to listen (will present all the available listeners using the specified port).

Types
------
nc/netcat/ncat, rustcat/rcat, pwncat, powercat, socat, msf, hoaxshell, xnest
```
`v{__version__}`
"""

def help_ping(prefix):
    return f"""
```
Usage: {prefix}ping

Command used to check the bot latency. It looks like an actual ping command from a legitimate operating system, but that's just the visual feature. The latency is provided at the end of the command.
```
`v{__version__}`
"""

def help_revshell(prefix):
    return f"""
```
Usage: {prefix}revshell <type> <host> <port> [<shell>]
Example: {prefix}revshell jsp 10.10.100.132 9001 /bin/bash

Generates commands to create a reverse shell. Useful when exploiting remote targets and a listener is running.
The command does not require the shell to be provided (default: /bin/sh).

Types
------
sh/bash, nc/netcat/ncat, dart, rustcat/rcat, c, c#/cs/csharp, haskell, perl/pl, php, ps/ps1/pwsh/powershell, python3/python2/py/python, ruby/rb, socat, nodejs/node.js, java, jsp, javascript/js, groovy, telnet, zsh, lua, golang/go, vlang/v, awk, xterm, gawk"

Shells
------
sh, /bin/sh, bash, /bin/bash, cmd, powershell, powershell.exe, cmd.exe, pwsh, ash, bsh, csh, ksh, zsh, pdksh, tcsh, mksh, rbash, dash
```
`v{__version__}`
"""

def help_set(prefix):
    return f"""
```
Usage: {prefix}set <var> <value>
Example: {prefix}set prefix !

Set the bot prefix (maximum of 7 characters) or an API variable.

Variables
------
prefix
MALSHARE_API_KEY
NVD_API_KEY
VIRUSTOTAL_API_KEY
SHODAN_API_KEY
```
`v{__version__}`
"""

def help_shellcode(prefix):
    return f"""
```
Usage: {prefix}shellcode <keyword> [<keyword> ...]
Example: {prefix}shellcode bind sh

Searches for shellcode available on ShellStorm.
```
`v{__version__}`
"""

def help_shodan(prefix):
    return f"""
Usage: {prefix}shodan <keyword> [<keyword> ...]
Example: {prefix}shodan 1.1.1.1

Searches on Shodan.
```
`v{__version__}`
"""

def help_vt(prefix):
    return f"""
```
Usage: {prefix}vt <hash>
Example: {prefix}vt a04714dcfad52b9dbf2f649810a6c489c5eb2a15118043f0173571310597b8cb

Searches VirusTotal for a given hash and, besides returning information from the file related to the hash, provides the download link to the file (if available) from MalShare.
Returns the following data: detection, type, reputation, times submitted, threat label, tags, names history, strings, threat categories, file type, packers and download link.
Some data will not appear, if non-existant.
```
`v{__version__}`
"""

def help_writeup(prefix):
    return f"""
```
Usage: {prefix}writeup <keyword> [<keyword> ...]
Example: {prefix}writeup defcon qualifier 2022

Searches for available writeups on CTFtime.org.
```
`v{__version__}`
"""