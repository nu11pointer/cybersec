import requests
import urllib
from bs4 import BeautifulSoup
from discord import ActionRow, Button, ButtonStyle

def search(query):
    components = None
    headers = {"User-Agent": "Mozilla/5.0 CyberSec"}
    pre = requests.post("https://consent.google.com/save?continue=https://www.google.com/&gl=GB&m=0&pc=shp&x=5&src=2&hl=en&bl=gws_20230417-0_RC2&uxe=none&set_eom=true", headers=headers)
    url = "https://www.google.com/search?q="
    encoded_query = urllib.parse.quote_plus(f"{query}", safe=":")
    url += encoded_query
    req = requests.get(url, headers=headers, cookies=pre.cookies)
    if (req.status_code == 429):
        response = "Too many requests! Wait a few minutes and try again."
        return response, components
    soup = BeautifulSoup(req.text, 'html.parser')
    results = []
    for entry in soup.find_all('div', class_="Gx5Zad fP1Qef xpd EtOod pkphOe"):
        title = entry.find('h3').div.get_text()
        link = entry.find('a')['href'].split("=")[1].split("&")[0]
        description = entry.find('div', class_="BNeawe s3v9rd AP7Wnd").div.div.div.get_text()
        results.append({'title': title, 'link': link, 'description': description})
    
    q = query.split("site:ctftime.org inurl:writeup")[1].strip()
    response = f"**Query:** `{q}`"
    response += f"""

Results:
```
"""
    for i in range(len(results)):
        try:
            r = results[i]
            length = len(r["title"])
            for z in range(length + 7):
                response += "~"
            response += "\n"
            
            response += "| " + f"{i + 1}. "
            response += r["title"] + " |\n"
            for z in range(length + 7):
                response += "~"
            response += "\n\t" + r["description"].replace("`", "")
            response += "\n\n"
        except:
            return "Error while performing query.", None

        if i == 4:
            break

    response += "```"
    
    if (len(results) >= 5):
        components = ActionRow(
                Button(label="", style=ButtonStyle.red, emoji="1️⃣", url=results[0]["link"]),
                Button(label="", style=ButtonStyle.red, emoji="2️⃣", url=results[1]["link"]),
                Button(label="", style=ButtonStyle.red, emoji="3️⃣", url=results[2]["link"]),
                Button(label="", style=ButtonStyle.red, emoji="4️⃣", url=results[3]["link"]),
                Button(label="", style=ButtonStyle.red, emoji="5️⃣", url=results[4]["link"])
            )
    return response, components
