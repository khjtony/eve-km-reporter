import urllib.request
import urllib.parse
import sys
import json
from pprint import pprint

url = 'https://redisq.zkillboard.com/listen.php'
alliance_list = [99007362]
km_dict = {}
while(True):
    res = urllib.request.urlopen(url)
    res = json.load(res)
    debug_flag =False 
    if(res['package'] == None):
        continue
    else:
        try:
            if(debug_flag or ('alliance_id' in res['package']['killmail']['victim'] and res['package']['killmail']['victim']['alliance_id'] in alliance_list)):
                character_url = 'https://esi.evetech.net/latest/characters/{}/?datasource=tranquility'.format(res['package']['killmail']['victim']['character_id'])
                character_res = urllib.request.urlopen(character_url)
                character_res = json.load(character_res)
                corporation_url = 'https://esi.evetech.net/latest/corporations/{}/?datasource=tranquility'.format(res['package']['killmail']['victim']['corporation_id'])
                corporation_res = json.load(urllib.request.urlopen(corporation_url))
                totalValue = res['package']['zkb']['totalValue']
                if(character_res['name'] not in km_dict or totalValue not in km_dict[character_res['name']]):
                      print('[{}]{}军团的{}惨死，损失了{} isk.'.format(res['package']['killmail']['killmail_time'], corporation_res['name'], character_res['name'], res['package']['zkb']['totalValue']))
                      if(character_res['name'] not in km_dict):
                          km_dict[character_res['name']] = []
                      km_dict[character_res['name']].append(totalValue)
        except Exception as e:
            pprint(res)
            pprint(e.args)
            continue
