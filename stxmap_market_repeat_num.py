import requests
import json
from datetime import datetime
import time
import binascii
import csv

def hex_to_str(hex_str):
	hex = hex_str.encode('utf-8')
	str_bin = binascii.unhexlify(hex)
	return str_bin.decode('utf-8')

def check_repeat_num(map_str) :
	repeat_str = ""
	cnt = 1
	lt_list = list(map_str)
	lt = lt_list[0]
	i = 1
	while i < len(lt_list) :
		if lt == lt_list[i] :
			cnt += 1
		else :
			lt = lt_list[i]
			cnt = 1
		
		if cnt == 3 :
			repeat_str += "[3]"
		elif cnt == 4 :
			repeat_str += "[4]"
		elif cnt == 5 :
			repeat_str += "[5]"
		elif cnt == 6 :
			repeat_str += "[6]"
		
		i += 1
	
	return repeat_str
	
def stxmap_market_repeat_num():
	map_list = []
	url = "https://api.stx-info.com/listings"
	headers = {"Content-Type": "application/json; charset=UTF-8"}
	
	try :
		json_data = requests.get(url, headers=headers,verify=False).json()
		
		for item in json_data :
			map_str = item['map']
			mapId = item['mapId']
			stxValue = int(item['stxValue']) / 1000000
			pendingPurchaseTx = item['pendingPurchaseTx']
			if len(pendingPurchaseTx) == 0 :
				map = {'map_str' : map_str, 'mapId' : mapId, 'stxValue' : stxValue}
				map_list.append(map)
	except Exception as e:
		print(e)
		
	map_list.sort(key = lambda k: (k.get('stxValue', 0)))
	for idx, map in enumerate(map_list) :
		repeat_str = check_repeat_num(map['map_str'] )
		if repeat_str != "" :
			print(map['map_str'] + "  " + repeat_str + " : " + str(map['stxValue']))
		mapId = map['mapId']
		#if mapId < 100 :
		#	print(map['map_str'] + " <2D> : " + str(map['stxValue']))
		#elif mapId < 1000 :
		#	print(map['map_str'] + " <3D> : " + str(map['stxValue']))
		#elif mapId < 10000 :
		#	print(map['map_str'] + " <4D> : " + str(map['stxValue']))
	

def main():
	stxmap_market_repeat_num()

# 主函数
if __name__=="__main__":
	main()
