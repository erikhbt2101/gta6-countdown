import datetime as dt
import json
import os
import urllib.error
import urllib.request

TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = os.environ['DISCORD_CHANNEL_ID']
# Set to the actual release instant once confirmed.
TARGET = dt.datetime.fromisoformat(os.getenv('RELEASE_DATETIME', '2026-11-19T00:00:00+01:00'))
now = dt.datetime.now(dt.timezone.utc)
seconds = max(0, int((TARGET.astimezone(dt.timezone.utc) - now).total_seconds()))
if seconds == 0:
    name = '🌴・gta-vi-megjelent'
else:
    days, hours = divmod(seconds // 3600, 24)
    name = f'🌴・gta-vi-{days}nap-{hours}ora'

url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}'
headers = {'Authorization': f'Bot {TOKEN}', 'User-Agent': 'Morgo2101-GTA6-Countdown/1.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=20) as response:
    current = json.load(response)
if current.get('name') == name:
    print(f'Already current: {name}')
else:
    data = json.dumps({'name': name}).encode()
    req = urllib.request.Request(url, data=data, headers={**headers, 'Content-Type': 'application/json'}, method='PATCH')
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            print('Updated channel:', json.load(response)['name'])
    except urllib.error.HTTPError as exc:
        print('Discord API error:', exc.code, exc.read().decode()[:1000])
        raise
