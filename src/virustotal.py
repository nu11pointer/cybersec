import requests
import os
from discord import ActionRow, Button, ButtonStyle

VT_URL = "https://www.virustotal.com/api/v3/files/"

def submit(hash):
    headers = {"X-Apikey": os.getenv("VIRUSTOTAL_API_KEY")}
    url = VT_URL + hash.lower()
    r = requests.get(url, headers=headers)
    data = r.json()

    try:
        detected = data['data']['attributes']['last_analysis_stats']['malicious']
        if (detected) > 0:
            final = "**MALWARE DETECTED**"
    except:
        final = "**FILE NOT DETECTED**"
    
    try:
        final += f"""
```
Detection: {data['data']['attributes']['last_analysis_stats']['malicious']}/{len(data['data']['attributes']['last_analysis_results'].keys())}
Type: {data["data"]["attributes"]["type_description"]}
Reputation: {data["data"]["attributes"]["reputation"]}
Times Submitted: {data["data"]["attributes"]["times_submitted"]}
"""
        try:
            final += f'Threat Label: {data["data"]["attributes"]["popular_threat_classification"]["suggested_threat_label"]}\n'
        except:
            pass

        try:
            final += "Tags: "
            length = len(data["data"]["attributes"]["tags"])
            i = 0
            for tag in data["data"]["attributes"]["tags"]:
                if (i < length - 1):
                    final += tag + ", "
                else:
                    final += tag
                i += 1
            final += "\n"
        except:
            pass

        final += f"\nNames:\n"
        count = 0
        for name in data["data"]["attributes"]["names"]:
            final += f"\t{name}\n"
            count += 1
            if (count >= 20):
                break
        
        try:
            if (data["data"]["attributes"]["androguard"]["StringsInformation"]):
                final += f"\nStrings:\n"
                for string in data["data"]["attributes"]["androguard"]["StringsInformation"]:
                    final += f"\t{string}\n"
        except:
            pass
        
        try:
            if (data["data"]["attributes"]["popular_threat_classification"]["popular_threat_category"]):
                final += "\nThreat Categories:\n"
                for threats in data["data"]["attributes"]["popular_threat_classification"]["popular_threat_category"]:
                    final += f'\t{threats["value"]}\n'
        except:
            pass
        
        try:
            final += "\nFile Type:\n"
            for trid in data["data"]["attributes"]["trid"]:
                final += f'\t{trid["file_type"]} ({trid["probability"]})\n'
        except:
            pass
            
        try:
            if (data["data"]["attributes"]["packers"]):
                final += "\nPackers:\n"
                for packer in data["data"]["attributes"]["packers"]:
                    final += f'\t{packer}: {data["data"]["attributes"]["packers"][packer]}\n'
        except:
            pass
        
        final += f"""
```
"""
    except Exception:
        final = "Invalid hash or hash not found!"

    components = ActionRow(Button(label="Details", style=ButtonStyle.red, emoji="🔗", url=f"https://virustotal.com/gui/file/{hash}"))
    
    return final, components