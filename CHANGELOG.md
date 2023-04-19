# CYBERSEC - Changelog

## 1.0.0 - 14/09/2022 - Official Release

## 1.1.0 - 16/09/2022 - Malware Sample Download

- Added a feature that lets a user download the malware sample (if available) that was searched via hash using the `vt` command. This feature requires a Malshare API Key (`MALSHARE_API_KEY`)
- Added a new sentence to the hello command
- Added documentation (README.md)
- Improved the help page

## 1.1.1 - 16/09/2022 - Security Bug Fix

- Fixed a small bug where the admin help page would show no matter what channel, even if the `management_channel` was active
- Fixed bug when searching for a CVE (exception if CVE would not exist)

## 1.2.0 - 16/10/2022 - Searching for exploits

- Added an install script that automatically installs all the requirements to run the bot
- You are now able to search for exploits (like you do when using searchsploit), using the Exploit DB, calling the `exploit` command
- Now, instead of using `search` to search for writeups, you should use `writeup`
- Small improvements on the overall usage
- Documentation improvements

## 1.2.1 - 16/10/2022 - Bug fixes

- Fixed (empty) response of when there are no results for a writeup search
- Fixed badly formatted response when it contains ` ``` ` in the results of a writeup search
- Changed exploit search structure (has a new source file dedicated to it)
- Fixed no response when no results were found while searching for exploits
- Fixed no responde when too many results were found while searching for exploits
- Fixed no escaping of `"` in logs.
- Now the exploit search results provide the number of exploits found
- Disabled writeup search for now (API permissions problem yet to be solved)

## 1.2.2 - 18/04/2023 - Bug fixes

- Exploit command was down due to outdated source

## 1.3.0 - 19/04/2023 - Hash cracker

- Fixed unauthorized access logging bug which was raising exception
- New command "crack" - has the ability to try and "crack" a hash by accessing the Hash-Decrypt API
- Removed the Google API
- Fixed writeup searching
- Interface improvement
- Fixed writeup flaw which caused interface bugs when containing ` characters in the description

## 1.3.1 - 19/04/2023 - Bug fixes

- Fixed requirements
- Fixed path joining issues
