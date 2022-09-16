import requests
import os
import re
from discord import ActionRow, Button, ButtonStyle

CVE_URL = "https://services.nvd.nist.gov/rest/json/cve/1.0/"

def cve(cve):
    r = requests.get(CVE_URL + cve.lower() +"?apiKey=" + os.getenv("NVD_API_KEY"))
    data = r.json()
    html = requests.get('https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword='+cve)
    try:
        description = re.split(r".*<\/a><\/td>\\n\\t\\t<td valign=\"top\">(.*)\\n\\n<\/td>\\n\\t<\/tr>\\n\\n<\/table>.*" , str(html.content))[1]
        final = f'''
**{data['result']['CVE_Items'][0]['cve']['CVE_data_meta']['ID']}**
```
Link: {data['result']['CVE_Items'][0]['cve']['references']['reference_data'][0]['url']}

Published Date: {data['result']['CVE_Items'][0]['publishedDate'].split('T')[0]}

Description: 
{description}
'''
        if ('baseMetricV3' in data['result']['CVE_Items'][0]['impact'].keys()):
            final += f'''
Base Metrics V3:
    Vector:                 {data['result']['CVE_Items'][0]['impact']['baseMetricV3']['cvssV3']['attackVector']}
    Complexity:             {data['result']['CVE_Items'][0]['impact']['baseMetricV3']['cvssV3']['attackComplexity']}
    Privileges Required:    {data['result']['CVE_Items'][0]['impact']['baseMetricV3']['cvssV3']['privilegesRequired']}
    Base Score:             {data['result']['CVE_Items'][0]['impact']['baseMetricV3']['cvssV3']['baseScore']}
    Severity:               {data['result']['CVE_Items'][0]['impact']['baseMetricV3']['cvssV3']['baseSeverity']}
    Impact Score:           {data['result']['CVE_Items'][0]['impact']['baseMetricV3']['impactScore']}
    Exploitability Score:   {data['result']['CVE_Items'][0]['impact']['baseMetricV3']['exploitabilityScore']}
'''
        if ('baseMetricV2' in data['result']['CVE_Items'][0]['impact'].keys()):
            final += f'''
Base Metrics V2:
    Vector:                 {data['result']['CVE_Items'][0]['impact']['baseMetricV2']['cvssV2']['accessVector']}
    Complexity:             {data['result']['CVE_Items'][0]['impact']['baseMetricV2']['cvssV2']['accessComplexity']}
    BaseScore:              {data['result']['CVE_Items'][0]['impact']['baseMetricV2']['cvssV2']['baseScore']}
    Severity:               {data['result']['CVE_Items'][0]['impact']['baseMetricV2']['severity']}
    ImpactScore:            {data['result']['CVE_Items'][0]['impact']['baseMetricV2']['impactScore']}
    Exploitability Score:   {data['result']['CVE_Items'][0]['impact']['baseMetricV2']['exploitabilityScore']}
'''
        final += "```"
    except:
        final = "Couldn't get information for the provided CVE."

    components = ActionRow(Button(label="Details", style=ButtonStyle.blurple, emoji="🔗", url=f"https://nvd.nist.gov/vuln/detail/{cve}"))

    return final, components