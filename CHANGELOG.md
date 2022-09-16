# CYBERSEC - Changelog

## 1.0.0 - 14/09/2022 - Official Release

## 1.1.0 - 16/09/2022 - Malware Sample Download

- Added a feature that lets a user download the malware sample (if available) searched via hash using the `vt` command. This feature requires a Malshare API Key (`MALSHARE_API_KEY`).
- Added a new sentence to the hello command
- Added documentation (README.md)
- Improved the help page

## 1.1.1 - 16/09/2022 - Security Bug Fix

- Fixed a small bug where the admin help page would show no matter what channel, even if the `management_channel` was active
- Fixed bug when searching for a CVE (exception if CVE would not exist)
