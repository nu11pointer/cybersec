import os
from googleapiclient.discovery import build
from discord import ActionRow, Button, ButtonStyle

def search(query):
    searchengineId='30caf11dcffda85e3'
    service = build("customsearch", "v1", developerKey = os.getenv("GOOGLE_API_KEY"))
    abc = query.split("site:ctftime.org inurl:writeup")[1].strip()
    response = f"**Query:** `{abc}`"
    response += f"""

```
Results:"""
    results = service.cse().list(q=query, cx=searchengineId).execute()
    if "items" in results.keys():
        results = results["items"]
    else:
        results = ""
        return results, None

    for i in range(len(results)):
        try:
            r = results[i]
            response += f"\n{i + 1}  |  {r['snippet'][0:145]}..."
        except:
            break
        if i == 4:
            break
    
    """
    if (len(response) > 1997):
        response = response[:1997]
    if (len(response) == 1997):
        response += "..."
    """
    
    response += "\n```"
    
    components = None

    components = ActionRow(
        Button(label="", style=ButtonStyle.red, emoji="1️⃣", url=results[0]["link"]),
        Button(label="", style=ButtonStyle.red, emoji="2️⃣", url=results[1]["link"]),
        Button(label="", style=ButtonStyle.red, emoji="3️⃣", url=results[2]["link"]),
        Button(label="", style=ButtonStyle.red, emoji="4️⃣", url=results[3]["link"]),
        Button(label="", style=ButtonStyle.red, emoji="5️⃣", url=results[4]["link"]),
        #Button(label="", style=ButtonStyle.red, emoji="6️⃣", url=results[5]["link"]),
        #Button(label="", style=ButtonStyle.red, emoji="7️⃣", url=results[6]["link"]),
        #Button(label="", style=ButtonStyle.red, emoji="8️⃣", url=results[7]["link"]),
        #Button(label="", style=ButtonStyle.red, emoji="9️⃣", url=results[8]["link"]),
        #Button(label="", style=ButtonStyle.red, emoji="🔟", url=results[9]["link"])
    )
    return response, components