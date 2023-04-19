import os

def env():
    res = f"""
```
NVD_API_KEY         =   {os.getenv("NVD_API_KEY")}
VIRUSTOTAL_API_KEY  =   {os.getenv("VIRUSTOTAL_API_KEY")}
MALSHARE_API_KEY    =   {os.getenv("MALSHARE_API_KEY")}
```"""

    return res

def set(bot, variable=None, value=None):
    msg = ""
    
    if (not variable or not value):
        msg = f"Invalid command."
    elif (variable == "prefix"):
        if (len(value) > 7):
            msg = f"New prefix is too long!"
        else:
            bot.command_prefix = value
            msg = f"Prefix changed to {bot.command_prefix} successfully."
    elif (variable == "NVD_API_KEY" or variable == "VIRUSTOTAL_API_KEY" or variable == "MALSHARE_API_KEY"):
        os.environ[variable] = value
        msg = f"API key has been set successfully."
    else:
        msg = f"Invalid command."
    
    return msg