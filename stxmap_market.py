import requests
import json
from datetime import datetime
import time
import binascii

def hex_to_str(hex_str):
	hex = hex_str.encode('utf-8')
	str_bin = binascii.unhexlify(hex)
	return str_bin.decode('utf-8')

def stxmap_market():
	while 1:
		now = datetime.now()
		now_str = now.strftime("%Y-%m-%d %H:%M:%S")
		print("-- (" +now_str + ") --")
		
		page = 0
		while page < 6 :
			url = "https://api-marketplace.stx20.com/api/v1/map-sell-requests/search?sort=price_asc&page=" + str(page) + "&limit=500"
			headers = {"Content-Type": "application/json; charset=UTF-8"}
			
			try :
				#print(url)
				json_data = requests.post(url, headers=headers).json()
				map_list = json_data['data']
				
				for map in map_list :
					map_str = map['map']
					mapId = map['mapId']
					stxValue = int(map['stxValue']) / 1000000
					pendingPurchaseTx = map['pendingPurchaseTx']
					if len(pendingPurchaseTx) == 0 :
						#3D
						if mapId < 1000 and stxValue <= 10 :
							print("[3D] mapId: [" + map_str + "] price: " + str(stxValue) + "\a")
						#4D
						elif mapId < 10000 and stxValue <= 3 :
							print("[4D] mapId: [" + map_str + "] price: " + str(stxValue) + "\a")
					#回文
					if len(pendingPurchaseTx) == 0 and map_str == map_str[::-1] and stxValue <= 10 :
						print("[DP] mapId: [" + map_str + "] price: " + str(stxValue) + "\a")
			except Exception as e:
				print(e)
				time.sleep(15)
			
			page += 1
		
		time.sleep(15)

def main():
	stxmap_market()

# 主函数
if __name__=="__main__":
	main()
