import requests
import json
from datetime import datetime
import time
import binascii

def hex_to_str(hex_str):
	hex = hex_str.encode('utf-8')
	str_bin = binascii.unhexlify(hex)
	return str_bin.decode('utf-8')

def search_mempool_by_addr(addr_str):
	url = "https://api.mainnet.hiro.so/extended/v1/tx/mempool?address=" + addr_str
	
	json_data = requests.get(url).json()
	results_list = json_data['results']
	
	print("\n◇ addr: ", addr_str)
	print("(receipt_time) [nonce] | fee_rate(stx) | memo")
	print("-----------------------------------------------------")
	
	for tx in results_list:
		receipt_time = datetime.fromtimestamp(tx['receipt_time'])
		receipt_time_str = receipt_time.strftime("%Y-%m-%d %H:%M:%S")
		fee_rate = int(tx['fee_rate']) / 1000000
		memo_hex = tx['token_transfer']['memo']
		memo = hex_to_str(memo_hex[2:28])
		print("(" + receipt_time_str + ") [" + str(tx['nonce']) + "] | " + str(fee_rate) + " | " + memo)

	print("-----------------------------------------------------\n")

def main():
	search_mempool_by_addr("SP24NK8TF3SVN3ZZJQE4NWAN82EH8P9R9N8C6N3NW")

# 主函数
if __name__=="__main__":
	main()
