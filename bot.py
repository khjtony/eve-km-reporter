from qqbot import _bot as qbot
import urllib.request
import urllib.parse
import sys
import json
from pprint import pprint

def km_get(qbot, group):
    url = 'https://redisq.zkillboard.com/listen.php'
    alliance_list = [99007362]
    km_dict = {}
    while(True):
        res = urllib.request.urlopen(url)
        res = json.load(res)
        debug_flag = False 
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
                        km_msg = '[熊当当KM报告] {}军团的{}惨死，损失了{} isk.\n https://zkillboard.com/kill/{}'.format(corporation_res['name'], character_res['name'], res['package']['zkb']['totalValue'], res['package']['killID'])
                        if(not debug_flag):
                            qbot.SendTo(group, km_msg)
                        print(km_msg)

                          
                        if(character_res['name'] not in km_dict):
                            km_dict[character_res['name']] = []
                        km_dict[character_res['name']].append(totalValue)
            except Exception as e:
                pprint(e.args)
                continue

qbot.Login(['-q', '254533538'])
RR_group = qbot.List('group', 'RR游骑兵-为战而生')
if(RR_group):
    group = RR_group[0]
    km_get(qbot, group)


