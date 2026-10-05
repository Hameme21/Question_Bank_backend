import json
import requests

raw_cookie = (
    "_ga=GA1.1.704616745.1787159287; "
    "browserFingerprint=deviceBrowserId=c52626c7-f10a-4e10-b499-9ceb85621c3f; "
    "_ga_ZZT8JYHK0Q=GS2.1.s1788439151$o1$g0$t1788439151$j60$l0$h0; "
    "_ga_WBX63B1XWW=GS2.1.s1788784668$o2$g1$t1788785204$j60$l0$h0; "
    "_ga_2PB67RCHDL=GS2.1.s1791048577$o8$g0$t1791048577$j60$l0$h0; "
    "_ga_BYBNKJLJ9V=GS2.1.s1791135979$o49$g1$t1791137378$j14$l0$h0; "
    "ASP.NET_SessionId=0tidnxy5ygay0ia1k4zn250j; "
    ".ASPXAUTH=A001F25671799BBAC72953AB3CD4C98F173455B6AFF7B73A2E41C535BB8C943BE6EDBC90AA8CB7E84A6686584120D565DFD370EB356BF361A6E245B47B29BDB2BA77637F73CDA3C25BDD5334F7945A41A96FB204C2F7386BB0BCFEF58AD527C0B40F7340E2C6599175D11AA72557729346DC10A69C035637BD13D759EE6978A01984BC275F0EA5B2973565B31D87C1FB01A156E9C5F039DB62F7CE7E99D0893237A81A5EEC3934D8ED90B23F0FBBE1D15B430DA9FD0227513536BD2C2F5ABB8EF407E591E6AF608E980507567BD5F9D70082F9F2F8FDDDD76B33D44CE57E7CB5"
)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': raw_cookie
}

url = 'https://ucam.uiu.ac.bd/Scheduler/WeeklyRoutineViewer.aspx/GetFacultyList'

response = requests.post(url, headers=headers, json={'acId': 116})

if response.status_code != 200:
    print(f"Request failed with HTTP {response.status_code}.")
    print(response.text[:300])
    exit(1)

raw_data = response.json().get('d', [])
data = json.loads(raw_data) if isinstance(raw_data, str) else raw_data

real_faculties = []
for item in data:
    name = item.get('Text') or item.get('name') or ''
    fid = item.get('Value') or item.get('id')
    if fid and name:
        code_match = name.split('(')[-1].replace(')', '').strip() if '(' in name else ''
        real_faculties.append({
            'id': int(fid),
            'name': name,
            'code': code_match
        })

with open('faculties.json', 'w', encoding='utf-8') as f:
    json.dump(real_faculties, f, indent=2, ensure_ascii=False)

print(f"Success! Written {len(real_faculties)} real faculty records into faculties.json")