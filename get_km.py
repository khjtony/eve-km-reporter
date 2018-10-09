import urllib.request
import urllib.parse
import json
from pprint import pprint

url = 'https://redisq.zkillboard.com/listen.php'
while(True):
    res = urllib.request.urlopen(url)
    res = json.load(res)
    if(res['package'] == 'null'):
        continue
    else:
        try:
            character_url = 'https://esi.evetech.net/latest/characters/{}/?datasource=tranquility'.format(res['package']['killmail']['victim']['character_id'])
            character_res = urllib.request.urlopen(character_url)
            character_res = json.load(character_res)
            print('[{}] {} has been killed. Lost is {} isk.'.format(res['package']['killmail']['killmail_time'], character_res['name'], res['package']['zkb']['totalValue']))
        except:
            continue
