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
        res = json.loads(res.read().decode('utf-8'))
        debug_flag = True 
        if(res['package'] == None):
            continue
        else:
            try:
                if(debug_flag or ('alliance_id' in res['package']['killmail']['victim'] and res['package']['killmail']['victim']['alliance_id'] in alliance_list)):
                    character_url = 'https://esi.evetech.net/latest/characters/{}/?datasource=tranquility'.format(res['package']['killmail']['victim']['character_id'])
                    character_res = urllib.request.urlopen(character_url)
                    character_res = json.loads(character_res.read().decode('utf-8'))
                    corporation_url = 'https://esi.evetech.net/latest/corporations/{}/?datasource=tranquility'.format(res['package']['killmail']['victim']['corporation_id'])
                    corporation_res = json.loads(urllib.request.urlopen(corporation_url).read().decode('utf-8'))
                    system_url = 'https://esi.evetech.net/latest/universe/systems/{}/?datasource=tranquility&language=en-us'.format(res['package']['killmail']['solar_system_id'])
                    system_res = json.loads(urllib.request.urlopen(system_url).read().decode('utf-8'))
                    ship_url = 'https://esi.evetech.net/latest/universe/types/{}/?datasource=tranquility&language=en-us'.format(res['package']['killmail']['victim']['ship_type_id'])
                    ship_res = json.loads(urllib.request.urlopen(ship_url).read().decode('utf-8'))

                    totalValue = res['package']['zkb']['totalValue']
                    if(character_res['name'] not in km_dict or totalValue not in km_dict[character_res['name']]):
                        km_msg = '[熊当当KM报告] {0} 军团 {1} 驾驶的 {2} 惨死于 {3} ，损失了 {4:.2f}亿 isk.\n https://zkillboard.com/kill/{5}'.format(
                            corporation_res['name'], 
                            character_res['name'], 
                            ship_res['name'],
                            system_res['name'],
                            res['package']['zkb']['totalValue']/100000000.0, 
                            res['package']['killID'])
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


