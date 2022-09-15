import os

def env():
    res = f"""
```
NVD_API_KEY         =   {os.getenv("NVD_API_KEY")}
GOOGLE_API_KEY      =   {os.getenv("GOOGLE_API_KEY")}
VIRUSTOTAL_API_KEY  =   {os.getenv("VIRUSTOTAL_API_KEY")}
```"""

    return res

def set(bot, var=None, value=None):
    msg = ""
    
    if (not var or not value):
        msg = f"Invalid command."
    elif (var == "prefix"):
        if (len(value) > 7):
            msg = f"New prefix is too long!"
        else:
            bot.command_prefix = value
            msg = f"Prefix changed to {bot.command_prefix} successfully."
    elif (var == "NVD_API_KEY"):
        os.environ[var] = value
        msg = f"API key has been set successfully."
    elif (var == "GOOGLE_API_KEY"):
        os.environ[var] = value
        msg = f"API key has been set successfully."
    elif (var == "VIRUSTOTAL_API_KEY"):
        os.environ[var] = value
        msg = f"API key has been set successfully."
    else:
        msg = f"Invalid command."
    
    return msg