import json
import requests

cookies = {
    'ASP.NET_SessionId': 'PASTE_YOUR_ASP_NET_SESSION_ID_HERE',
    '.ASPXAUTH': 'PASTE_YOUR_ASPXAUTH_TOKEN_HERE',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest'
}

url = 'https://ucam.uiu.ac.bd/Scheduler/WeeklyRoutineViewer.aspx/GetFacultyList'

response = requests.post(url, cookies=cookies, headers=headers, json={'acId': 116})

if response.status_code != 200:
    print(f"Request failed with status code {response.status_code}")
    exit()

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

print(f"Saved {len(real_faculties)} real faculty records into faculties.json")