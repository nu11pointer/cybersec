# CYBERSEC DISCORD BOT

> An easy to use cybersecurity discord bot that attempts to make the life easier for individuals, teams and groups interested in researching, sharing, learning, or even playing some CTFs.

## DESCRIPTION

This bot makes use of several APIs and google dorks to search for the intended content.  
Features:

- Encode and decode text to or from `base64` and `URL`
- Search for CTF writeups, on [CTFtime](https://ctftime.org/), related to given keywords
- Verify if an hash belongs to a malicious file and get the details from that file
- Download malware samples by simply providing its hash
- Search and find details of CVEs

You should register on the platforms listed below to retrieve the API keys and get the full potential of the bot.

Used APIs:

- [Google](https://cloud.google.com/docs/authentication/api-keys)
- [NVD](https://nvd.nist.gov/developers/request-an-api-key)
- [Malshare](https://malshare.com/register.php)
- [Virustotal](https://www.virustotal.com/gui/join-us)

For security and management purposes, there are 2 log files being used: `access.log` and `error.log`. The first one reveals when, who and how a user tried to execute sensitive commands on the bot. The other one outlines runtime errors that might arouse from the bot. These are stored in the `logs` folder (created when the bot is executed for the first time).

*Note: The amount of information given by the several API commands (such as `search`, `vt` and `cve`) will depend on the availability from those external services and the amount of data retrieved from the search results. Some results contain more information than others.*

## INSTALL

To install the bot it's as simple as cloning the repository and installing the python requirements:

```sh
git clone https://github.com/fssecur3/cybersec
cd cybersec
pip install -r requirements.txt
```

You can set up the API keys right away by creating environment variables with the names shown at the end of the README and setting their value to the key. If you want to set them up later, you can use the bot command `set` to set the API keys.

## USAGE

There are some arguments (required and optional) to be passed when starting the bot:

```text
usage: main.py [-h] -r role [-c channel] [-p prefix] [-V]

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit

Settings:
  -r role, --management-role role               Management role
  -c channel, --management-channel channel      Management channel
  -p prefix, --prefix prefix                    Bot prefix (default: $)
```

The only required argument is the `management role`. Since API keys are sensitive content, only certain members (with a given role) should be able to see that content. You can specify that role using the `-r` tag. You can also, optionally, specify a text channel, with the `-c` flag, that forces the bot to only reply to sensitive commands (such as `env` and `set`) on that channel. This way, a manager/administrator can use the bot safely on community text channels without leaking any API keys or changing the bot settings.  
The prefix length is limited to a maximum of 7 characters, in case you want to change it (prefix suggestion: '`sudo `' 😉).

## HELP

On discord, you can get the bot help page by simply sending $help to the chat. The bot should answer with the following list of commands:

```text
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

## EXAMPLES

1. Searching for a CVE

Command: `$cve CVE-2020-1921`
![CVE](img/1.png)

2. Getting information about a file hash and download link

Command: `$vt 84c82835a5d21bbcf75a61706d8ab549`
![VT](img/2.png)

3. Searching for writeups

Command: `$search format string pie`
![CTF](img/3.png)

4. Encoding text

Command: `$encode b64 hello there`
![B64](img/4.png)

***Enjoy! 🙂***
